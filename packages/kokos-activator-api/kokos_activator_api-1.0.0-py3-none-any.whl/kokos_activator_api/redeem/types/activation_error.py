# This file was auto-generated from our API Definition.

import datetime as dt
import typing

import pydantic
import typing_extensions
from ...core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from ...core.serialization import FieldMetadata
from .code import Code
from .error_code import ErrorCode
from .player_id import PlayerId


class ActivationError(UniversalBaseModel):
    """
    Examples
    --------
    import datetime

    from kokos_activator_api.redeem import ActivationError

    ActivationError(
        id=100407,
        created_at=datetime.datetime.fromisoformat(
            "2024-09-25 17:32:28+00:00",
        ),
        error_code="CODE_USED",
        error_message="REDEEM_CODE_ALREADY_USED: Redeem code is already used, please check the redeem code, cause: -, solution:-, debugid: 98fa4c6ab945320d0fe4304f38cc5653",
        code_reset=False,
        player_id="51709255708",
        code="r3h4xcJ72f2056g7h7",
    )
    """

    type: typing.Literal["ActivationError"] = "ActivationError"
    id: int = pydantic.Field()
    """
    Unique ID of this receipt
    """

    code: typing.Optional[Code] = pydantic.Field(default=None)
    """
    The redemption code that was used (null if no code was found)
    """

    player_id: typing_extensions.Annotated[PlayerId, FieldMetadata(alias="playerId")] = pydantic.Field()
    """
    The player ID that was used
    """

    error_code: typing_extensions.Annotated[ErrorCode, FieldMetadata(alias="errorCode")]
    error_message: typing_extensions.Annotated[typing.Optional[str], FieldMetadata(alias="errorMessage")] = (
        pydantic.Field(default=None)
    )
    """
    Detailed and technical error message. (Should NOT be shown to an untrusted user)
    """

    code_reset: typing_extensions.Annotated[bool, FieldMetadata(alias="codeReset")] = pydantic.Field()
    """
    True if the code was put back into the database. Always false when codeOverride is used.
    """

    created_at: typing_extensions.Annotated[dt.datetime, FieldMetadata(alias="createdAt")] = pydantic.Field()
    """
    When this error was created
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
