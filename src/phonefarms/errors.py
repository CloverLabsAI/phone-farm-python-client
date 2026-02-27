class PhoneFarmError(Exception):
    """Base error for all phone farm API errors."""

    def __init__(self, status: int, detail: str) -> None:
        super().__init__(f"PhoneFarm API error {status}: {detail}")
        self.status = status
        self.detail = detail


class NoPhonesAvailableError(PhoneFarmError):
    def __init__(self, detail: str = "No phones available") -> None:
        super().__init__(409, detail)


class SlotNotFoundError(PhoneFarmError):
    def __init__(self, detail: str = "Slot not found") -> None:
        super().__init__(404, detail)


class DeviceBusyError(PhoneFarmError):
    def __init__(self, detail: str = "Device is busy") -> None:
        super().__init__(409, detail)


class DeviceOfflineError(PhoneFarmError):
    def __init__(self, detail: str = "Device is offline") -> None:
        super().__init__(409, detail)


class TunnelNotAvailableError(PhoneFarmError):
    def __init__(self, detail: str = "Tunnel not available") -> None:
        super().__init__(503, detail)
