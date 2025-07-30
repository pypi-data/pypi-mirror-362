# This file was auto-generated from our API Definition.

import datetime as dt
import typing

import pydantic
import typing_extensions
from ...core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from ...core.serialization import FieldMetadata
from ...redeem.types.code import Code
from ...redeem.types.pack_denomination import PackDenomination
from ...redeem.types.player_id import PlayerId


class ShortReceipt(UniversalBaseModel):
    """
    Examples
    --------
    import datetime

    from kokos_activator_api.history import ShortReceipt

    ShortReceipt(
        id=5120,
        error=False,
        warning=False,
        code="NQ7QDWZw2F2eZ4ndZd",
        denomination=60,
        player_id="51709255708",
        created_at=datetime.datetime.fromisoformat(
            "2025-05-12 14:23:21.220000+00:00",
        ),
    )
    """

    id: int = pydantic.Field()
    """
    Activation ID
    """

    error: bool = pydantic.Field()
    """
    Whether the activation was unsuccessful
    """

    warning: bool = pydantic.Field()
    """
    Whether the activation doesn't have a full receipt (login+password)
    """

    code: typing.Optional[Code] = pydantic.Field(default=None)
    """
    The code that was used, unless the error is `NO_CODES_AVAILABLE`
    """

    denomination: typing.Optional[PackDenomination] = pydantic.Field(default=None)
    """
    Amount of UC activated, if known from the database or the full receipt
    """

    player_id: typing_extensions.Annotated[PlayerId, FieldMetadata(alias="playerId")] = pydantic.Field()
    """
    Destination player ID
    """

    created_at: typing_extensions.Annotated[dt.datetime, FieldMetadata(alias="createdAt")] = pydantic.Field()
    """
    Activation time
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
