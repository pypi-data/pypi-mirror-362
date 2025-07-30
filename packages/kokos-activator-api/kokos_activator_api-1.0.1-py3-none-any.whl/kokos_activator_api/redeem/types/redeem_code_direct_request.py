# This file was auto-generated from our API Definition.

import typing

import pydantic
import typing_extensions
from ...core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from ...core.serialization import FieldMetadata
from .code import Code
from .player_id import PlayerId


class RedeemCodeDirectRequest(UniversalBaseModel):
    """
    Examples
    --------
    from kokos_activator_api.redeem import RedeemCodeDirectRequest

    RedeemCodeDirectRequest(
        require_receipt=True,
        player_id="51709255708",
        code_override="r3h4xcJ72f2056g7h7",
    )
    """

    require_receipt: typing_extensions.Annotated[bool, FieldMetadata(alias="requireReceipt")] = pydantic.Field()
    """
    Does this activation require authentication and a full receipt?
    """

    player_id: typing_extensions.Annotated[PlayerId, FieldMetadata(alias="playerId")]
    code_override: typing_extensions.Annotated[Code, FieldMetadata(alias="codeOverride")] = pydantic.Field()
    """
    The redemption code to activate
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
