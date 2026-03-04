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
from .types import ReleaseSessionResponse, SlotInfo

__version__ = "0.1.0"

__all__ = [
    "PhoneFarmClient",
    "PhoneFarmError",
    "NoPhonesAvailableError",
    "SlotNotFoundError",
    "DeviceBusyError",
    "DeviceOfflineError",
    "TunnelNotAvailableError",
    "ReleaseSessionResponse",
    "SlotInfo",
    "__version__",
]
