from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.list_slots_response import ListSlotsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    status: None | str | Unset = UNSET,
    cluster_id: None | str | Unset = UNSET,
    owner: None | str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_status: None | str | Unset
    if isinstance(status, Unset):
        json_status = UNSET
    else:
        json_status = status
    params["status"] = json_status

    json_cluster_id: None | str | Unset
    if isinstance(cluster_id, Unset):
        json_cluster_id = UNSET
    else:
        json_cluster_id = cluster_id
    params["cluster_id"] = json_cluster_id

    json_owner: None | str | Unset
    if isinstance(owner, Unset):
        json_owner = UNSET
    else:
        json_owner = owner
    params["owner"] = json_owner

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/slots",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> HTTPValidationError | ListSlotsResponse | None:
    if response.status_code == 200:
        response_200 = ListSlotsResponse.from_dict(response.json())

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
) -> Response[HTTPValidationError | ListSlotsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    status: None | str | Unset = UNSET,
    cluster_id: None | str | Unset = UNSET,
    owner: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ListSlotsResponse]:
    r"""List Slots

     List all slots with enriched phone, cluster, and session data.

    Optional filters:
    - status: \"available\", \"busy\", or \"offline\"
    - cluster_id: filter by cluster
    - owner: filter by slot owner

    Args:
        status (None | str | Unset):
        cluster_id (None | str | Unset):
        owner (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ListSlotsResponse]
    """

    kwargs = _get_kwargs(
        status=status,
        cluster_id=cluster_id,
        owner=owner,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    status: None | str | Unset = UNSET,
    cluster_id: None | str | Unset = UNSET,
    owner: None | str | Unset = UNSET,
) -> HTTPValidationError | ListSlotsResponse | None:
    r"""List Slots

     List all slots with enriched phone, cluster, and session data.

    Optional filters:
    - status: \"available\", \"busy\", or \"offline\"
    - cluster_id: filter by cluster
    - owner: filter by slot owner

    Args:
        status (None | str | Unset):
        cluster_id (None | str | Unset):
        owner (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ListSlotsResponse
    """

    return sync_detailed(
        client=client,
        status=status,
        cluster_id=cluster_id,
        owner=owner,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    status: None | str | Unset = UNSET,
    cluster_id: None | str | Unset = UNSET,
    owner: None | str | Unset = UNSET,
) -> Response[HTTPValidationError | ListSlotsResponse]:
    r"""List Slots

     List all slots with enriched phone, cluster, and session data.

    Optional filters:
    - status: \"available\", \"busy\", or \"offline\"
    - cluster_id: filter by cluster
    - owner: filter by slot owner

    Args:
        status (None | str | Unset):
        cluster_id (None | str | Unset):
        owner (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError | ListSlotsResponse]
    """

    kwargs = _get_kwargs(
        status=status,
        cluster_id=cluster_id,
        owner=owner,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    status: None | str | Unset = UNSET,
    cluster_id: None | str | Unset = UNSET,
    owner: None | str | Unset = UNSET,
) -> HTTPValidationError | ListSlotsResponse | None:
    r"""List Slots

     List all slots with enriched phone, cluster, and session data.

    Optional filters:
    - status: \"available\", \"busy\", or \"offline\"
    - cluster_id: filter by cluster
    - owner: filter by slot owner

    Args:
        status (None | str | Unset):
        cluster_id (None | str | Unset):
        owner (None | str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError | ListSlotsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            status=status,
            cluster_id=cluster_id,
            owner=owner,
        )
    ).parsed
