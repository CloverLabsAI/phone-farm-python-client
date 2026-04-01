"""Echos Automation phone farm Python SDK."""

from .client import PhoneFarmClient
from .errors import (
    DeviceBusyError,
    DeviceOfflineError,
    NoPhonesAvailableError,
    PhoneFarmError,
    SlotNotFoundError,
    TunnelNotAvailableError,
)
from .types import (
    PreparationDefinition,
    ReleaseSessionResponse,
    SetupDefinition,
    SlotInfo,
)

__version__ = "0.1.0"

__all__ = [
    "DeviceBusyError",
    "DeviceOfflineError",
    "NoPhonesAvailableError",
    "PhoneFarmClient",
    "PhoneFarmError",
    "PreparationDefinition",
    "ReleaseSessionResponse",
    "SetupDefinition",
    "SlotInfo",
    "SlotNotFoundError",
    "TunnelNotAvailableError",
    "__version__",
]
