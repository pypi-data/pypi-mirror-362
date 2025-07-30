"""ML Adapter mixing providing access to assets."""

from collections.abc import Iterable
from glob import iglob
from pathlib import Path
from typing import Self

from ml_adapter.api.types import (
    AssetLocation,
    AssetLocationLike,
    AssetSource,
    as_location,
)

from .base import Asset
from .root import AssetsRoot


class WithAssets:
    """Mixin for a configuration backed by assets.

    Manages _assets_ of the the _plugin_ or _webscript_.

    Used read-only within a deployed _adapter_ to e.g. load the model definition.

    Used read/write within the `ml_tool` to edit
    the assets of a _plugin_ or _webscript_.
    """

    assets: AssetsRoot

    def __init__(self, location: AssetLocationLike | None = None, **kwargs):
        """Create assets support."""
        self.assets = AssetsRoot(location=as_location(location), **kwargs)

    async def save(self, **kwargs) -> Self:
        """Save the current assets when accessed."""
        await self.assets.save(**kwargs)
        return self

    async def load(self, *asset_classes: type["Asset"], **kwargs) -> Self:
        """Load all assets."""
        await self.assets.load(*asset_classes, **kwargs)
        return self

    async def save_archive(
        self, target: AssetLocationLike | None = None, **kwargs
    ) -> AssetLocation:
        """Save the archive."""
        return await self.assets.save_archive(target, **kwargs)

    async def add_asset(self, source: AssetSource, path: str | None = None) -> Asset:
        """Add a generic file asset to a function archive.

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
        return await self.assets.load_from(source, path=path)

    async def add_assets(
        self,
        *sources: AssetLocationLike,
        relative_to: AssetLocationLike | None = ".",
        path: str | None = None,
    ) -> Iterable[Asset]:
        """Add multiple file assets to the function archive.

        Parameters
        ----------
        *sources : AssetLocationLike
            A variable number of locations for the asset sources.
            When a string, the location can be a glob pattern containing
            `**`, `*` and `?` wildcards.
        relative_to: str | None
            The (common) root path for the sources.

            If not `None` (or defaulted as `.`, the current working directory):
            - glob patterns in the `sources` are expanded at that location.
            - the directory structure is preserved in the target.

            If `None`:
            - the source directory structure is flattened, using the _basename_ as path.
            - glob patterns are expanded at the current working directory.
        path: str | None
            The target directory path with the archive.
            If not given, the assets are added to the root location.

        """
        all_sources: list[Path] = []
        for src in sources:
            if not isinstance(src, str):
                all_sources.append(src)
                continue
            for gsrc in iglob(src, root_dir=relative_to, recursive=True):
                src_path = Path(relative_to or ".") / gsrc
                if not src_path.is_dir():
                    all_sources.append(src_path)
        assets = []
        for src in all_sources:
            rel_src = (
                src.name if relative_to is None else str(src.relative_to(relative_to))
            )
            src_path = rel_src if path is None else f"{path}/{rel_src}"
            assets.append(await self.assets.load_from(src, path=src_path))
        return assets

    @property
    def location(self) -> AssetLocation:
        """Return the location of the stored assets."""
        return self.assets.location
