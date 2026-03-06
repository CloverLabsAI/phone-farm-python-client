from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.http_validation_error import HTTPValidationError
from ...models.slot_detail import SlotDetail
from typing import cast


def _get_kwargs(
    slot_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/slots/{slot_id}".format(
            slot_id=quote(str(slot_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | SlotDetail | None:
    if response.status_code == 200:
        response_200 = SlotDetail.from_dict(response.json())

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
) -> Response[HTTPValidationError | SlotDetail]:
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
) -> Response[HTTPValidationError | SlotDetail]:
    """Get Slot

     Get a single slot by ID with enriched phone, cluster, and session data.

    Args:
        slot_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SlotDetail]
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
) -> HTTPValidationError | SlotDetail | None:
    """Get Slot

     Get a single slot by ID with enriched phone, cluster, and session data.

    Args:
        slot_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SlotDetail
    """

    return sync_detailed(
        slot_id=slot_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    slot_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[HTTPValidationError | SlotDetail]:
    """Get Slot

     Get a single slot by ID with enriched phone, cluster, and session data.

    Args:
        slot_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | SlotDetail]
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
) -> HTTPValidationError | SlotDetail | None:
    """Get Slot

     Get a single slot by ID with enriched phone, cluster, and session data.

    Args:
        slot_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | SlotDetail
    """

    return (
        await asyncio_detailed(
            slot_id=slot_id,
            client=client,
        )
    ).parsed
