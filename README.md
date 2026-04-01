# phonefarms

Python SDK for the Echos Automation phone farm API. Single runtime dependency: `httpx`.

## Install

**With uv (recommended):**

```bash
uv add phonefarms --index-url https://cloverlabsai.github.io/phone-farm-python-client/simple/
```

**With pip:**

```bash
pip install phonefarms --index-url https://cloverlabsai.github.io/phone-farm-python-client/simple/
```

**From source:**

```bash
pip install git+https://github.com/CloverLabsAI/phone-farm-python-client.git
```

## Quick Start

```python
from phonefarms import PhoneFarmClient

with PhoneFarmClient("https://farm.echos.social", "your-api-key") as client:
    # 1. Create a slot (auto-assigns an available device)
    slot_id = client.create_slot()

    # 2. Start a session (locks the device, returns tunnel URL)
    tunnel_url = client.create_session(slot_id)

    # 3. Use the device via tunnel_url ...

    # 4. Release the session when done (unlocks the device)
    client.release_session(slot_id)

    # 5. Delete the slot when no longer needed
    client.delete_slot(slot_id)
```

## API

### `PhoneFarmClient(base_url, api_key)`

| Parameter  | Type  | Description                |
| ---------- | ----- | -------------------------- |
| `base_url` | `str` | Farm server URL            |
| `api_key`  | `str` | API key for authentication |

Supports use as a context manager (`with` statement) for automatic cleanup.

### `client.create_slot(*, cluster_id?, owner?) -> str`

Auto-assigns an available online device and creates a persistent slot. Returns the slot ID.

| Parameter    | Type          | Description                                  |
| ------------ | ------------- | -------------------------------------------- |
| `cluster_id` | `str \| None` | Optional. Restrict to a specific cluster     |
| `owner`      | `str \| None` | Optional. Slot owner label (default: `"api"`) |

**Raises:** `NoPhonesAvailableError` if no online devices have capacity.

### `client.delete_slot(slot_id) -> None`

Deletes a slot. Automatically releases any active session on it first.

**Raises:** `SlotNotFoundError` if the slot does not exist.

### `client.create_session(slot_id) -> str`

Starts an active session for a slot, locking the assigned device. Returns the tunnel URL for device access. Only one active session is allowed per device at a time.

**Raises:**
- `SlotNotFoundError` — slot does not exist
- `DeviceOfflineError` — assigned device is offline
- `DeviceBusyError` — device already has an active session
- `TunnelNotAvailableError` — device has no tunnel URL configured

### `client.release_session(slot_id) -> ReleaseSessionResponse`

Releases the active session for a slot, unlocking the device. Idempotent — returns successfully even if no active session exists.

**Returns:** `ReleaseSessionResponse` with fields:

```python
ReleaseSessionResponse(
    slot_id="...",
    session_id="..." or None,
    status="released",
)
```

### `client.close() -> None`

Close the underlying HTTP client. Called automatically when using a `with` block.

## Error Handling

All errors extend `PhoneFarmError`, which exposes `status` and `detail` attributes:

```python
from phonefarms import (
    NoPhonesAvailableError,
    SlotNotFoundError,
    DeviceBusyError,
    DeviceOfflineError,
    TunnelNotAvailableError,
)

try:
    url = client.create_session(slot_id)
except DeviceBusyError:
    # retry later
    pass
except DeviceOfflineError:
    # device went offline
    pass
```

| Error class                | HTTP Status | When                                    |
| -------------------------- | ----------- | --------------------------------------- |
| `NoPhonesAvailableError`   | 409         | No online devices with available slots  |
| `SlotNotFoundError`        | 404         | Slot ID does not exist                  |
| `DeviceBusyError`          | 409         | Device already has an active session    |
| `DeviceOfflineError`       | 409         | Assigned device is offline              |
| `TunnelNotAvailableError`  | 503         | Device has no tunnel URL                |
| `PhoneFarmError`           | any         | Base class for all other API errors     |
