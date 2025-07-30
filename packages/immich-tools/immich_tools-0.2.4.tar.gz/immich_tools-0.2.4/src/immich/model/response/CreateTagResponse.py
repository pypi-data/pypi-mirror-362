from dataclasses import dataclass
from datetime import datetime

@dataclass
class CreateTagResponse:
  color: str | None
  created_at: datetime | None
  id: str
  name: str
  parent_id: str | None
  updated_at: datetime
  value: str