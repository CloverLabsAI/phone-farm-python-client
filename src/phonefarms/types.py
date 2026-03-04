from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ReleaseSessionResponse:
    slot_id: str
    session_id: str | None
    status: str


@dataclass
class SlotInfo:
    slot_id: str
    device_serial: str
    device_name: str
    status: str  # "available" | "busy" | "offline"
    cluster_id: str
    cluster_name: str | None = None
    owner: str = ""
    has_active_session: bool = False
    tunnel_url: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
