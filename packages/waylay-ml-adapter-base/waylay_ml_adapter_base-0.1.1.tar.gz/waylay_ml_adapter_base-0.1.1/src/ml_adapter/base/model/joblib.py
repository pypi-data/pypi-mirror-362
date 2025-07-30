"""Serialization of models using joblib."""

from functools import cache
from typing import Generic

import ml_adapter.api.types as T

from .base import ModelAsset


@cache
def joblib():
    """Load and cache the joblib module."""
    import joblib as joblib_loaded  # pylint:disable=import-outside-toplevel

    return joblib_loaded


class JoblibModelAsset(ModelAsset[T.MI], Generic[T.MI]):
    """Model asset with joblib serialization.

    Reads/writes the model from `model.joblib` or `model.joblib.gz`
    using [joblib](https://pypi.org/project/joblib/) serialisation.
    """

    PATH_INCLUDES = ["*.joblib", "*.joblib.gz"]
    DEFAULT_PATH = "model.joblib"

    joblib_serialization_defaults = {"compress": ("gzip", 3)}

    async def load_content(self, **kwargs):
        """Load joblib a model."""
        with open(self.location, "rb") as f:
            self.content = joblib().load(f, **kwargs)  # type: ignore

    async def save_content(self, **kwargs):
        """Save a joblib model."""
        with open(self.location, "wb") as f:
            defaulted_kwargs = {**self.joblib_serialization_defaults, **kwargs}
            joblib().dump(self.content, f, **defaulted_kwargs)  # type: ignore
