from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
  avatar_color: str
  created_at: datetime
  deleted_at: datetime | None
  email: str
  id: str
  is_admin: bool
  name: str
  oauth_id: str
  profile_changed_at: str
  profile_image_path: str
  quota_size_in_bytes: int | None
  quota_usage_in_bytes: int
  should_change_password: bool
  status: str
  storage_label: str
  updated_at: datetime
  