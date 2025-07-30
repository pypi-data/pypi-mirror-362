# This file was auto-generated from our API Definition.

import datetime as dt
import typing

import pydantic
import typing_extensions
from ...core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from ...core.serialization import FieldMetadata
from .open_id import OpenId
from .pack_denomination import PackDenomination
from .player_id import PlayerId
from .player_name import PlayerName


class RedemptionTime(UniversalBaseModel):
    redemption_time: typing_extensions.Annotated[dt.datetime, FieldMetadata(alias="redemptionTime")] = pydantic.Field()
    """
    When the code was activated
    """

    expiration_time: typing_extensions.Annotated[dt.datetime, FieldMetadata(alias="expirationTime")] = pydantic.Field()
    """
    When the code expires
    """

    channel_name: typing_extensions.Annotated[str, FieldMetadata(alias="channelName")] = pydantic.Field()
    """
    Company that distributed the code
    """

    openid: OpenId
    amount: PackDenomination = pydantic.Field()
    """
    Amount of UC
    """

    name: str = pydantic.Field()
    """
    Product name of the code
    """

    player_id: typing_extensions.Annotated[typing.Optional[PlayerId], FieldMetadata(alias="playerId")] = pydantic.Field(
        default=None
    )
    """
    Player ID to whom the code was redeemed (if known)
    """

    player_name: typing_extensions.Annotated[typing.Optional[PlayerName], FieldMetadata(alias="playerName")] = (
        pydantic.Field(default=None)
    )
    """
    Name of the player to whom the code was redeemed (if known)
    """

    receipt_id: typing_extensions.Annotated[typing.Optional[int], FieldMetadata(alias="receiptId")] = pydantic.Field(
        default=None
    )
    """
    ID of the activation receipt (if known)
    """

    receipt_successful: typing_extensions.Annotated[typing.Optional[bool], FieldMetadata(alias="receiptSuccessful")] = (
        pydantic.Field(default=None)
    )
    """
    Whether the activation receipt was successful (if known)
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
