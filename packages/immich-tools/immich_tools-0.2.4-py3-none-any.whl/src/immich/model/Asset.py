from dataclasses import dataclass
from datetime import datetime

from src.immich.model.Tag import Tag

@dataclass
class Asset:
    checksum: str
    device_asset_id: str
    device_id: str
    duplicate_id: str | None
    duration: str
    file_created_at: datetime
    file_modified_at: datetime
    has_metadata: bool
    id: str
    is_archived: bool
    is_favorite: bool
    is_offline: bool
    is_trashed: bool
    live_photo_video_id: str | None
    local_date_time: datetime
    original_file_name: str
    original_mime_type: str | None
    original_path: str
    owner_id: str
    thumbhash: str | None
    type: str
    updated_at: str
    visibility: str
    tags: list[Tag] | None