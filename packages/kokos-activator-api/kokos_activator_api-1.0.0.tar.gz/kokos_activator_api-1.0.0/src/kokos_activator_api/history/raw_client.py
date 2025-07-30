# This file was auto-generated from our API Definition.

import datetime as dt
import typing
from json.decoder import JSONDecodeError

from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.datetime_utils import serialize_datetime
from ..core.http_response import AsyncHttpResponse, HttpResponse
from ..core.jsonable_encoder import jsonable_encoder
from ..core.pydantic_utilities import parse_obj_as
from ..core.request_options import RequestOptions
from ..redeem.types.full_receipt_or_error import FullReceiptOrError
from .errors.activation_not_found_error import ActivationNotFoundError
from .types.get_activation_history_response import GetActivationHistoryResponse
from .types.stats_response import StatsResponse


class RawHistoryClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def get_stats(
        self, *, date: typing.Optional[dt.date] = None, request_options: typing.Optional[RequestOptions] = None
    ) -> HttpResponse[StatsResponse]:
        """
        Get statistics about the number of redemptions for each pack on a given date. `0` in the `activations` field means that the activation was successful, but was performed with `codeOverride` and `requireReceipt` set to `false`, and so the amount is unknown. `0` in the `errors` field means that the activation was unsuccessful, and the amount is unknown.

        Parameters
        ----------
        date : typing.Optional[dt.date]
            The date to get statistics for. Defaults to the current date.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[StatsResponse]
        """
        _response = self._client_wrapper.httpx_client.request(
            "stats",
            method="GET",
            params={
                "date": str(date) if date is not None else None,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    StatsResponse,
                    parse_obj_as(
                        type_=StatsResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)

    def get_activation_history(
        self,
        *,
        before: typing.Optional[dt.datetime] = None,
        after: typing.Optional[dt.datetime] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> HttpResponse[GetActivationHistoryResponse]:
        """
        Get the list of recent activations

        Parameters
        ----------
        before : typing.Optional[dt.datetime]
            Get activations before this timestamp (sorted newest first)

        after : typing.Optional[dt.datetime]
            Get activations after this timestamp (sorted oldest first)

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[GetActivationHistoryResponse]
        """
        _response = self._client_wrapper.httpx_client.request(
            "history",
            method="GET",
            params={
                "before": serialize_datetime(before) if before is not None else None,
                "after": serialize_datetime(after) if after is not None else None,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    GetActivationHistoryResponse,
                    parse_obj_as(
                        type_=GetActivationHistoryResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)

    def get_receipt(
        self, id: int, *, request_options: typing.Optional[RequestOptions] = None
    ) -> HttpResponse[FullReceiptOrError]:
        """
        Get the full receipt for an existing activation

        Parameters
        ----------
        id : int
            Activation ID

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[FullReceiptOrError]
        """
        _response = self._client_wrapper.httpx_client.request(
            f"history/{jsonable_encoder(id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    FullReceiptOrError,
                    parse_obj_as(
                        type_=FullReceiptOrError,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            if _response.status_code == 404:
                raise ActivationNotFoundError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)


class AsyncRawHistoryClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def get_stats(
        self, *, date: typing.Optional[dt.date] = None, request_options: typing.Optional[RequestOptions] = None
    ) -> AsyncHttpResponse[StatsResponse]:
        """
        Get statistics about the number of redemptions for each pack on a given date. `0` in the `activations` field means that the activation was successful, but was performed with `codeOverride` and `requireReceipt` set to `false`, and so the amount is unknown. `0` in the `errors` field means that the activation was unsuccessful, and the amount is unknown.

        Parameters
        ----------
        date : typing.Optional[dt.date]
            The date to get statistics for. Defaults to the current date.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[StatsResponse]
        """
        _response = await self._client_wrapper.httpx_client.request(
            "stats",
            method="GET",
            params={
                "date": str(date) if date is not None else None,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    StatsResponse,
                    parse_obj_as(
                        type_=StatsResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)

    async def get_activation_history(
        self,
        *,
        before: typing.Optional[dt.datetime] = None,
        after: typing.Optional[dt.datetime] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AsyncHttpResponse[GetActivationHistoryResponse]:
        """
        Get the list of recent activations

        Parameters
        ----------
        before : typing.Optional[dt.datetime]
            Get activations before this timestamp (sorted newest first)

        after : typing.Optional[dt.datetime]
            Get activations after this timestamp (sorted oldest first)

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[GetActivationHistoryResponse]
        """
        _response = await self._client_wrapper.httpx_client.request(
            "history",
            method="GET",
            params={
                "before": serialize_datetime(before) if before is not None else None,
                "after": serialize_datetime(after) if after is not None else None,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    GetActivationHistoryResponse,
                    parse_obj_as(
                        type_=GetActivationHistoryResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)

    async def get_receipt(
        self, id: int, *, request_options: typing.Optional[RequestOptions] = None
    ) -> AsyncHttpResponse[FullReceiptOrError]:
        """
        Get the full receipt for an existing activation

        Parameters
        ----------
        id : int
            Activation ID

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[FullReceiptOrError]
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"history/{jsonable_encoder(id)}",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    FullReceiptOrError,
                    parse_obj_as(
                        type_=FullReceiptOrError,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            if _response.status_code == 404:
                raise ActivationNotFoundError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)
