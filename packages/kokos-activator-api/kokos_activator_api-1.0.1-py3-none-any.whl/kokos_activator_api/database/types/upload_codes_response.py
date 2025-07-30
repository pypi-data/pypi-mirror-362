# This file was auto-generated from our API Definition.

import typing

import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from ...redeem.types.code import Code
from .database_inventory import DatabaseInventory


class UploadCodesResponse(UniversalBaseModel):
    """
    Examples
    --------
    from kokos_activator_api.database import UploadCodesResponse

    UploadCodesResponse(
        inventory={"60": 18, "325": 0, "660": 0, "1800": 2, "3850": 0, "8100": 1},
        accepted={"60": 4, "325": 0, "660": 0, "1800": 0, "3850": 0, "8100": 0},
        used=["r3h4x2Jh2W2853g9g4"],
        disowned=[],
    )
    """

    inventory: DatabaseInventory = pydantic.Field()
    """
    New state of the database
    """

    accepted: DatabaseInventory = pydantic.Field()
    """
    Number of codes that were added to the database
    """

    used: typing.Set[Code] = pydantic.Field()
    """
    List of codes that were already in the database
    """

    disowned: typing.Set[Code] = pydantic.Field()
    """
    List of codes that belong to someone else and cannot be added
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
