from dataclasses import dataclass


@dataclass
class UploadAssetResponse:
    id: str
    status: str
