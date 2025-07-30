# This file was auto-generated from our API Definition.

import typing
from json.decoder import JSONDecodeError

from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.http_response import AsyncHttpResponse, HttpResponse
from ..core.pydantic_utilities import parse_obj_as
from ..core.request_options import RequestOptions
from ..core.serialization import convert_and_respect_annotation_metadata
from .errors.activation_error_response import ActivationErrorResponse
from .errors.character_not_found_error import CharacterNotFoundError
from .errors.code_not_found_error import CodeNotFoundError
from .errors.request_error import RequestError
from .types.activation_error import ActivationError
from .types.activation_receipt import ActivationReceipt
from .types.character import Character
from .types.code import Code
from .types.player_id import PlayerId
from .types.redeem_code_request import RedeemCodeRequest
from .types.redemption_time import RedemptionTime

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class RawRedeemClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def redeem_code(
        self, *, request: RedeemCodeRequest, request_options: typing.Optional[RequestOptions] = None
    ) -> HttpResponse[ActivationReceipt]:
        """
        Activate a code

        Parameters
        ----------
        request : RedeemCodeRequest

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[ActivationReceipt]
        """
        _response = self._client_wrapper.httpx_client.request(
            "redeem",
            method="POST",
            json=convert_and_respect_annotation_metadata(
                object_=request, annotation=RedeemCodeRequest, direction="write"
            ),
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    ActivationReceipt,
                    parse_obj_as(
                        type_=ActivationReceipt,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            if _response.status_code == 503:
                raise ActivationErrorResponse(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        ActivationError,
                        parse_obj_as(
                            type_=ActivationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)

    def get_redemption_time(
        self, *, code: Code, request_options: typing.Optional[RequestOptions] = None
    ) -> HttpResponse[RedemptionTime]:
        """
        Get the redemption time of a code

        Parameters
        ----------
        code : Code
            Code to check

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[RedemptionTime]
        """
        _response = self._client_wrapper.httpx_client.request(
            "redemption-time",
            method="GET",
            params={
                "code": code,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    RedemptionTime,
                    parse_obj_as(
                        type_=RedemptionTime,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            if _response.status_code == 404:
                raise CodeNotFoundError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            if _response.status_code == 503:
                raise RequestError(
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

    def get_character(
        self, *, player_id: PlayerId, request_options: typing.Optional[RequestOptions] = None
    ) -> HttpResponse[Character]:
        """
        Get information about a player

        Parameters
        ----------
        player_id : PlayerId

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[Character]
        """
        _response = self._client_wrapper.httpx_client.request(
            "character",
            method="GET",
            params={
                "playerId": player_id,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    Character,
                    parse_obj_as(
                        type_=Character,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            if _response.status_code == 404:
                raise CharacterNotFoundError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            if _response.status_code == 503:
                raise RequestError(
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


class AsyncRawRedeemClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def redeem_code(
        self, *, request: RedeemCodeRequest, request_options: typing.Optional[RequestOptions] = None
    ) -> AsyncHttpResponse[ActivationReceipt]:
        """
        Activate a code

        Parameters
        ----------
        request : RedeemCodeRequest

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[ActivationReceipt]
        """
        _response = await self._client_wrapper.httpx_client.request(
            "redeem",
            method="POST",
            json=convert_and_respect_annotation_metadata(
                object_=request, annotation=RedeemCodeRequest, direction="write"
            ),
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    ActivationReceipt,
                    parse_obj_as(
                        type_=ActivationReceipt,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            if _response.status_code == 503:
                raise ActivationErrorResponse(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        ActivationError,
                        parse_obj_as(
                            type_=ActivationError,  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response.text)
        raise ApiError(status_code=_response.status_code, headers=dict(_response.headers), body=_response_json)

    async def get_redemption_time(
        self, *, code: Code, request_options: typing.Optional[RequestOptions] = None
    ) -> AsyncHttpResponse[RedemptionTime]:
        """
        Get the redemption time of a code

        Parameters
        ----------
        code : Code
            Code to check

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[RedemptionTime]
        """
        _response = await self._client_wrapper.httpx_client.request(
            "redemption-time",
            method="GET",
            params={
                "code": code,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    RedemptionTime,
                    parse_obj_as(
                        type_=RedemptionTime,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            if _response.status_code == 404:
                raise CodeNotFoundError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            if _response.status_code == 503:
                raise RequestError(
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

    async def get_character(
        self, *, player_id: PlayerId, request_options: typing.Optional[RequestOptions] = None
    ) -> AsyncHttpResponse[Character]:
        """
        Get information about a player

        Parameters
        ----------
        player_id : PlayerId

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[Character]
        """
        _response = await self._client_wrapper.httpx_client.request(
            "character",
            method="GET",
            params={
                "playerId": player_id,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    Character,
                    parse_obj_as(
                        type_=Character,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            if _response.status_code == 404:
                raise CharacterNotFoundError(
                    headers=dict(_response.headers),
                    body=typing.cast(
                        typing.Optional[typing.Any],
                        parse_obj_as(
                            type_=typing.Optional[typing.Any],  # type: ignore
                            object_=_response.json(),
                        ),
                    ),
                )
            if _response.status_code == 503:
                raise RequestError(
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
