"""Cached json asset."""

import json
from typing import Generic, cast

from .cached import C, CachedFileAsset


class JsonAsset(CachedFileAsset[C], Generic[C]):
    """An asset that loads json content."""

    JSON_INDENT = 2
    PATH_INCLUDES: list[str] = ["*.json"]

    @property
    def json(self) -> C:
        """The cached json-serializable content."""
        # None can be valid (`null` as json)
        return cast(C, self.content)

    @json.setter
    def json(self, content: C):
        """Set the cache json-serializable content."""
        self.content = content

    async def load_content(self, **kwargs):
        """Read the json content."""
        with open(self.location, encoding="utf-8") as f:
            self.content = json.load(f)

    async def save_content(self, **kwargs):
        """Write the jsoncontent."""
        with open(self.location, "w", encoding="utf-8") as f:
            json.dump(self.content, f, indent=self.JSON_INDENT)
