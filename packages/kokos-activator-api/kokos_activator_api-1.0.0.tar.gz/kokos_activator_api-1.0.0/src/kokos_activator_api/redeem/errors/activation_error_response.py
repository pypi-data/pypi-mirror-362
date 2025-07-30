# This file was auto-generated from our API Definition.

import typing

from ...core.api_error import ApiError
from ..types.activation_error import ActivationError


class ActivationErrorResponse(ApiError):
    def __init__(self, body: ActivationError, headers: typing.Optional[typing.Dict[str, str]] = None):
        super().__init__(status_code=503, headers=headers, body=body)
