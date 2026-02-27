from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ReleaseSessionResponse:
    slot_id: str
    session_id: str | None
    status: str
