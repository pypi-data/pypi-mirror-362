# This file was auto-generated from our API Definition.

import typing
from json.decoder import JSONDecodeError

from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.http_response import AsyncHttpResponse, HttpResponse
from ..core.pydantic_utilities import parse_obj_as
from ..core.request_options import RequestOptions
from ..core.serialization import convert_and_respect_annotation_metadata
from ..redeem.types.code import Code
from ..redeem.types.pack_denomination import PackDenomination
from .types.database_inventory import DatabaseInventory
from .types.upload_codes_response import UploadCodesResponse
from .types.upload_pack import UploadPack

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class RawDatabaseClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def get_inventory(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> HttpResponse[DatabaseInventory]:
        """
        Get the amount of codes in the database for each pack

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[DatabaseInventory]
        """
        _response = self._client_wrapper.httpx_client.request(
            "db",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    DatabaseInventory,
                    parse_obj_as(
                        type_=DatabaseInventory,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)

    def upload_codes(
        self, *, request: typing.Sequence[UploadPack], request_options: typing.Optional[RequestOptions] = None
    ) -> HttpResponse[UploadCodesResponse]:
        """
        Add codes to the database

        Parameters
        ----------
        request : typing.Sequence[UploadPack]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[UploadCodesResponse]
        """
        _response = self._client_wrapper.httpx_client.request(
            "db",
            method="POST",
            json=convert_and_respect_annotation_metadata(
                object_=request, annotation=typing.Sequence[UploadPack], direction="write"
            ),
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    UploadCodesResponse,
                    parse_obj_as(
                        type_=UploadCodesResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)

    def download_codes(
        self, *, denomination: PackDenomination, amount: int, request_options: typing.Optional[RequestOptions] = None
    ) -> HttpResponse[typing.Set[Code]]:
        """
        Extract codes from the database

        Parameters
        ----------
        denomination : PackDenomination

        amount : int
            Amount of codes to extract

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[typing.Set[Code]]
        """
        _response = self._client_wrapper.httpx_client.request(
            "db/extract",
            method="POST",
            json={
                "denomination": denomination,
                "amount": amount,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    typing.Set[Code],
                    parse_obj_as(
                        type_=typing.Set[Code],  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)


class AsyncRawDatabaseClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def get_inventory(
        self, *, request_options: typing.Optional[RequestOptions] = None
    ) -> AsyncHttpResponse[DatabaseInventory]:
        """
        Get the amount of codes in the database for each pack

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[DatabaseInventory]
        """
        _response = await self._client_wrapper.httpx_client.request(
            "db",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    DatabaseInventory,
                    parse_obj_as(
                        type_=DatabaseInventory,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)

    async def upload_codes(
        self, *, request: typing.Sequence[UploadPack], request_options: typing.Optional[RequestOptions] = None
    ) -> AsyncHttpResponse[UploadCodesResponse]:
        """
        Add codes to the database

        Parameters
        ----------
        request : typing.Sequence[UploadPack]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[UploadCodesResponse]
        """
        _response = await self._client_wrapper.httpx_client.request(
            "db",
            method="POST",
            json=convert_and_respect_annotation_metadata(
                object_=request, annotation=typing.Sequence[UploadPack], direction="write"
            ),
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    UploadCodesResponse,
                    parse_obj_as(
                        type_=UploadCodesResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)

    async def download_codes(
        self, *, denomination: PackDenomination, amount: int, request_options: typing.Optional[RequestOptions] = None
    ) -> AsyncHttpResponse[typing.Set[Code]]:
        """
        Extract codes from the database

        Parameters
        ----------
        denomination : PackDenomination

        amount : int
            Amount of codes to extract

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[typing.Set[Code]]
        """
        _response = await self._client_wrapper.httpx_client.request(
            "db/extract",
            method="POST",
            json={
                "denomination": denomination,
                "amount": amount,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    typing.Set[Code],
                    parse_obj_as(
                        type_=typing.Set[Code],  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)
