from __future__ import annotations

import json
from http import HTTPStatus

from ._generated.client import Client as GenClient
from ._generated.api.slots import (
    create_slot as gen_create_slot,
    delete_slot as gen_delete_slot,
    create_session as gen_create_session,
    release_session as gen_release_session,
)
from ._generated.models.create_slot_body import CreateSlotBody
from ._generated.types import Response as GenResponse
from .errors import (
    DeviceBusyError,
    DeviceOfflineError,
    NoPhonesAvailableError,
    PhoneFarmError,
    SlotNotFoundError,
    TunnelNotAvailableError,
)
from .types import ReleaseSessionResponse


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
        *,
        cluster_id: str | None = None,
        owner: str | None = None,
    ) -> str:
        """Create a persistent slot (auto-assigns a device). Returns the slot ID."""
        body = CreateSlotBody(cluster_id=cluster_id, owner=owner) if cluster_id is not None or owner is not None else None
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
            slot_id=parsed.slot_id,
            session_id=parsed.session_id,
            status=parsed.status,
        )

    # -- internal ----------------------------------------------------------

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
