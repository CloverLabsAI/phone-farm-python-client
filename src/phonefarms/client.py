from __future__ import annotations

import json
from http import HTTPStatus
from typing import TYPE_CHECKING

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
    SlotInfo,
)

if TYPE_CHECKING:
    from ._generated.types import Response as GenResponse


class PhoneFarmClient:
    """Synchronous client for the Echos Automation phone farm API."""

    def __init__(self, base_url: str, api_key: str) -> None:
        self._client = GenClient(
            base_url=base_url.rstrip("/"),
            headers={
                "X-API-Key": api_key,
                "Content-Type": "application/json",
            },
        )

    # -- context manager --------------------------------------------------

    def __enter__(self) -> PhoneFarmClient:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP client."""
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
        result = gen_delete_slot.sync_detailed(slot_id, client=self._client)
        self._check_error(result)

    def create_session(self, slot_id: str) -> str:
        """Start an active session for a slot. Returns the tunnel URL."""
        result = gen_create_session.sync_detailed(slot_id, client=self._client)
        self._check_error(result)
        return result.parsed.url  # type: ignore[union-attr]

    def release_session(self, slot_id: str) -> ReleaseSessionResponse:
        """Release the active session for a slot (idempotent)."""
        result = gen_release_session.sync_detailed(slot_id, client=self._client)
        self._check_error(result)
        parsed = result.parsed  # type: ignore[union-attr]
        return ReleaseSessionResponse(
            slot_id=parsed.slot_id,  # type: ignore[union-attr]
            session_id=parsed.session_id,  # type: ignore[union-attr]
            status=parsed.status,  # type: ignore[union-attr]
        )

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
