# This file was auto-generated from our API Definition.

import typing

from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.request_options import RequestOptions
from .raw_client import AsyncRawRedeemClient, RawRedeemClient
from .types.activation_receipt import ActivationReceipt
from .types.character import Character
from .types.code import Code
from .types.player_id import PlayerId
from .types.redeem_code_request import RedeemCodeRequest
from .types.redemption_time import RedemptionTime

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class RedeemClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._raw_client = RawRedeemClient(client_wrapper=client_wrapper)

    @property
    def with_raw_response(self) -> RawRedeemClient:
        """
        Retrieves a raw implementation of this client that returns raw responses.

        Returns
        -------
        RawRedeemClient
        """
        return self._raw_client

    def redeem_code(
        self, *, request: RedeemCodeRequest, request_options: typing.Optional[RequestOptions] = None
    ) -> ActivationReceipt:
        """
        Activate a code

        Parameters
        ----------
        request : RedeemCodeRequest

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ActivationReceipt

        Examples
        --------
        from kokos_activator_api import KokosApi
        from kokos_activator_api.environment import KokosApiEnvironment
        from kokos_activator_api.redeem import RedeemCodeFromDbRequest

        client = KokosApi(
            token="YOUR_TOKEN",
            environment=KokosApiEnvironment.PRODUCTION,
        )
        client.redeem.redeem_code(
            request=RedeemCodeFromDbRequest(
                require_receipt=True,
                player_id="51709255708",
                denomination=660,
            ),
        )
        """
        _response = self._raw_client.redeem_code(request=request, request_options=request_options)
        return _response.data

    def get_redemption_time(
        self, *, code: Code, request_options: typing.Optional[RequestOptions] = None
    ) -> RedemptionTime:
        """
        Get the redemption time of a code

        Parameters
        ----------
        code : Code
            Code to check

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        RedemptionTime

        Examples
        --------
        from kokos_activator_api import KokosApi
        from kokos_activator_api.environment import KokosApiEnvironment

        client = KokosApi(
            token="YOUR_TOKEN",
            environment=KokosApiEnvironment.PRODUCTION,
        )
        client.redeem.get_redemption_time(
            code="r3h4xcJ72f2056g7h7",
        )
        """
        _response = self._raw_client.get_redemption_time(code=code, request_options=request_options)
        return _response.data

    def get_character(
        self, *, player_id: PlayerId, request_options: typing.Optional[RequestOptions] = None
    ) -> Character:
        """
        Get information about a player

        Parameters
        ----------
        player_id : PlayerId

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        Character

        Examples
        --------
        from kokos_activator_api import KokosApi
        from kokos_activator_api.environment import KokosApiEnvironment

        client = KokosApi(
            token="YOUR_TOKEN",
            environment=KokosApiEnvironment.PRODUCTION,
        )
        client.redeem.get_character(
            player_id="51709255708",
        )
        """
        _response = self._raw_client.get_character(player_id=player_id, request_options=request_options)
        return _response.data


class AsyncRedeemClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._raw_client = AsyncRawRedeemClient(client_wrapper=client_wrapper)

    @property
    def with_raw_response(self) -> AsyncRawRedeemClient:
        """
        Retrieves a raw implementation of this client that returns raw responses.

        Returns
        -------
        AsyncRawRedeemClient
        """
        return self._raw_client

    async def redeem_code(
        self, *, request: RedeemCodeRequest, request_options: typing.Optional[RequestOptions] = None
    ) -> ActivationReceipt:
        """
        Activate a code

        Parameters
        ----------
        request : RedeemCodeRequest

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        ActivationReceipt

        Examples
        --------
        import asyncio

        from kokos_activator_api import AsyncKokosApi
        from kokos_activator_api.environment import KokosApiEnvironment
        from kokos_activator_api.redeem import RedeemCodeFromDbRequest

        client = AsyncKokosApi(
            token="YOUR_TOKEN",
            environment=KokosApiEnvironment.PRODUCTION,
        )


        async def main() -> None:
            await client.redeem.redeem_code(
                request=RedeemCodeFromDbRequest(
                    require_receipt=True,
                    player_id="51709255708",
                    denomination=660,
                ),
            )


        asyncio.run(main())
        """
        _response = await self._raw_client.redeem_code(request=request, request_options=request_options)
        return _response.data

    async def get_redemption_time(
        self, *, code: Code, request_options: typing.Optional[RequestOptions] = None
    ) -> RedemptionTime:
        """
        Get the redemption time of a code

        Parameters
        ----------
        code : Code
            Code to check

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        RedemptionTime

        Examples
        --------
        import asyncio

        from kokos_activator_api import AsyncKokosApi
        from kokos_activator_api.environment import KokosApiEnvironment

        client = AsyncKokosApi(
            token="YOUR_TOKEN",
            environment=KokosApiEnvironment.PRODUCTION,
        )


        async def main() -> None:
            await client.redeem.get_redemption_time(
                code="r3h4xcJ72f2056g7h7",
            )


        asyncio.run(main())
        """
        _response = await self._raw_client.get_redemption_time(code=code, request_options=request_options)
        return _response.data

    async def get_character(
        self, *, player_id: PlayerId, request_options: typing.Optional[RequestOptions] = None
    ) -> Character:
        """
        Get information about a player

        Parameters
        ----------
        player_id : PlayerId

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        Character

        Examples
        --------
        import asyncio

        from kokos_activator_api import AsyncKokosApi
        from kokos_activator_api.environment import KokosApiEnvironment

        client = AsyncKokosApi(
            token="YOUR_TOKEN",
            environment=KokosApiEnvironment.PRODUCTION,
        )


        async def main() -> None:
            await client.redeem.get_character(
                player_id="51709255708",
            )


        asyncio.run(main())
        """
        _response = await self._raw_client.get_character(player_id=player_id, request_options=request_options)
        return _response.data
