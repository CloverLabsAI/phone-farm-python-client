from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ShellResult:
    """Result of running a shell command on a device."""

    exit_code: int
    stdout: str
    stderr: str


@dataclass
class ReleaseSessionResponse:
    slot_id: str
    session_id: str | None
    status: str


@dataclass
class SetupDefinition:
    """A setup template defining which apps to install on a device."""

    id: str
    name: str
    apps_installed: list[str]
    apk_urls: dict[str, str]
    setup_commands: list[str]


@dataclass
class PreparationDefinition:
    """A versioned set of one-time device preparation steps."""

    id: int
    pre_install_commands: list[str]
    apps_installed: list[str]
    post_install_commands: list[str]


@dataclass
class SlotInfo:
    slot_id: str
    device_serial: str
    device_name: str
    status: str  # "available" | "busy" | "offline"
    setup_name: str
    cluster_id: str
    cluster_name: str | None = None
    owner: str = ""
    has_active_session: bool = False
    tunnel_url: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
