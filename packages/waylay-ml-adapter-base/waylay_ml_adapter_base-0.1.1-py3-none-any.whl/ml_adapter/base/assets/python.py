"""Python dependencies as a function asset."""

import re
from collections import namedtuple
from collections.abc import Iterator, Mapping

from .base import AssetsFolder, AssetSource, FileAsset
from .cached import CachedFileAsset
from .manifest import FunctionType, WithManifest


class PythonRequirementsAsset(CachedFileAsset[list[str]]):
    """The python requirements.txt."""

    PATH_INCLUDES = ["requirements.txt"]
    DEFAULT_PATH = "requirements.txt"

    def __init__(self, *args, **kwargs):
        """Create a requirements asset, with empty list as default."""
        super().__init__(*args, **kwargs)
        self.content = []

    async def load_content(self, **_kwargs):
        """Cache the content."""
        with open(self.location, encoding="utf-8") as f:
            self.content = [line.strip() for line in f.readlines()]

    async def save_content(self, **_kwargs):
        """Write the cached content."""
        with open(self.location, "w", encoding="utf-8") as f:
            for line in self.requirements:
                f.write(f"{line}\n")

    @property
    def requirements(self) -> list[str]:
        """Get (or initialize) the dependency requirements."""
        if not self.content:
            self.content = []
        return self.content

    def __iter__(self) -> Iterator[str]:
        """Read the requirments as an iterator."""
        return self.requirements.__iter__()

    def add(self, *dependency: str, replace_same_env=True):
        """Add a dependency, replacing an existing dependency for the same name/extra.

        With `replace_same_env=False`,
        only existing dependencies with same name, extra AND condition is replaced.
        """
        self.content = PEP508.requirements(
            {
                **PEP508.mapping(
                    *self.requirements, by_env_condition=not replace_same_env
                ),
                **PEP508.mapping(*dependency, by_env_condition=not replace_same_env),
            }
        )
        return self.requirements

    def add_default(self, *dependency: str, default_different_env=True):
        """Add a default dependency.

        An existing dependency has priority for same name/extra/condition.
        With `default_different_env=False`,
        an existing dependency has priority for same name/extra.
        """
        self.content = PEP508.requirements(
            {
                **PEP508.mapping(*dependency, by_env_condition=default_different_env),
                **PEP508.mapping(
                    *self.requirements, by_env_condition=default_different_env
                ),
            }
        )
        return self.requirements


class PythonLibraryAsset(FileAsset):
    """An installable python library."""

    PATH_INCLUDES = ["*.tar.gz"]


class PythonScriptAsset(CachedFileAsset):
    """A python script."""

    PATH_INCLUDES = ["*.py"]
    DEFAULT_PATH = "main.py"

    async def load_content(self, **_kwargs):
        """Cache the content."""
        with open(self.location, encoding="utf-8") as f:
            self.content = "".join(f.readlines())

    async def save_content(self, **_kwargs):
        """Write the cached content."""
        if self.content:
            with open(self.location, "w", encoding="utf-8") as f:
                f.write(self.content)


class PythonLibAssetDir(AssetsFolder):
    """Default location for packaged libraries."""

    DEFAULT_PATH = "lib"
    PATH_INCLUDES = [DEFAULT_PATH]
    DEFAULT_ASSET_CLASSES = [PythonLibraryAsset]

    async def add_library(
        self,
        source: AssetSource,
        path: str | None = None,
        requirement: str | None = None,
    ):
        """Add a library as a asset and as requirement."""
        library = await self.add_from(PythonLibraryAsset, source, path=path)
        requirements = self.parent.get_or_fail(PythonRequirementsAsset)
        if requirement:
            requirements.add(f"--find-links {library.parent.full_path}")
            requirements.add(requirement)
        else:
            requirements.add(library.full_path)
        return library


class PythonFunctionAdapter(WithManifest):
    """Adapter for python based plugs or webscripts.

    * `requirements` handles the dependency file (at `requirements.txt`)
    * `lib` handles the libraries that are uploaded with
       the function archive itself. (at `lib/*.tar.gz`)
    * `main_script` handles the main script of the function (`main.py`)
    * `scripts` handles other utility scripts of the function (`*.py`)
    """

    DEFAULT_RUNTIME: dict[FunctionType, str] = {
        "webscripts": "web-python3",
        "plugs": "plug-python3",
    }
    MAIN_SCRIPT_NAME = "main.py"
    MAIN_SCRIPT_PATHS = [MAIN_SCRIPT_NAME]

    def __init__(self, **kwargs):
        """Register the requirements asset classes."""
        super().__init__(**kwargs)
        self.assets.asset_classes.extend(
            [
                PythonRequirementsAsset,
                PythonLibAssetDir,
                PythonScriptAsset,
            ]
        )
        self.assets.add(PythonRequirementsAsset)
        self.assets.add(PythonScriptAsset)
        self.assets.add(PythonLibAssetDir)

    @property
    def requirements(self) -> PythonRequirementsAsset:
        """The asset holding python requirements."""
        return self.assets.get_or_fail(asset_type=PythonRequirementsAsset)

    @property
    def lib(self) -> PythonLibAssetDir:
        """The lib dir holding python libraries."""
        return self.assets.get_or_fail(
            PythonLibAssetDir, PythonLibAssetDir.DEFAULT_PATH
        )

    async def add_script(
        self, source: AssetSource, path: str | None = None
    ) -> PythonScriptAsset:
        """Add a (main) python script.

        Parameters
        ----------
        source : AssetSource
            Either:
            - A string or Path that indicates the source for the asset.
            - A (text or binary) I/O object such as `io.StringIO`.
        path   : str | None
            The target location path within the function assets.
            Can be omitted if the source is path-like,
            and has the same location in the assets archive.

        """
        return await self.assets.add_from(PythonScriptAsset, source=source, path=path)

    async def add_library(
        self,
        source: AssetSource,
        path: str | None = None,
        requirement: str | None = None,
    ) -> PythonLibraryAsset:
        """Add a (main) python script."""
        return await self.lib.add_library(
            source=source, path=path, requirement=requirement
        )

    @property
    def main_script(self) -> PythonScriptAsset:
        """The main python script."""
        return self.assets.get_or_fail(PythonScriptAsset, "main.py")

    @property
    def scripts(self) -> Iterator[PythonScriptAsset]:
        """The main python script."""
        return self.assets.iter(PythonScriptAsset)


ParsedDependency = namedtuple("ParsedDependency", "name, spec, marker")


class PEP508:
    """Utilities related to python package dependency specifications.

    See https://peps.python.org/pep-0508
    """

    RE_DEPENDENCY = re.compile(
        r"^\s*(?P<name>[^\<\!\=\>@;]*)\s*(?P<spec>[\<\!\=\>@][^;]*)?\s*(?P<marker>;.*)?\s*$"
    )

    @staticmethod
    def parse(*dependency: str) -> Iterator[ParsedDependency]:
        """Parse dependency specifications."""
        for dep in dependency:
            match = PEP508.RE_DEPENDENCY.match(dep)
            if match:
                yield ParsedDependency(**match.groupdict())
            else:
                yield ParsedDependency(dep, "", "")

    @staticmethod
    def mapping(
        *dependency: str, by_env_condition=True
    ) -> Mapping[str, ParsedDependency]:
        """Create a mapping from identifier;marker->parsed dependency."""
        return {
            f"{dep.name}{dep.marker or ''}" if by_env_condition else dep.name: dep
            for dep in PEP508.parse(*dependency)
        }

    @staticmethod
    def requirements(parsed_deps: Mapping[str, ParsedDependency]) -> list[str]:
        """Render a mapping with ParsedDependency values to a requirement lists."""
        return list(
            f"{parsed_dep.name}{parsed_dep.spec or ''}{parsed_dep.marker or ''}"
            for parsed_dep in parsed_deps.values()
        )
