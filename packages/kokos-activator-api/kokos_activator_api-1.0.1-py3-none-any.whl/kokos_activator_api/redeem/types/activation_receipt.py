# This file was auto-generated from our API Definition.

import datetime as dt
import typing

import pydantic
import typing_extensions
from ...core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from ...core.serialization import FieldMetadata
from .code import Code
from .midas_uid import MidasUid
from .open_id import OpenId
from .pack_denomination import PackDenomination
from .player_id import PlayerId
from .player_name import PlayerName
from .product_name import ProductName
from .region import Region


class ActivationReceipt(UniversalBaseModel):
    """
    Examples
    --------
    import datetime

    from kokos_activator_api.redeem import ActivationReceipt

    ActivationReceipt(
        id=100407,
        created_at=datetime.datetime.fromisoformat(
            "2025-01-13 08:27:18.520000+00:00",
        ),
        warning=False,
        took=6250,
        player_id="51709255708",
        code="r3h4xcJ72f2056g7h7",
        openid="89924021864760616",
        name="『NT』ярый",
        user_id=42,
        product_name="UC*600",
        amount=660,
        uid="U2463icbmr4k8h",
        email="midwereo45mdn9cs@kokos.world",
        password="KOKOS1_H1HA5CT1",
    )
    """

    type: typing.Literal["ActivationReceipt"] = "ActivationReceipt"
    id: int = pydantic.Field()
    """
    Unique ID of this receipt
    """

    user_id: typing_extensions.Annotated[typing.Optional[int], FieldMetadata(alias="userId")] = pydantic.Field(
        default=None
    )
    """
    ID of the user who owns this receipt
    """

    created_at: typing_extensions.Annotated[dt.datetime, FieldMetadata(alias="createdAt")] = pydantic.Field()
    """
    When this receipt was created
    """

    warning: bool = pydantic.Field()
    """
    True if this activation was performed without a full receipt
    """

    took: int = pydantic.Field()
    """
    How long the activation took in milliseconds
    """

    player_id: typing_extensions.Annotated[PlayerId, FieldMetadata(alias="playerId")] = pydantic.Field()
    """
    ID of the player to whom this activation was made
    """

    code: Code = pydantic.Field()
    """
    The redemption code that was used
    """

    openid: OpenId
    name: PlayerName
    region: typing.Optional[Region] = None
    product_name: typing_extensions.Annotated[typing.Optional[ProductName], FieldMetadata(alias="productName")] = None
    amount: typing.Optional[PackDenomination] = None
    uid: typing.Optional[MidasUid] = None
    email: typing.Optional[str] = pydantic.Field(default=None)
    """
    Email of the MidasBuy account that performed the activation
    """

    password: typing.Optional[str] = pydantic.Field(default=None)
    """
    Password of the MidasBuy account that performed the activation
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
