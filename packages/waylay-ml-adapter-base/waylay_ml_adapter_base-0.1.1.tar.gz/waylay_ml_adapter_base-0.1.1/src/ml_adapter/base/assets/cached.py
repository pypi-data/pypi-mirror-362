"""Assets that have a local edit cache."""

import abc
from typing import Generic, TypeVar

from . import _err
from .base import FileAsset

C = TypeVar("C")


class CachedFileAsset(FileAsset, abc.ABC, Generic[C]):
    """Accessor to a file with local caching."""

    content: C | None = None

    def has_content(self) -> bool:
        """Check that cached content is not empty."""
        return self.content is not None

    def get_or_fail(self) -> C:
        """Get the content or fail if not set."""
        if self.content is None:
            raise ValueError(f"No content set or loaded from {self.path}")
        return self.content

    @abc.abstractmethod
    async def load_content(self, **kwargs):
        """Cache the content."""

    def load_empty(self):
        """Clear the (cached) content."""
        self.content = None

    @abc.abstractmethod
    async def save_content(self, **kwargs):
        """Write the cached content."""

    async def save_empty(self):
        """Remove the content from storage."""
        self.location.unlink()

    async def load(self, **kwargs):
        """Load a json file asset."""
        if self.location.exists():
            await self.load_content(**kwargs)
        else:
            self.load_empty()
        return self

    async def save(self, **kwargs):
        """Save a json file asset."""
        if self.has_content():
            await self.save_content(**kwargs)
        elif self.location.exists():
            await self.save_empty()
        return self


class RequiredCachedFileAsset(CachedFileAsset[C], Generic[C]):
    """A required cached asset."""

    def load_empty(self):
        """Cannot load a with empty asset."""
        raise _err.not_found(self.location)
