from dataclasses import dataclass


@dataclass
class AssignTagResponse:
    error: str | None
    id: str
    success: bool
