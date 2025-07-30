"""Base python adapter with initialization for ML runtimes."""

import json
import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any, Literal, Self, Union

from .python import PythonFunctionAdapter, PythonRequirementsAsset, PythonScriptAsset
from .script import default_plug_v1_script, default_webscript_script

LOG = logging.getLogger(__name__)

WEBSCRIPT_MANIFEST_NAME = "webscript.json"
PLUG_MANIFEST_NAME = "plug.json"

ManifestSpec = dict[str, Any]
ManifestMergeSpec = dict[str, Union[str, "ManifestMergeSpec"]]
FunctionType = Literal["webscripts"] | Literal["plugs"]

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


def _read_json(name: str):
    location = Path(__file__).parent.joinpath(name)
    with open(location, encoding="utf-8") as f:
        return json.load(f)


DEFAULT_PLUG_MANIFEST_V1 = _read_json("default.v1.plug.json")
DEFAULT_PLUG_MANIFEST_V2 = _read_json("default.v2.plug.json")
DEFAULT_WEBSCRIPT_MANIFEST_V1 = _read_json("default.v1.webscript.json")


class PythonMLAdapter(PythonFunctionAdapter):
    """Base adapter for a python ML function.

    Adds methods to intialize the _manifest_ and _script_
    for a python  _plugin_ or _webscript_.

    * `as_webscript()` initializes the manifest
        and script for a _webscript_ that uses an ML Adapter.
    * `as_plug()` initializes the manifest and script for
        a rule _plugin_ that uses an ML Adapter.
    """

    DEFAULT_REQUIREMENTS = ["starlette"]
    DEFAULT_SCRIPT: dict[FunctionType, Callable] = {
        "webscripts": default_webscript_script,
        "plugs": default_plug_v1_script,
    }
    DEFAULT_MANIFEST: dict[FunctionType, ManifestSpec] = {
        "webscripts": DEFAULT_WEBSCRIPT_MANIFEST_V1,
        "plugs": DEFAULT_PLUG_MANIFEST_V1,
    }

    def default_script(self, function_type: FunctionType = "plugs") -> Callable:
        """Get a default main script for a webscript."""
        return self.DEFAULT_SCRIPT[function_type]

    def default_requirements(self) -> list[str]:
        """Get the default requirements for this archive."""
        return self.DEFAULT_REQUIREMENTS

    def _as_function(self, manifest: ManifestSpec, function_type: FunctionType) -> Self:
        super()._as_function(manifest, function_type=function_type)
        self._assure_script(function_type)
        self._assure_requirements()
        return self

    def _assure_script(self, function_type: FunctionType) -> Self:
        """Verify or initialize main script."""
        script_asset = self.assets.get_or_add(PythonScriptAsset, self.MAIN_SCRIPT_NAME)
        if not script_asset.has_content():
            LOG.warning(
                "No %s provided, generating a default %sscript",
                self.MAIN_SCRIPT_NAME,
                function_type,
            )
            model_path = None
            model_class = None
            from ..model import WithModel

            if isinstance(self, WithModel):
                model_path = self.model_path
                model_class = self.model_class
            script_asset.content = self.default_script(function_type)(
                self.__class__,
                model_path=model_path,
                model_class=model_class,
            )
        return self

    def _assure_requirements(self) -> Self:
        """Verify or initialize python requirements."""
        requirements_asset = self.assets.get_or_add(PythonRequirementsAsset)
        requirements_asset.add_default(*self.default_requirements())
        return self
