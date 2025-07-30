# This file was auto-generated from our API Definition.

import typing

import pydantic
import typing_extensions
from ...core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from ...core.serialization import FieldMetadata
from .open_id import OpenId
from .player_id import PlayerId
from .player_name import PlayerName


class Character(UniversalBaseModel):
    """
    Examples
    --------
    from kokos_activator_api.redeem import Character

    Character(
        player_id="51709255708",
        openid="89924021864760616",
        name="『NT』ярый",
    )
    """

    player_id: typing_extensions.Annotated[PlayerId, FieldMetadata(alias="playerId")]
    openid: OpenId
    name: PlayerName

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
