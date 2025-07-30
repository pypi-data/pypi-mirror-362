"""Utilities for the openapi description of the adapter."""

from typing import Any

import openapi_spec_validator
from jsonschema.protocols import Validator
from jsonschema_path import SchemaPath
from openapi_schema_validator import OAS31Validator
from openapi_spec_validator.validation.validators import SpecValidator

from ml_adapter.api.types import AssetLocation

from .json import JsonAsset
from .manifest import FunctionManifestAsset
from .mixin import WithAssets

SchemaSpec = bool | dict
OpenapiSpec = dict


class SchemaAsset(JsonAsset[SchemaSpec]):
    """The assets containing the json spec."""

    PATH_INCLUDES = ["*.schema.json"]
    SCHEMA_VALIDATOR: Validator = OAS31Validator

    @property
    def schema(self) -> SchemaSpec | None:
        """Get and validate the schema spec."""
        if self.json is None:
            return None
        return self.validate_schema(self.json)

    @schema.setter
    def schema(self, schema: SchemaSpec | None | AssetLocation):
        """Validate and set schema definition."""
        if isinstance(schema, AssetLocation):
            schema = SchemaPath.from_file_path(schema).content()
        if schema is not None:
            schema = self.validate_schema(schema)
        self.json = schema

    def validate_schema(self, schema: SchemaSpec):
        """Validate the schema."""
        self.SCHEMA_VALIDATOR.check_schema(schema)
        return schema

    async def save_content(self, **kwargs):
        """Write the validated schema content."""
        self.json = self.validate_schema(self.content)
        return await super().save_content(**kwargs)


class OpenApiAsset(SchemaAsset):
    """Asset for an openapi specification."""

    PATH_INCLUDES = ["*openapi.json"]
    DEFAULT_PATH = "openapi.json"

    OPENAPI_VALIDATOR: SpecValidator = openapi_spec_validator

    def validate_schema(self, schema: dict) -> dict:
        """Validate the schema."""
        schema = self.update_with_manifest(schema)
        self.OPENAPI_VALIDATOR.validate(schema, self.location.as_uri())
        return schema

    def update_with_manifest(self, schema):
        """Update the openapi description with manifest information."""
        manifest_asset = self.parent.get(FunctionManifestAsset)
        if not manifest_asset:
            return schema
        manifest = manifest_asset.json
        if not manifest:
            return schema
        return _update_openapi_with_manifest(schema, manifest)


class WithOpenapi(WithAssets):
    """Mixin for a configuration that has an openapi description.

    Adds methods to a `WithAssets` adapter to manage the
    openapi description of waylay _plugin_ or _webscript_.

    * `openapi` returns an asset of type `OpenApiAsset` (normally at `openapi.json`)

    """

    def __init__(self, **kwargs):
        """Register the openapi asset classes."""
        super().__init__(**kwargs)
        self.assets.asset_classes.extend([OpenApiAsset, SchemaAsset])
        self.assets.add(OpenApiAsset)

    @property
    def openapi(self) -> OpenApiAsset:
        """The openapi asset."""
        return self.assets.get(asset_type=OpenApiAsset)


def _update_openapi_with_manifest(openapi: OpenapiSpec, manifest: dict[str, Any]):
    """Update the openapi description with manifest information."""
    openapi["paths"] = openapi.get("paths", {})
    openapi["info"] = (info := openapi.get("info", {}))
    info["title"] = manifest["name"]
    info["version"] = manifest["version"]
    if "description" not in info:
        manifest_meta = manifest.get("metadata", {})
        manifest_desc = manifest_meta.get("description")
        if manifest_desc:
            info["description"] = manifest_desc
    return openapi
