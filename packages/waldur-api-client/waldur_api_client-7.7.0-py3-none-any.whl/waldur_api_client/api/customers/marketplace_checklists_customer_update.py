from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import Response


def _get_kwargs(
    customer_uuid: str,
    *,
    body: list[UUID],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/customers/{customer_uuid}/marketplace-checklists/",
    }

    _kwargs["json"] = []
    for body_item_data in body:
        body_item = str(body_item_data)
        _kwargs["json"].append(body_item)

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list[UUID]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = UUID(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[list[UUID]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    customer_uuid: str,
    *,
    client: AuthenticatedClient,
    body: list[UUID],
) -> Response[list[UUID]]:
    """
    Args:
        customer_uuid (str):
        body (list[UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[UUID]]
    """

    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    customer_uuid: str,
    *,
    client: AuthenticatedClient,
    body: list[UUID],
) -> list[UUID]:
    """
    Args:
        customer_uuid (str):
        body (list[UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[UUID]
    """

    return sync_detailed(
        customer_uuid=customer_uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    customer_uuid: str,
    *,
    client: AuthenticatedClient,
    body: list[UUID],
) -> Response[list[UUID]]:
    """
    Args:
        customer_uuid (str):
        body (list[UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[UUID]]
    """

    kwargs = _get_kwargs(
        customer_uuid=customer_uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    customer_uuid: str,
    *,
    client: AuthenticatedClient,
    body: list[UUID],
) -> list[UUID]:
    """
    Args:
        customer_uuid (str):
        body (list[UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[UUID]
    """

    return (
        await asyncio_detailed(
            customer_uuid=customer_uuid,
            client=client,
            body=body,
        )
    ).parsed
