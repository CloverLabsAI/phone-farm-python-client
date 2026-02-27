from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.release_session_response import ReleaseSessionResponse
from ...types import Response


def _get_kwargs(
    slot_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/slots/{slot_id}/sessions/release".format(
            slot_id=quote(str(slot_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ReleaseSessionResponse | None:
    if response.status_code == 200:
        response_200 = ReleaseSessionResponse.from_dict(response.json())

        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[HTTPValidationError | ReleaseSessionResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    slot_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | ReleaseSessionResponse]:
    """Release Session

     Release the active session for a slot (idempotent).

    Args:
        slot_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ReleaseSessionResponse]
    """

    kwargs = _get_kwargs(
        slot_id=slot_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    slot_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | ReleaseSessionResponse | None:
    """Release Session

     Release the active session for a slot (idempotent).

    Args:
        slot_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ReleaseSessionResponse
    """

    return sync_detailed(
        slot_id=slot_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    slot_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | ReleaseSessionResponse]:
    """Release Session

     Release the active session for a slot (idempotent).

    Args:
        slot_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ReleaseSessionResponse]
    """

    kwargs = _get_kwargs(
        slot_id=slot_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    slot_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> HTTPValidationError | ReleaseSessionResponse | None:
    """Release Session

     Release the active session for a slot (idempotent).

    Args:
        slot_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ReleaseSessionResponse
    """

    return (
        await asyncio_detailed(
            slot_id=slot_id,
            client=client,
        )
    ).parsed
