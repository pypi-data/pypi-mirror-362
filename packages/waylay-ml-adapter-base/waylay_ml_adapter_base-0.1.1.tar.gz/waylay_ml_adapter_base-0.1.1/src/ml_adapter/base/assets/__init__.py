"""Asset utilities."""

from ml_adapter.api.types import AssetLocation, AssetSource, as_location

from .base import Asset, AssetsFolder, DirAsset, FileAsset
from .cached import CachedFileAsset, RequiredCachedFileAsset
from .json import JsonAsset
from .manifest import (
    FunctionType,
    PlugManifestAsset,
    WebscriptManifestAsset,
    WithManifest,
)
from .mixin import WithAssets
from .node import NodeFunctionAdapter
from .openapi import OpenApiAsset, SchemaAsset, WithOpenapi
from .python import PythonFunctionAdapter
from .python_ml import PythonMLAdapter
from .root import AssetsRoot

__all__ = [
    "AssetLocation",
    "AssetSource",
    "as_location",
    "FileAsset",
    "Asset",
    "DirAsset",
    "AssetsFolder",
    "WithAssets",
    "AssetsRoot",
    "JsonAsset",
    "RequiredCachedFileAsset",
    "CachedFileAsset",
    "WithManifest",
    "WebscriptManifestAsset",
    "PlugManifestAsset",
    "WithOpenapi",
    "SchemaAsset",
    "OpenApiAsset",
    "NodeFunctionAdapter",
    "PythonFunctionAdapter",
    "PythonMLAdapter",
    "FunctionType",
]
