"""Utility functions for accessing assets."""

import abc
import fnmatch
import io
import logging
import shutil
import tarfile
from collections.abc import Iterator
from pathlib import Path
from typing import Self, TypeVar, cast

from ml_adapter.api.types import (
    AssetLocation,
    AssetLocationLike,
    AssetSource,
    as_location,
)

from . import _err

LOG = logging.getLogger(__name__)
A = TypeVar("A", bound="Asset")

PathFilter = str | list[str] | None

NO_DEFAULT_PATH = "__?__"


class Asset(abc.ABC):
    """Item(s) that can be saved/loaded as asset(s) for a waylay function."""

    parent: "AssetsFolder"
    path: str

    PATH_INCLUDES: list[str] = ["*"]
    PATH_EXCLUDES: list[str] = [".*"]
    DEFAULT_PATH: str = NO_DEFAULT_PATH

    def __init__(self, parent: "AssetsFolder", path: str | None = None, **_kwargs):
        """Create an asset in the given assets directory."""
        self.parent = parent
        if path is None and self.DEFAULT_PATH == NO_DEFAULT_PATH:
            raise ValueError(
                f"Assets of type {self.__class__.__qualname__}"
                " require a path to be specified."
            )
        self.path = path or self.DEFAULT_PATH

    @property
    def full_path(self) -> str:
        """Full path in an assets archive."""
        return self.parent.full_path + self.path

    @property
    def location(self) -> AssetLocation:
        """Path of asset(s)."""
        return self.parent.location / self.path

    @property
    @abc.abstractmethod
    def synced(self) -> bool:
        """True when the storage existence is in sync with the content."""

    @abc.abstractmethod
    def assert_synced(self):
        """Raise an approriate error if not synced."""

    @abc.abstractmethod
    async def save(self, **_kwargs) -> Self:
        """Write the asset(s) to the intended location."""

    @abc.abstractmethod
    async def load(self, **_kwargs) -> Self:
        """Sync the asset(s) from the intended location."""

    def has_content(self):
        """Check whether the asset (should) exist.

        If true, the _save_ will create storage,
            and _load_ will insist on its existence.
        If false, the _save_ will remove storage,
            and _load_ will verify that it does not exist.
        """
        return self.location.exists()

    def is_empty(self):
        """Check that no content is present."""
        return not self.has_content()

    def iter_locations(
        self,
        /,
        relative_to: AssetLocationLike | None = None,
        exclude_empty=False,
        **_kwargs,
    ):
        """Iterate the paths for the assets."""
        if exclude_empty and self.is_empty():
            return
        if relative_to:
            yield self.location.relative_to(as_location(relative_to))
        else:
            yield self.location

    def iter(
        self,
        /,
        asset_type: type[A] | None = None,
        path_includes: PathFilter = None,
        path_excludes: PathFilter = None,
        exclude_empty=False,
        **_kwargs,
    ) -> Iterator[A]:
        """Iterate the assets."""
        if exclude_empty and self.is_empty():
            return
        if not (asset_type is None or isinstance(self, asset_type)):
            return
        if not self._path_matches(self.path, path_includes, path_excludes):
            return
        yield cast(A, self)

    @classmethod
    def _path_matches(
        cls,
        path: str,
        includes: str | list[str] | None = None,
        excludes: str | list[str] | None = None,
    ) -> bool:
        excluded = _matches(path, excludes, cls.PATH_EXCLUDES)
        default_includes = [] if excluded else cls.PATH_INCLUDES
        return _matches(path, includes, default_includes)

    @classmethod
    def supports_path(cls, path: str, is_dir: bool) -> bool:
        """Check whether this asset class can load the given class."""
        assert isinstance(is_dir, bool)
        return cls._path_matches(path)

    async def load_from(self, source: AssetSource):
        """Copy external data to this asse, replacing existing data."""
        if source == self.location:
            pass
        elif isinstance(source, io.TextIOBase):
            with open(self.location, "w", encoding="utf-8") as target:
                shutil.copyfileobj(source, target)
        elif isinstance(source, io.IOBase):
            with open(self.location, "wb") as target:
                shutil.copyfileobj(source, target)
        else:
            source = Path(source)
            if source.is_dir():
                shutil.copytree(source, self.location)
            else:
                self.location.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, self.location)
        await self.load()

    def __iter__(self):
        """Iterate over assets."""
        return self.iter()

    def __repr__(self):
        """Get a string representation."""
        return f"{self.path} <{self.__class__.__module__}.{self.__class__.__name__}>"


class FileAsset(Asset):
    """A file asset."""

    @property
    def synced(self) -> bool:
        """True when the storage existence is in sync with the content."""
        return self.has_content() == (
            self.location.exists() and not self.location.is_dir()
        )

    async def save(self, **_kwargs):
        """Assert existence of the file."""
        self.assert_synced()
        return self

    async def load(self, **_kwargs):
        """Assert existence of the file."""
        self.assert_synced()
        return self

    def assert_synced(self):
        """Raise an approriate error if not synced."""
        if self.synced:
            return
        err = (
            _err.is_dir
            if self.location.is_dir()
            else _err.not_found
            if self.has_content()
            else _err.exists
        )
        raise err(self.location)

    @classmethod
    def supports_path(cls, path: str, is_dir: bool) -> bool:
        """Check whether this asset class can load the given class."""
        return not is_dir and super().supports_path(path, is_dir=is_dir)


class DirAsset(Asset):
    """A directoy asset."""

    @property
    def synced(self) -> bool:
        """True when the storage existence is in sync with the content."""
        return self.has_content() == self.location.is_dir()

    def assert_synced(self):
        """Raise an approriate error if not synced."""
        if self.synced:
            return
        err = (
            _err.exists
            if not self.has_content()
            else _err.not_dir
            if self.location.exists()
            else _err.not_found
        )
        raise err(self.location)

    def has_content(self):
        """By default, a loaded directory asset should exists."""
        return self.parent is not None

    def is_empty(self):
        """Check that no directory content is present."""
        return not self.location.is_dir() or next(self.location.iterdir(), None) is None

    async def save(self, **_kwargs):
        """Assert create (or remove) the directory."""
        if self.has_content():
            self.location.mkdir(parents=True, exist_ok=True)
        elif self.location.is_dir():
            self.location.rmdir()
        return self

    async def load(self, **_kwargs):
        """Assert existence of the directory."""
        self.assert_synced()
        return self

    @classmethod
    def supports_path(cls, path: str, is_dir: bool = False) -> bool:
        """Check whether this asset class can load the given class."""
        return is_dir and super().supports_path(path, is_dir=is_dir)

    def iter_locations(
        self,
        /,
        relative_to: AssetLocationLike | None = None,
        exclude_empty=False,
        include_dir=False,
        **kwargs,
    ):
        """Iterate the paths for the assets."""
        if include_dir:
            yield from super().iter_locations(
                relative_to=relative_to, exclude_empty=exclude_empty, **kwargs
            )

    def iter(
        self,
        /,
        asset_type: type[A] | None = None,
        path_includes: PathFilter = None,
        path_excludes: PathFilter = None,
        exclude_empty=False,
        include_dir=False,
        **kwargs,
    ) -> Iterator[A]:
        """Iterate the assets."""
        if include_dir:
            yield from super().iter(
                asset_type,
                path_includes=path_includes,
                path_excludes=path_excludes,
                exclude_empty=exclude_empty,
                **kwargs,
            )


AssetType = type[Asset]


class PlainFileAsset(FileAsset):
    """A file asset that has no special handling."""


class PlainDirAsset(DirAsset):
    """A directory asset that has no special handling."""


class AssetsFolder(DirAsset):
    """A container of assets in a separate folder."""

    DEFAULT_ASSET_CLASSES: list[AssetType] = []
    DEFAULT_FILE_ASSET_CLASS = PlainFileAsset
    DEFAULT_DIR_ASSET_CLASS = PlainDirAsset

    children: list[Asset]
    asset_classes: list[AssetType]

    def __init__(
        self,
        parent: "AssetsFolder",
        asset_classes: list[AssetType] | None = None,
        **kwargs,
    ):
        """Create an assets directory."""
        is_dir = kwargs.pop("is_dir", True)
        super().__init__(parent, is_dir=is_dir, **kwargs)
        self.asset_classes = list(asset_classes or self.DEFAULT_ASSET_CLASSES)
        self.children = []

    @property
    def full_path(self) -> str:
        """Full path in an assets archive."""
        return self.parent.full_path + self.path + "/"

    def add(
        self,
        child_class: type[A],
        path: str | None = None,
        is_dir: bool = False,
        **kwargs,
    ) -> A:
        """Add (or get) child asset."""
        child = self.get(asset_type=child_class, path_includes=path, is_dir=is_dir)
        if not child:
            child = child_class(self, path=path, is_dir=is_dir, **kwargs)
            self.children.append(child)
        return child

    async def add_from(
        self,
        child_class: type[A],
        source: AssetSource,
        path: str | None = None,
        **kwargs,
    ) -> A:
        """Add a child asset from an external location."""
        is_dir = False
        if isinstance(source, Path | str):
            source = Path(source)
            is_dir = source.is_dir()
            path = path or source.name
        child_asset = self.add(child_class, path, is_dir=is_dir, **kwargs)
        if isinstance(source, io.TextIOBase):
            child_asset.location.parent.mkdir(parents=True, exist_ok=True)
            with open(child_asset.location, "w+", encoding="utf-8") as f:
                for line in source:
                    f.write(line)
            source = child_asset.location
        elif isinstance(source, io.IOBase):
            child_asset.location.parent.mkdir(parents=True, exist_ok=True)
            with open(child_asset.location, "wb") as f:
                for line in source:
                    f.write(line)
            source = child_asset.location
        if isinstance(child_asset, AssetsFolder):
            await child_asset.add_from_dir(source, recursive=True)
        else:
            await child_asset.load_from(source)
        return child_asset

    def asset_class_for(
        self, path: str, *asset_classes: AssetType, is_dir: bool = False
    ) -> type[Asset] | None:
        """Get the asset class for the given path."""
        for asset_class in list(asset_classes) or self.asset_classes:
            if asset_class.supports_path(path, is_dir=is_dir):
                return asset_class
        return None

    async def save(self, **kwargs) -> Self:
        """Save the current assets when accessed."""
        await super().save(**kwargs)
        for child in self.children:
            await child.save(**kwargs)
        return self

    async def save_archive(self, target: AssetLocationLike | None = None, **_kwargs):
        """Create a compressed tar archive.

        By default as a file in the parent folder."""
        await self.save()
        path = self.location.absolute().name
        target = Path(target or self.location.parent.joinpath(f"{path}.tar.gz"))
        with tarfile.open(target, "w:gz") as tar:
            for child in self.children:
                if child.is_empty():
                    continue
                tar.add(child.location, recursive=True, arcname=child.full_path)
        return target

    async def load(self, *asset_classes: type[Asset], recursive=True, **kwargs) -> Self:
        """Discover child assets from the intended location."""
        self.children = []
        return await self.load_from_dir(
            self.location, *asset_classes, recursive=recursive, **kwargs
        )

    async def load_from(
        self,
        source: AssetSource,
        *asset_classes: AssetType,
        path: str | None = None,
        **kwargs,
    ) -> Self:
        """Load an asset from an external location."""
        is_dir = False
        if isinstance(source, Path):
            is_dir = source.is_dir()
            path = path or source.name
        if isinstance(source, str):
            path = path or Path(source).name
        if path is None:
            raise TypeError(
                "A `path` should be specified when the asset source is a stream."
            )
        _asset_classes = asset_classes or [
            *self.asset_classes,
            self.DEFAULT_DIR_ASSET_CLASS,
            self.DEFAULT_FILE_ASSET_CLASS,
        ]
        asset_class = self.asset_class_for(path, *_asset_classes, is_dir=is_dir)
        if asset_class is None:
            raise TypeError(f"No supported asset class found for {path}")
        asset = await self.add_from(asset_class, source, path, **kwargs)
        await asset.load()
        return self

    async def load_from_dir(
        self,
        from_location: AssetLocation,
        *asset_classes: type["Asset"],
        path_includes: PathFilter = None,
        path_excludes: PathFilter = None,
        recursive=True,
        **kwargs,
    ) -> Self:
        """Discover and load assets from an external location."""
        _asset_classes = asset_classes or self.asset_classes
        await self.add_from_dir(
            from_location,
            *_asset_classes,
            recursive=recursive,
            path_includes=path_includes,
            path_excludes=path_excludes,
            **kwargs,
        )
        for child in self.children:
            await child.load()
        return self

    async def add_from_dir(
        self,
        from_location: AssetLocation,
        *asset_classes: type["Asset"],
        recursive=True,
        path_prefix: str = "",
        path_includes: PathFilter = None,
        path_excludes: PathFilter = None,
        **kwargs,
    ) -> Self:
        """Copy asset(s) (without loading) from an other location."""
        target_location = self.location / path_prefix
        target_location.mkdir(parents=True, exist_ok=True)
        if not from_location.exists():
            raise _err.not_found(from_location)
        if not from_location.is_dir():
            raise _err.not_dir(from_location)
        _asset_classes = asset_classes or self.asset_classes
        for child_location in from_location.iterdir():
            child_path = child_location.relative_to(from_location)
            target_path = f"{path_prefix}{child_path}"
            asset_class = self.asset_class_for(
                target_path,
                *_asset_classes,
                self.DEFAULT_DIR_ASSET_CLASS,
                self.DEFAULT_FILE_ASSET_CLASS,
                is_dir=child_location.is_dir(),
            )
            if asset_class == self.DEFAULT_DIR_ASSET_CLASS and recursive:
                await self.add_from_dir(
                    child_location,
                    *_asset_classes,
                    recursive=recursive,
                    path_prefix=f"{path_prefix}{child_location.name}/",
                    path_includes=path_includes,
                    path_excludes=path_excludes,
                    **kwargs,
                )
                continue
            if asset_class is not None and asset_class._path_matches(
                child_location.name, path_includes, path_excludes
            ):
                await self.add_from(asset_class, child_location, target_path, **kwargs)
        return self

    def is_empty(self):
        """Check that no child asset are present."""
        return all(child.is_empty() for child in self.children)

    def iter_locations(
        self,
        /,
        relative_to: AssetLocationLike | None = None,
        exclude_empty=False,
        include_dir=False,
        recursive=True,
        **kwargs,
    ) -> Iterator[AssetLocation]:
        """List the asset locations."""
        relative_to = relative_to or self.location
        if exclude_empty and self.is_empty():
            return
        yield from super().iter_locations(
            relative_to=relative_to,
            exclude_empty=exclude_empty,
            include_dir=include_dir,
            **kwargs,
        )
        if recursive:
            for child in self.children:
                yield from child.iter_locations(
                    relative_to=relative_to,
                    exclude_empty=exclude_empty,
                    include_dir=include_dir,
                    recursive=recursive,
                    **kwargs,
                )

    def iter(
        self,
        /,
        asset_type: type[A] | None = Asset,
        path_includes: PathFilter = None,
        path_excludes: PathFilter = None,
        exclude_empty=False,
        include_dir=False,
        recursive=True,
        **kwargs,
    ) -> Iterator[A]:
        """List the assets."""
        if exclude_empty and self.is_empty():
            return
        yield from super().iter(
            asset_type=asset_type,
            include_dir=include_dir,
            exclude_empty=exclude_empty,
            path_includes=path_includes,
            path_excludes=path_excludes,
            **kwargs,
        )
        if recursive:
            for child in self.children:
                yield from child.iter(
                    asset_type=asset_type,
                    include_dir=include_dir,
                    exclude_empty=exclude_empty,
                    path_includes=path_includes,
                    path_excludes=path_excludes,
                    recursive=recursive,
                    **kwargs,
                )

    def get(
        self,
        asset_type: type[A],
        path_includes: PathFilter = None,
        path_excludes: PathFilter = None,
        recursive=True,
        **kwargs,
    ) -> A | None:
        """Get the asset of the given type, if it exists."""
        asset_it = self.iter(
            asset_type=asset_type,
            path_includes=path_includes,
            path_excludes=path_excludes,
            recursive=recursive,
            include_dir=True,
            **kwargs,
        )
        asset = next(asset_it, None)
        if asset is None:
            return None
        asset_2 = next(asset_it, None)
        if asset_2 is not None:
            raise IndexError(
                f"Multiple assets of type {asset_type} found: {[asset, asset_2]}"
            )
        return asset

    def get_or_fail(
        self,
        asset_type: type[A],
        path_includes: PathFilter = None,
        path_excludes: PathFilter = None,
        recursive=True,
        **kwargs,
    ) -> A:
        """Get the asset of the given type, fail if it not exists."""
        asset = self.get(asset_type, path_includes, path_excludes, recursive, **kwargs)
        if asset is None:
            raise _err.not_found(path_includes)
        return asset

    def get_or_add(
        self,
        asset_type: type[A],
        path: str | None = None,
        recursive=True,
        **kwargs,
    ) -> A:
        """Get or create the asset of the given type."""
        asset = self.get(asset_type, path_includes=path, recursive=recursive, **kwargs)
        if asset is None:
            asset = self.add(asset_type, path, **kwargs)
        return asset


def _matches(path: str, patterns: str | list[str] | None, default_patterns: list[str]):
    patterns = (
        default_patterns
        if patterns is None
        else [patterns]
        if isinstance(patterns, str)
        else patterns
    )
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)
