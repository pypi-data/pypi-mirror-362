"""Asset folder and root asset folder."""

from ml_adapter.api.types import AssetLocation, AssetLocationLike, as_location

from .base import AssetsFolder


class AssetsRoot(AssetsFolder):
    """Root of the assets storage."""

    _location: AssetLocation

    @property
    def location(self) -> AssetLocation:
        """Path of asset(s)."""
        return self._location

    @property
    def full_path(self) -> str:
        """Full path in an assets archive."""
        return ""

    def __init__(self, location: AssetLocationLike = ".", **kwargs):
        """Create an assets root."""
        super().__init__(parent=self, path=".", **kwargs)
        location = as_location(location)
        if location.exists() and not location.is_dir():
            location = location.parent
        self._location = location
