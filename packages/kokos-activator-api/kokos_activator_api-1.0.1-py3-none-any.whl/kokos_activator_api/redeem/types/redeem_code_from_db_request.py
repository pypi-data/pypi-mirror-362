# This file was auto-generated from our API Definition.

import typing

import pydantic
import typing_extensions
from ...core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from ...core.serialization import FieldMetadata
from .pack_denomination import PackDenomination
from .player_id import PlayerId


class RedeemCodeFromDbRequest(UniversalBaseModel):
    require_receipt: typing_extensions.Annotated[bool, FieldMetadata(alias="requireReceipt")] = pydantic.Field()
    """
    Does this activation require authentication and a full receipt?
    """

    player_id: typing_extensions.Annotated[PlayerId, FieldMetadata(alias="playerId")]
    denomination: PackDenomination = pydantic.Field()
    """
    The database pack from which the code should be taken
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
