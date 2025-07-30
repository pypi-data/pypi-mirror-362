"""Assets for a node-based function."""

import json
from collections.abc import Iterator
from typing import Any

from ml_adapter.api.types import AssetSource

from .cached import CachedFileAsset
from .json import JsonAsset
from .manifest import FunctionType, WithManifest

NodeDependencySpec = dict[str, str] | tuple[str, str]


class NodePackageAsset(JsonAsset[dict[str, Any]]):
    """The javascript package.json.

    When used in webscripts/plugs only the 'dependencies' section is relevant.
    """

    PATH_INCLUDES = ["package.json"]
    DEFAULT_PATH = "package.json"
    DEFAULT_PACKAGE_CONTENT = {
        "name": "waylay-function",
        "version": "1.0.0",
        "dependencies": [],
    }

    @property
    def package(self) -> dict[str, Any]:
        """Get the package json, initialize when absent."""
        if self.content is None:
            initial_content: dict[str, Any] = json.loads(
                json.dumps(self.DEFAULT_PACKAGE_CONTENT)
            )
            self.content = initial_content
        return self.content

    @property
    def dependencies(self) -> dict[str, str]:
        """Get (or initialize) the dependencies."""
        if not self.content:
            self.content = {}
        if "dependencies" not in self.package:
            self.package["dependencies"] = {}
        return self.package["dependencies"]

    def __iter__(self) -> Iterator[tuple[str, str]]:
        """Read the requirements as an iterator."""
        return self.dependencies.items.__iter__()

    def add(self, *spec: NodeDependencySpec, override=True):
        """Add dependencies, replacing an existing dependency,
        unless `override` is set to False.
        """
        new_dependencies = {
            name: dependency
            for s in spec
            for name, dependency in (
                [s]
                if isinstance(s, tuple)
                else s.items()
                if isinstance(s, dict)
                else []
            )
        }
        if override:
            self.package["dependencies"] = {
                **self.dependencies,
                **new_dependencies,
            }
        else:
            self.package["dependencies"] = {
                **new_dependencies,
                **self.dependencies,
            }
        return self.dependencies


class NodeScriptAsset(CachedFileAsset):
    """A python script."""

    PATH_INCLUDES = ["*.ts", "*.js"]
    DEFAULT_PATH = "index.js"

    async def load_content(self, **_kwargs):
        """Cache the content."""
        with open(self.location, encoding="utf-8") as f:
            self.content = "".join(f.readlines())

    async def save_content(self, **_kwargs):
        """Write the cached content."""
        if self.content:
            with open(self.location, "w", encoding="utf-8") as f:
                f.write(self.content)


class NodeFunctionAdapter(WithManifest):
    """Adapter for node based plugs or webscripts.

    * `package` handles the project file (at `package.json`)
    * `main_script` handles the main script of the function (`index.js` or `index.ts`)
    * `scripts` handles other utility scripts of the function (`*.js`,`*.ts`)
    """

    DEFAULT_RUNTIME: dict[FunctionType, str] = {
        "webscripts": "web-legacy",
        "plugs": "plug-node",
    }
    MAIN_SCRIPT_NAME = "index.js"
    MAIN_SCRIPT_PATHS = [MAIN_SCRIPT_NAME, "index.ts"]

    def __init__(self, **kwargs):
        """Register the requirements asset classes."""
        super().__init__(**kwargs)
        self.assets.asset_classes.extend(
            [
                NodeScriptAsset,
                NodePackageAsset,
            ]
        )
        self.assets.add(NodeScriptAsset)
        self.assets.add(NodePackageAsset)

    @property
    def package(self) -> NodePackageAsset:
        """The asset holding the dependencies."""
        return self.assets.get_or_fail(asset_type=NodePackageAsset)

    async def add_script(
        self, source: AssetSource, path: str | None = None
    ) -> NodeScriptAsset:
        """Add a (main) script.

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
        return await self.assets.add_from(NodeScriptAsset, source=source, path=path)

    @property
    def main_script(self) -> NodeScriptAsset:
        """The main python script."""
        return self.assets.get_or_fail(NodeScriptAsset, self.MAIN_SCRIPT_PATHS)

    @property
    def scripts(self) -> Iterator[NodeScriptAsset]:
        """The main python script."""
        return self.assets.iter(NodeScriptAsset)
