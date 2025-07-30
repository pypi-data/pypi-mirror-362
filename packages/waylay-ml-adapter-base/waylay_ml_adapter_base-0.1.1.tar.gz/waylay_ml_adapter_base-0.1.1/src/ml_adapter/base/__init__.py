"""ML Adapter base infrastructure."""

import importlib.metadata

from .adapter import ModelAdapter, ModelAdapterBase, TensorModelAdapter
from .assets import (
    NodeFunctionAdapter,
    PythonFunctionAdapter,
    PythonMLAdapter,
    WithAssets,
    WithManifest,
    WithOpenapi,
)
from .marshall import Marshaller
from .model import (
    DillModelAsset,
    JoblibModelAsset,
    SelfSerializingModelAsset,
    WithModel,
)

__version__ = importlib.metadata.version("waylay-ml-adapter-base")

__all__ = [
    "PythonMLAdapter",
    "PythonFunctionAdapter",
    "NodeFunctionAdapter",
    "WithManifest",
    "ModelAdapter",
    "TensorModelAdapter",
    "ModelAdapterBase",
    "WithAssets",
    "WithOpenapi",
    "WithModel",
    "SelfSerializingModelAsset",
    "DillModelAsset",
    "JoblibModelAsset",
    "Marshaller",
]
