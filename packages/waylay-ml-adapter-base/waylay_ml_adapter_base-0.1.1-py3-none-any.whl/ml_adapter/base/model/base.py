"""Model asset holder."""

from typing import Generic

import ml_adapter.api.types as T

from ..assets import RequiredCachedFileAsset, _err


class ModelAsset(RequiredCachedFileAsset[T.MI], Generic[T.MI]):
    """Asset for the ml model storage."""

    PATH_INCLUDES = ["model.*"]
    PATH_SUFFIXES = []

    @property
    def model(self) -> T.MI:
        """The model instance."""
        if self.content is None:
            raise _err.not_found(location=self.location)
        return self.content

    @model.setter
    def model(self, content: T.MI):
        """Set the model instance."""
        self.content = content
