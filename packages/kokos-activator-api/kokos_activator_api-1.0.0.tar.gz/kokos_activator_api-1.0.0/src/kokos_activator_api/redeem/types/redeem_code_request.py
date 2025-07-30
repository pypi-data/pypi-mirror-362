# This file was auto-generated from our API Definition.

import typing

from .redeem_code_direct_request import RedeemCodeDirectRequest
from .redeem_code_from_db_request import RedeemCodeFromDbRequest

RedeemCodeRequest = typing.Union[RedeemCodeFromDbRequest, RedeemCodeDirectRequest]
