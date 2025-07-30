from dataclasses import dataclass
from datetime import datetime
from .Asset import Asset

@dataclass
class Album:
    album_name: str
    album_thumbnail_asset_id: str
    asset_count: int
    assets: list[Asset]
    created_at: datetime
    description: str
    end_date: datetime | None
    has_shared_link: bool
    id: str
    is_activity_enabled: bool
    last_modified_asset_timestamp: str | None
    order: str | None
    owner_id: str
    shared: bool
    start_date: datetime | None
    updated_at: datetime
    