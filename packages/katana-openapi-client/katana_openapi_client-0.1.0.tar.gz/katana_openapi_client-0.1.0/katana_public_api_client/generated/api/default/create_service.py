from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_service_response_401 import CreateServiceResponse401
from ...models.create_service_response_429 import CreateServiceResponse429
from ...models.create_service_response_500 import CreateServiceResponse500
from ...models.service_request import ServiceRequest
from ...models.service_response import ServiceResponse
from ...types import Response


def _get_kwargs(
    *,
    body: ServiceRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/services",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        CreateServiceResponse401,
        CreateServiceResponse429,
        CreateServiceResponse500,
        ServiceResponse,
    ]
]:
    if response.status_code == 201:
        response_201 = ServiceResponse.from_dict(response.json())

        return response_201
    if response.status_code == 401:
        response_401 = CreateServiceResponse401.from_dict(response.json())

        return response_401
    if response.status_code == 429:
        response_429 = CreateServiceResponse429.from_dict(response.json())

        return response_429
    if response.status_code == 500:
        response_500 = CreateServiceResponse500.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        CreateServiceResponse401,
        CreateServiceResponse429,
        CreateServiceResponse500,
        ServiceResponse,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ServiceRequest,
) -> Response[
    Union[
        CreateServiceResponse401,
        CreateServiceResponse429,
        CreateServiceResponse500,
        ServiceResponse,
    ]
]:
    """Create Service

     Create a new Service. (See: [Create
    Service](https://developer.katanamrp.com/reference/createservice))

    Args:
        body (ServiceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateServiceResponse401, CreateServiceResponse429, CreateServiceResponse500, ServiceResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ServiceRequest,
) -> Optional[
    Union[
        CreateServiceResponse401,
        CreateServiceResponse429,
        CreateServiceResponse500,
        ServiceResponse,
    ]
]:
    """Create Service

     Create a new Service. (See: [Create
    Service](https://developer.katanamrp.com/reference/createservice))

    Args:
        body (ServiceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateServiceResponse401, CreateServiceResponse429, CreateServiceResponse500, ServiceResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ServiceRequest,
) -> Response[
    Union[
        CreateServiceResponse401,
        CreateServiceResponse429,
        CreateServiceResponse500,
        ServiceResponse,
    ]
]:
    """Create Service

     Create a new Service. (See: [Create
    Service](https://developer.katanamrp.com/reference/createservice))

    Args:
        body (ServiceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateServiceResponse401, CreateServiceResponse429, CreateServiceResponse500, ServiceResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: ServiceRequest,
) -> Optional[
    Union[
        CreateServiceResponse401,
        CreateServiceResponse429,
        CreateServiceResponse500,
        ServiceResponse,
    ]
]:
    """Create Service

     Create a new Service. (See: [Create
    Service](https://developer.katanamrp.com/reference/createservice))

    Args:
        body (ServiceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateServiceResponse401, CreateServiceResponse429, CreateServiceResponse500, ServiceResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
