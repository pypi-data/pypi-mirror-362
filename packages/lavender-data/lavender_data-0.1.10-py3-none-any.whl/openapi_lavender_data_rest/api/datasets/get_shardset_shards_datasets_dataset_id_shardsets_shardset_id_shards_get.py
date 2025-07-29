from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_shardset_shards_response import GetShardsetShardsResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    dataset_id: str,
    shardset_id: str,
    *,
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 10,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["offset"] = offset

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/datasets/{dataset_id}/shardsets/{shardset_id}/shards",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetShardsetShardsResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = GetShardsetShardsResponse.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[GetShardsetShardsResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    dataset_id: str,
    shardset_id: str,
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 10,
) -> Response[Union[GetShardsetShardsResponse, HTTPValidationError]]:
    """Get Shardset Shards

    Args:
        dataset_id (str):
        shardset_id (str):
        offset (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetShardsetShardsResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        dataset_id=dataset_id,
        shardset_id=shardset_id,
        offset=offset,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    dataset_id: str,
    shardset_id: str,
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 10,
) -> Optional[Union[GetShardsetShardsResponse, HTTPValidationError]]:
    """Get Shardset Shards

    Args:
        dataset_id (str):
        shardset_id (str):
        offset (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetShardsetShardsResponse, HTTPValidationError]
    """

    return sync_detailed(
        dataset_id=dataset_id,
        shardset_id=shardset_id,
        client=client,
        offset=offset,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    dataset_id: str,
    shardset_id: str,
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 10,
) -> Response[Union[GetShardsetShardsResponse, HTTPValidationError]]:
    """Get Shardset Shards

    Args:
        dataset_id (str):
        shardset_id (str):
        offset (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetShardsetShardsResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        dataset_id=dataset_id,
        shardset_id=shardset_id,
        offset=offset,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    dataset_id: str,
    shardset_id: str,
    *,
    client: AuthenticatedClient,
    offset: Union[Unset, int] = 0,
    limit: Union[Unset, int] = 10,
) -> Optional[Union[GetShardsetShardsResponse, HTTPValidationError]]:
    """Get Shardset Shards

    Args:
        dataset_id (str):
        shardset_id (str):
        offset (Union[Unset, int]):  Default: 0.
        limit (Union[Unset, int]):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetShardsetShardsResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            dataset_id=dataset_id,
            shardset_id=shardset_id,
            client=client,
            offset=offset,
            limit=limit,
        )
    ).parsed
