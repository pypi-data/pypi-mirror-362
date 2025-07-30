"""Utility functions for accessing a function manifest."""

import json
import logging
from pathlib import Path
from typing import Any, Literal, Self, Union

from ml_adapter.base.assets.base import Asset
from ml_adapter.base.assets.mixin import WithAssets

from .base import AssetsFolder
from .json import JsonAsset

LOG = logging.getLogger(__name__)

WEBSCRIPT_MANIFEST_NAME = "webscript.json"
PLUG_MANIFEST_NAME = "plug.json"

ManifestSpec = dict[str, Any]
ManifestMergeSpec = dict[str, Union[str, "ManifestMergeSpec"]]

PLUG_MERGE_SPEC: ManifestMergeSpec = {
    "interface": {
        "states": "REPLACE",
        "input": "OVERWRITE_BY_NAME",
        "output": "OVERWRITE_BY_NAME",
    },
    "metadata": {
        "tags": "OVERWRITE_BY_NAME",
        "documentation": {
            "states": "REPLACE",
            "input": "OVERWRITE_BY_NAME",
            "output": "OVERWRITE_BY_NAME",
        },
    },
}


FunctionType = Literal["webscripts"] | Literal["plugs"]


class FunctionManifestAsset(JsonAsset):
    """An asset that represents a function manifest."""

    PATH_INCLUDES = []
    DEFAULT_MANIFEST: ManifestSpec | None = None
    FUNCTION_TYPE: FunctionType
    MERGE_SPEC: ManifestMergeSpec = {}

    def __init__(
        self, parent: AssetsFolder, manifest: ManifestSpec | None = None, **kwargs
    ):
        """Create the function manifest asset."""
        super().__init__(parent, **kwargs)
        if manifest:
            self.json = manifest
        elif self.DEFAULT_MANIFEST:
            self.json = json.loads(json.dumps(self.DEFAULT_MANIFEST))

    def merge(self, manifest: ManifestSpec) -> ManifestSpec:
        """Merge the existing manifest with new overrides."""
        self.json = merge_manifest(self.content, manifest, self.MERGE_SPEC)
        return self.json


class WebscriptManifestAsset(FunctionManifestAsset):
    """An asset that represents the webscript manifest."""

    FUNCTION_TYPE = "webscripts"
    DEFAULT_PATH = WEBSCRIPT_MANIFEST_NAME
    PATH_INCLUDES = [DEFAULT_PATH]


class PlugManifestAsset(FunctionManifestAsset):
    """An asset that represents the webscript manifest."""

    FUNCTION_TYPE = "plugs"
    DEFAULT_PATH = PLUG_MANIFEST_NAME
    PATH_INCLUDES = [DEFAULT_PATH]
    MERGE_SPEC: ManifestMergeSpec = PLUG_MERGE_SPEC


def _read_json(name: str):
    location = Path(__file__).parent.joinpath(name)
    with open(location, encoding="utf-8") as f:
        return json.load(f)


DEFAULT_PLUG_MANIFEST = _read_json("default.plug.json")
DEFAULT_WEBSCRIPT_MANIFEST = _read_json("default.webscript.json")


class WithManifest(WithAssets):
    """Mixin for a configuration that has a waylay _function_ manifest file.

    Adds methods to manage the function _manifest_ of a waylay _plugin_ or _webscript_.
    * `manifest` returns the manifest asset of the function archive
        at `plug.json` or `webscript.json`.
    """

    MANIFEST_ASSET_CLASSES: list[type[FunctionManifestAsset]] = [
        WebscriptManifestAsset,
        PlugManifestAsset,
    ]
    DEFAULT_MANIFEST_CLASS: type[FunctionManifestAsset] = WebscriptManifestAsset
    DEFAULT_RUNTIME: dict[FunctionType, str] = {}
    DEFAULT_MANIFEST: dict[FunctionType, ManifestSpec] = {
        "webscripts": DEFAULT_WEBSCRIPT_MANIFEST,
        "plugs": DEFAULT_PLUG_MANIFEST,
    }
    MAIN_SCRIPT_PATHS = []

    def __init__(
        self,
        manifest_path: str | None = None,
        manifest: ManifestSpec | None = None,
        function_type: FunctionType | None = None,
        **kwargs,
    ):
        """Register the manifest asset classes."""
        super().__init__(**kwargs)
        asset_classes = self.MANIFEST_ASSET_CLASSES
        asset_class = self.DEFAULT_MANIFEST_CLASS
        if function_type == "webscripts":
            asset_class = WebscriptManifestAsset
        if function_type == "plugs":
            asset_class = PlugManifestAsset
        self.assets.asset_classes.extend(asset_classes)
        if manifest_path:
            asset_class = self.assets.asset_class_for(manifest_path, is_dir=False)
            if asset_class is None:
                raise TypeError(
                    f"path {manifest_path} is not a supported path "
                    f"for any of the supported {asset_classes}"
                )
        self.assets.add(asset_class, manifest_path, manifest=manifest, **kwargs)

    @property
    def manifest(self) -> FunctionManifestAsset:
        """The manifest of the function that uses this adapter."""
        manifest: FunctionManifestAsset | None = None
        for asset in self.assets.iter(asset_type=FunctionManifestAsset):
            if asset.has_content():
                if manifest and manifest.has_content():
                    raise IndexError(
                        f"Multiple non empty manifest assets found:"
                        f" {[asset.path, manifest.path]}"
                    )
                manifest = asset
            manifest = manifest or asset
        if manifest is None:
            return self.assets.get_or_add(self.DEFAULT_MANIFEST_CLASS)
        return manifest

    async def load(self, *asset_classes: type[Asset], **kwargs) -> Self:
        """Load and assure manifest is present."""
        loaded = await super().load(*asset_classes, **kwargs)
        # initialize manifest if needed
        if not next(self.assets.iter(asset_type=FunctionManifestAsset), False):
            self.assets.get_or_add(self.DEFAULT_MANIFEST_CLASS)
        return loaded

    def as_webscript(self, /, *spec: ManifestSpec, **manifest_args) -> Self:
        """Make sure a webscript manifest is present."""
        manifest = {}
        for s in spec:
            manifest.update(s)
        manifest.update(manifest_args)
        return self._as_function(manifest, "webscripts")

    def as_plug(self, /, *spec: ManifestSpec, **manifest_args) -> Self:
        """Make sure that a plug manifest is present."""
        manifest = {}
        for s in spec:
            manifest.update(s)
        manifest.update(manifest_args)
        return self._as_function(manifest, "plugs")

    def default_runtime(self, function_type: FunctionType = "plugs") -> str:
        """Get the default runtime for this archive."""
        return self.DEFAULT_RUNTIME[function_type]

    def default_manifest(self, function_type: FunctionType = "plugs") -> ManifestSpec:
        """Get a default manifest for this archive."""
        return {
            **self.DEFAULT_MANIFEST[function_type],
            "runtime": self.default_runtime(function_type),
        }

    def _as_function(self, manifest: ManifestSpec, function_type: FunctionType) -> Self:
        # switch function type if neccessary
        manifest_asset = self._assure_manifest_type(function_type)
        manifest_asset.merge(manifest)
        return self

    def _assure_manifest_type(self, function_type: FunctionType):
        manifest_type = (
            WebscriptManifestAsset
            if function_type == "webscripts"
            else PlugManifestAsset
        )
        manifest_asset = None
        assets_to_remove: list[FunctionManifestAsset] = []
        for asset in self.assets.iter(asset_type=FunctionManifestAsset):
            if isinstance(asset, manifest_type):
                manifest_asset = asset
            else:
                assets_to_remove.append(asset)
        if manifest_asset is None:
            manifest_asset = self.assets.get_or_add(
                manifest_type, manifest_type.DEFAULT_PATH
            )
        for rem_asset in assets_to_remove:
            LOG.warning(
                "Wrong manifest %s for %s. Resetting main script and manifest.",
                rem_asset.path,
                function_type,
            )
            rem_asset.content = None
            rem_asset.location.unlink(missing_ok=True)
            self.assets.children.remove(rem_asset)
        if not manifest_asset.has_content():
            LOG.warning(
                "No manifest initialized, generating a default %s manifest",
                function_type,
            )
            manifest_asset.merge(self.default_manifest(function_type))
        return manifest_asset


def merge_manifest(
    default: ManifestSpec | None, overrides: ManifestSpec, paths: ManifestMergeSpec
) -> ManifestSpec:
    """Merge a default and override manifest, with deep merge at the indicated paths."""
    if default is None:
        return overrides
    merged = {**default, **overrides}
    for key, paths_at_key in paths.items():
        if key in overrides and key in default:
            if isinstance(paths_at_key, dict):
                merged[key] = merge_manifest(default[key], overrides[key], paths_at_key)
            if paths_at_key == "UNION":
                merged[key] = list(set(default[key]).union(overrides[key]))
            if paths_at_key == "OVERWRITE_BY_NAME":
                merged[key] = list(
                    merge_manifest(
                        {val["name"]: val for val in default[key]},
                        {val["name"]: val for val in overrides[key]},
                        {},
                    ).values()
                )
    return merged
