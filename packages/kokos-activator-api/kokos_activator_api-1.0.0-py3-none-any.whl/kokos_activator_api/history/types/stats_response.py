# This file was auto-generated from our API Definition.

import datetime as dt
import typing

import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2, UniversalBaseModel
from ...database.types.database_inventory import DatabaseInventory


class StatsResponse(UniversalBaseModel):
    """
    Examples
    --------
    import datetime

    from kokos_activator_api.history import StatsResponse

    StatsResponse(
        date=datetime.date.fromisoformat(
            "2025-05-12",
        ),
        activations={
            "0": 0,
            "60": 18,
            "325": 0,
            "660": 5,
            "1800": 2,
            "3850": 0,
            "8100": 0,
        },
        errors={
            "0": 5,
            "60": 18,
            "325": 0,
            "660": 0,
            "1800": 2,
            "3850": 0,
            "8100": 1,
        },
    )
    """

    date: dt.date = pydantic.Field()
    """
    The date for which the statistics were requested
    """

    activations: DatabaseInventory = pydantic.Field()
    """
    The number of activations for each pack
    """

    errors: DatabaseInventory = pydantic.Field()
    """
    The number of errors for each pack
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
