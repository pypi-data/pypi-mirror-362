from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.checklist import Checklist
from ...types import Response


def _get_kwargs(
    checklist_uuid: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/marketplace-checklists/{checklist_uuid}/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Checklist:
    if response.status_code == 200:
        response_200 = Checklist.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Checklist]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    checklist_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Response[Checklist]:
    """
    Args:
        checklist_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Checklist]
    """

    kwargs = _get_kwargs(
        checklist_uuid=checklist_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    checklist_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Checklist:
    """
    Args:
        checklist_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Checklist
    """

    return sync_detailed(
        checklist_uuid=checklist_uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    checklist_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Response[Checklist]:
    """
    Args:
        checklist_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Checklist]
    """

    kwargs = _get_kwargs(
        checklist_uuid=checklist_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    checklist_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Checklist:
    """
    Args:
        checklist_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Checklist
    """

    return (
        await asyncio_detailed(
            checklist_uuid=checklist_uuid,
            client=client,
        )
    ).parsed
