# This file was auto-generated from our API Definition.

import typing

import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from ...redeem.types.pack_denomination import PackDenomination


class DownloadCodesRequest(UniversalBaseModel):
    denomination: PackDenomination
    amount: int = pydantic.Field()
    """
    Amount of codes to extract
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
