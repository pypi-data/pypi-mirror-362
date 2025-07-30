from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.answer_submit import AnswerSubmit
from ...models.answer_submit_request import AnswerSubmitRequest
from ...types import UNSET, Response, Unset


def _get_kwargs(
    checklist_uuid: str,
    *,
    body: list["AnswerSubmitRequest"],
    on_behalf_user_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    json_on_behalf_user_uuid: Union[Unset, str] = UNSET
    if not isinstance(on_behalf_user_uuid, Unset):
        json_on_behalf_user_uuid = str(on_behalf_user_uuid)
    params["on_behalf_user_uuid"] = json_on_behalf_user_uuid

    params["page"] = page

    params["page_size"] = page_size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-checklists/{checklist_uuid}/answers/submit/",
        "params": params,
    }

    _kwargs["json"] = []
    for body_item_data in body:
        body_item = body_item_data.to_dict()
        _kwargs["json"].append(body_item)

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> list["AnswerSubmit"]:
    if response.status_code == 201:
        response_201 = []
        _response_201 = response.json()
        for response_201_item_data in _response_201:
            response_201_item = AnswerSubmit.from_dict(response_201_item_data)

            response_201.append(response_201_item)

        return response_201
    raise errors.UnexpectedStatus(response.status_code, response.content)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["AnswerSubmit"]]:
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
    body: list["AnswerSubmitRequest"],
    on_behalf_user_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> Response[list["AnswerSubmit"]]:
    """Submit answer to checklist question

    Args:
        checklist_uuid (str):
        on_behalf_user_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        body (list['AnswerSubmitRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AnswerSubmit']]
    """

    kwargs = _get_kwargs(
        checklist_uuid=checklist_uuid,
        body=body,
        on_behalf_user_uuid=on_behalf_user_uuid,
        page=page,
        page_size=page_size,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    checklist_uuid: str,
    *,
    client: AuthenticatedClient,
    body: list["AnswerSubmitRequest"],
    on_behalf_user_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> list["AnswerSubmit"]:
    """Submit answer to checklist question

    Args:
        checklist_uuid (str):
        on_behalf_user_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        body (list['AnswerSubmitRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AnswerSubmit']
    """

    return sync_detailed(
        checklist_uuid=checklist_uuid,
        client=client,
        body=body,
        on_behalf_user_uuid=on_behalf_user_uuid,
        page=page,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    checklist_uuid: str,
    *,
    client: AuthenticatedClient,
    body: list["AnswerSubmitRequest"],
    on_behalf_user_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> Response[list["AnswerSubmit"]]:
    """Submit answer to checklist question

    Args:
        checklist_uuid (str):
        on_behalf_user_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        body (list['AnswerSubmitRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['AnswerSubmit']]
    """

    kwargs = _get_kwargs(
        checklist_uuid=checklist_uuid,
        body=body,
        on_behalf_user_uuid=on_behalf_user_uuid,
        page=page,
        page_size=page_size,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    checklist_uuid: str,
    *,
    client: AuthenticatedClient,
    body: list["AnswerSubmitRequest"],
    on_behalf_user_uuid: Union[Unset, UUID] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
) -> list["AnswerSubmit"]:
    """Submit answer to checklist question

    Args:
        checklist_uuid (str):
        on_behalf_user_uuid (Union[Unset, UUID]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        body (list['AnswerSubmitRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['AnswerSubmit']
    """

    return (
        await asyncio_detailed(
            checklist_uuid=checklist_uuid,
            client=client,
            body=body,
            on_behalf_user_uuid=on_behalf_user_uuid,
            page=page,
            page_size=page_size,
        )
    ).parsed
