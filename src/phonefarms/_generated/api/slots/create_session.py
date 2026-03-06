from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_session_response import CreateSessionResponse
from ...models.http_validation_error import HTTPValidationError
from typing import cast


def _get_kwargs(
    slot_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/slots/{slot_id}/sessions".format(
            slot_id=quote(str(slot_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CreateSessionResponse | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = CreateSessionResponse.from_dict(response.json())

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
) -> Response[CreateSessionResponse | HTTPValidationError]:
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
) -> Response[CreateSessionResponse | HTTPValidationError]:
    """Create Session

     Create an active session for a slot and return tunnel URL.

    Args:
        slot_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateSessionResponse | HTTPValidationError]
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
) -> CreateSessionResponse | HTTPValidationError | None:
    """Create Session

     Create an active session for a slot and return tunnel URL.

    Args:
        slot_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateSessionResponse | HTTPValidationError
    """

    return sync_detailed(
        slot_id=slot_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    slot_id: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[CreateSessionResponse | HTTPValidationError]:
    """Create Session

     Create an active session for a slot and return tunnel URL.

    Args:
        slot_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreateSessionResponse | HTTPValidationError]
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
) -> CreateSessionResponse | HTTPValidationError | None:
    """Create Session

     Create an active session for a slot and return tunnel URL.

    Args:
        slot_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreateSessionResponse | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            slot_id=slot_id,
            client=client,
        )
    ).parsed
