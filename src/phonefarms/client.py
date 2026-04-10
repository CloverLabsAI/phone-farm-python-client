from __future__ import annotations

import contextlib
import json
import socket
import threading
from http import HTTPStatus
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import quote

import websockets.sync.client

from ._generated.api.slots import (
    create_session as gen_create_session,
)
from ._generated.api.slots import (
    create_slot as gen_create_slot,
)
from ._generated.api.slots import (
    delete_slot as gen_delete_slot,
)
from ._generated.api.slots import (
    get_slot as gen_get_slot,
)
from ._generated.api.slots import (
    list_slots as gen_list_slots,
)
from ._generated.api.slots import (
    release_session as gen_release_session,
)
from ._generated.client import Client as GenClient
from ._generated.models.create_slot_body import CreateSlotBody
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
    ShellResult,
    SlotInfo,
)

if TYPE_CHECKING:
    from ._generated.types import Response as GenResponse


class _AdbBridge:
    """Local TCP server that bridges ADB connections to a WebSocket relay."""

    def __init__(self, ws_url: str) -> None:
        self._ws_url = ws_url
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind(("127.0.0.1", 0))
        self._server_socket.listen(1)
        self.port = self._server_socket.getsockname()[1]
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self) -> None:
        self._server_socket.settimeout(1.0)
        while not self._stop.is_set():
            try:
                client_sock, _ = self._server_socket.accept()
            except TimeoutError:
                continue
            except OSError:
                break
            threading.Thread(
                target=self._handle_client, args=(client_sock,), daemon=True
            ).start()

    def _handle_client(self, client_sock: socket.socket) -> None:
        try:
            ws = websockets.sync.client.connect(self._ws_url, max_size=None)
        except Exception:
            client_sock.close()
            return

        stop = threading.Event()

        def tcp_to_ws() -> None:
            try:
                while not stop.is_set():
                    data = client_sock.recv(65536)
                    if not data:
                        break
                    ws.send(data)
            except Exception:
                pass
            finally:
                stop.set()

        def ws_to_tcp() -> None:
            try:
                for message in ws:
                    if stop.is_set():
                        break
                    if isinstance(message, bytes):
                        client_sock.sendall(message)
            except Exception:
                pass
            finally:
                stop.set()

        t1 = threading.Thread(target=tcp_to_ws, daemon=True)
        t2 = threading.Thread(target=ws_to_tcp, daemon=True)
        t1.start()
        t2.start()
        stop.wait()
        t1.join(timeout=2)
        t2.join(timeout=2)
        with contextlib.suppress(Exception):
            ws.close()
        with contextlib.suppress(Exception):
            client_sock.close()

    def close(self) -> None:
        self._stop.set()
        self._server_socket.close()
        self._thread.join(timeout=2)


class PhoneFarmClient:
    """Synchronous client for the Echos Automation phone farm API."""

    def __init__(self, base_url: str, api_key: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._client = GenClient(
            base_url=self._base_url,
            headers={
                "X-API-Key": api_key,
                "Content-Type": "application/json",
            },
        )
        self._bridges: dict[str, _AdbBridge] = {}  # slot_id -> bridge

    # -- context manager --------------------------------------------------

    def __enter__(self) -> PhoneFarmClient:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP client and all active bridges."""
        for bridge in self._bridges.values():
            bridge.close()
        self._bridges.clear()
        httpx_client = self._client.get_httpx_client()
        httpx_client.close()

    # -- public API --------------------------------------------------------

    def create_slot(
        self,
        setup: str,
        *,
        cluster_id: str | None = None,
        owner: str | None = None,
    ) -> str:
        """Create a persistent slot (auto-assigns a device). Returns the slot ID."""
        body = CreateSlotBody(setup=setup, cluster_id=cluster_id, owner=owner)
        result = gen_create_slot.sync_detailed(client=self._client, body=body)
        self._check_error(result)
        return result.parsed.slot_id  # type: ignore[union-attr]

    def delete_slot(self, slot_id: str) -> None:
        """Delete a slot and release any active session."""
        self._close_bridge(slot_id)
        result = gen_delete_slot.sync_detailed(slot_id, client=self._client)
        self._check_error(result)

    def create_session(self, slot_id: str) -> str:
        """Start an active session for a slot.

        Creates the session, starts a local TCP↔WebSocket bridge for ADB access,
        and returns a localhost:port address usable with ``adb -s``.
        """
        result = gen_create_session.sync_detailed(slot_id, client=self._client)
        self._check_error(result)
        parsed = result.parsed  # type: ignore[union-attr]
        phone_id = parsed.phone_id  # type: ignore[union-attr]

        # Build WS URL for the ADB relay
        ws_base = self._base_url.replace("http://", "ws://").replace(
            "https://", "wss://"
        )
        ws_url = (
            f"{ws_base}/api/v1/phones/{phone_id}/adb/ws"
            f"?api_key={quote(self._api_key, safe='')}"
        )

        # Start local TCP bridge
        bridge = _AdbBridge(ws_url)
        self._bridges[slot_id] = bridge

        return f"localhost:{bridge.port}"

    def release_session(self, slot_id: str) -> ReleaseSessionResponse:
        """Release the active session for a slot (idempotent)."""
        self._close_bridge(slot_id)
        result = gen_release_session.sync_detailed(slot_id, client=self._client)
        self._check_error(result)
        parsed = result.parsed  # type: ignore[union-attr]
        return ReleaseSessionResponse(
            slot_id=parsed.slot_id,  # type: ignore[union-attr]
            session_id=parsed.session_id,  # type: ignore[union-attr]
            status=parsed.status,  # type: ignore[union-attr]
        )

    # -- device control (HTTP) ---------------------------------------------

    def shell(self, phone_id: str, command: str, timeout: int = 30) -> ShellResult:
        """Run a shell command on a device. Uses the HTTP API (no ADB needed)."""
        httpx_client = self._client.get_httpx_client()
        response = httpx_client.post(
            f"/api/v1/phones/{phone_id}/shell",
            json={"command": command, "timeout": timeout},
            timeout=timeout + 10,
        )
        response.raise_for_status()
        data = response.json()
        return ShellResult(
            exit_code=data["exit_code"],
            stdout=data["stdout"],
            stderr=data["stderr"],
        )

    def open_app(self, phone_id: str, package: str) -> bool:
        """Launch an app by package name."""
        httpx_client = self._client.get_httpx_client()
        response = httpx_client.post(
            f"/api/v1/phones/{phone_id}/open_app",
            json={"package": package},
        )
        response.raise_for_status()
        return response.json().get("success", False)

    def push_file(
        self, phone_id: str, local_path: str | Path, remote_path: str
    ) -> bool:
        """Push a file to the device."""
        httpx_client = self._client.get_httpx_client()
        with open(local_path, "rb") as f:
            response = httpx_client.post(
                f"/api/v1/phones/{phone_id}/push",
                files={"file": ("file", f, "application/octet-stream")},
                data={"remote_path": remote_path},
                timeout=120,
            )
        response.raise_for_status()
        return response.json().get("success", False)

    def install_apk(self, phone_id: str, apk_path: str | Path) -> bool:
        """Install an APK on the device."""
        httpx_client = self._client.get_httpx_client()
        with open(apk_path, "rb") as f:
            response = httpx_client.post(
                f"/api/v1/phones/{phone_id}/install",
                files={
                    "file": (
                        Path(apk_path).name,
                        f,
                        "application/vnd.android.package-archive",
                    )
                },
                timeout=180,
            )
        response.raise_for_status()
        return response.json().get("success", False)

    # -- bridge management -------------------------------------------------

    def _close_bridge(self, slot_id: str) -> None:
        bridge = self._bridges.pop(slot_id, None)
        if bridge:
            bridge.close()

    def list_slots(
        self,
        *,
        status: str | None = None,
        cluster_id: str | None = None,
        owner: str | None = None,
    ) -> list[SlotInfo]:
        """List all slots, optionally filtered by status/cluster/owner."""
        result = gen_list_slots.sync_detailed(
            client=self._client,
            status=status,
            cluster_id=cluster_id,
            owner=owner,
        )
        self._check_error(result)
        parsed = result.parsed  # type: ignore[union-attr]
        return [self._slot_detail_to_info(s) for s in parsed.slots]  # type: ignore[union-attr]

    def get_slot(self, slot_id: str) -> SlotInfo:
        """Get a single slot by ID."""
        result = gen_get_slot.sync_detailed(slot_id, client=self._client)
        self._check_error(result)
        return self._slot_detail_to_info(result.parsed)  # type: ignore[arg-type]

    def get_slot_status_counts(self) -> dict[str, int]:
        """Get counts of slots by status. Returns {"available": N, "busy": N, "offline": N, "total": N}."""
        slots = self.list_slots()
        counts = {"available": 0, "busy": 0, "offline": 0, "total": len(slots)}
        for slot in slots:
            if slot.status in counts:
                counts[slot.status] += 1
        return counts

    # -- setups & preparation ------------------------------------------------

    def list_setups(self) -> list[SetupDefinition]:
        """List all setup definitions."""
        httpx_client = self._client.get_httpx_client()
        response = httpx_client.get("/api/v1/setups")
        response.raise_for_status()
        data = response.json()
        return [self._row_to_setup(s) for s in data.get("setups", [])]

    def get_setup_by_name(self, name: str) -> SetupDefinition:
        """Fetch a setup definition by name.

        Raises SlotNotFoundError if no setup with the given name exists.
        """
        setups = self.list_setups()
        for s in setups:
            if s.name == name:
                return s
        raise SlotNotFoundError(f"Setup '{name}' not found")

    def get_latest_preparation(self) -> PreparationDefinition | None:
        """Fetch the latest preparation steps.

        Returns None if no preparation steps are defined.
        """
        httpx_client = self._client.get_httpx_client()
        response = httpx_client.get("/api/v1/preparation/latest")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        data = response.json()
        return PreparationDefinition(
            id=data["id"],
            pre_install_commands=data.get("pre_install_commands", []),
            apps_installed=data.get("apps_installed", []),
            post_install_commands=data.get("post_install_commands", []),
        )

    # -- internal ----------------------------------------------------------

    @staticmethod
    def _row_to_setup(row: dict) -> SetupDefinition:
        """Convert a raw API row to a SetupDefinition."""
        return SetupDefinition(
            id=row["id"],
            name=row["name"],
            apps_installed=row.get("apps_installed", []),
            apk_urls=row.get("apk_urls", {}),
            setup_commands=row.get("setup_commands", []),
        )

    @staticmethod
    def _slot_detail_to_info(detail: object) -> SlotInfo:
        """Convert a generated SlotDetail to a public SlotInfo."""
        return SlotInfo(
            slot_id=detail.id,  # type: ignore[attr-defined]
            device_serial=detail.phone_serial,  # type: ignore[attr-defined]
            device_name=detail.phone_name or "",  # type: ignore[attr-defined]
            status=detail.status,  # type: ignore[attr-defined]
            setup_name=detail.setup_name,  # type: ignore[attr-defined]
            cluster_id=detail.cluster_id,  # type: ignore[attr-defined]
            cluster_name=detail.cluster_name,  # type: ignore[attr-defined]
            owner=detail.owner,  # type: ignore[attr-defined]
            has_active_session=detail.has_active_session,  # type: ignore[attr-defined]
            tunnel_url=detail.tunnel_url,  # type: ignore[attr-defined]
            created_at=detail.created_at,  # type: ignore[attr-defined]
            updated_at=detail.updated_at,  # type: ignore[attr-defined]
        )

    def _check_error(self, result: GenResponse) -> None:  # type: ignore[type-arg]
        status = result.status_code.value
        if 200 <= status < 300:
            return

        # Parse error detail from response body
        try:
            error_body = json.loads(result.content)
        except Exception:
            error_body = {"detail": HTTPStatus(status).phrase}

        raw_detail = error_body.get("detail", HTTPStatus(status).phrase)
        if isinstance(raw_detail, dict):
            detail = raw_detail.get("message", str(raw_detail))
            error_code = raw_detail.get("code")
        else:
            detail = str(raw_detail)
            error_code = None

        if status == 404:
            raise SlotNotFoundError(detail)
        if status == 409:
            if error_code == "DEVICE_BUSY":
                raise DeviceBusyError(detail)
            if error_code == "DEVICE_OFFLINE":
                raise DeviceOfflineError(detail)
            raise NoPhonesAvailableError(detail)
        if status == 503:
            raise TunnelNotAvailableError(detail)
        raise PhoneFarmError(status, detail)
