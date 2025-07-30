from dataclasses import dataclass
from datetime import datetime

@dataclass
class Tag:
    color: str | None
    created_at: datetime
    id: str
    parent_id: str | None
    updated_at: datetime
    value: str