"""Serialization of models using dill."""

from functools import cache
from typing import Generic

import ml_adapter.api.types as T

from .base import ModelAsset


@cache
def dill():
    """Load and cache the dill module."""
    import dill as dill_loaded  # pylint:disable=import-outside-toplevel

    return dill_loaded


class DillModelAsset(ModelAsset[T.MI], Generic[T.MI]):
    """Model asset for dill-serialized models.

    Reads/writes the model from paths like `model.dill`, `model.pkl`, `model.pickle`
    using [dill](https://pypi.org/project/dill/) serialisation.
    """

    PATH_INCLUDES = ["*.dill", "*.pkl", "*.pickle"]
    DEFAULT_PATH = "model.dill"

    async def load_content(self, **kwargs):
        """Load a dill model."""
        with open(self.location, "rb") as f:
            self.content = dill().load(f, **kwargs)  # type: ignore

    async def save_content(self, **kwargs):
        """Save a dill model."""
        with open(self.location, "wb") as f:
            dill().dump(self.content, f, **kwargs)  # type: ignore
