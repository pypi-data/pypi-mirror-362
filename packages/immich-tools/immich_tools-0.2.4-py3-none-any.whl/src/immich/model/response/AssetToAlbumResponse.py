from dataclasses import dataclass


@dataclass
class AssetToAlbumResponse:
    error: str | None
    id: str | None
    success: bool | None
