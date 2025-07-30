# This file was auto-generated from our API Definition.

import typing

from ...core.api_error import ApiError


class RequestError(ApiError):
    def __init__(self, body: typing.Optional[typing.Any], headers: typing.Optional[typing.Dict[str, str]] = None):
        super().__init__(status_code=503, headers=headers, body=body)
