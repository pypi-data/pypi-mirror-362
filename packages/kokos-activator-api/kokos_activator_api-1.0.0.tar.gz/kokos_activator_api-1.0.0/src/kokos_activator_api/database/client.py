# This file was auto-generated from our API Definition.

import typing

from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.request_options import RequestOptions
from ..redeem.types.code import Code
from ..redeem.types.pack_denomination import PackDenomination
from .raw_client import AsyncRawDatabaseClient, RawDatabaseClient
from .types.database_inventory import DatabaseInventory
from .types.upload_codes_response import UploadCodesResponse
from .types.upload_pack import UploadPack

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class DatabaseClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._raw_client = RawDatabaseClient(client_wrapper=client_wrapper)

    @property
    def with_raw_response(self) -> RawDatabaseClient:
        """
        Retrieves a raw implementation of this client that returns raw responses.

        Returns
        -------
        RawDatabaseClient
        """
        return self._raw_client

    def get_inventory(self, *, request_options: typing.Optional[RequestOptions] = None) -> DatabaseInventory:
        """
        Get the amount of codes in the database for each pack

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        DatabaseInventory

        Examples
        --------
        from kokos_activator_api import KokosApi
        from kokos_activator_api.environment import KokosApiEnvironment

        client = KokosApi(
            token="YOUR_TOKEN",
            environment=KokosApiEnvironment.PRODUCTION,
        )
        client.database.get_inventory()
        """
        _response = self._raw_client.get_inventory(request_options=request_options)
        return _response.data

    def upload_codes(
        self, *, request: typing.Sequence[UploadPack], request_options: typing.Optional[RequestOptions] = None
    ) -> UploadCodesResponse:
        """
        Add codes to the database

        Parameters
        ----------
        request : typing.Sequence[UploadPack]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        UploadCodesResponse

        Examples
        --------
        from kokos_activator_api import KokosApi
        from kokos_activator_api.database import UploadPack
        from kokos_activator_api.environment import KokosApiEnvironment

        client = KokosApi(
            token="YOUR_TOKEN",
            environment=KokosApiEnvironment.PRODUCTION,
        )
        client.database.upload_codes(
            request=[
                UploadPack(
                    denomination=60,
                    codes=[
                        "r3h4x2Jh2W2853g9g4",
                        "Nq7QDWZw2F2eZ4ndZd",
                        "Nq7QDHZA2Q2cZ7rdw3",
                        "Nq7QDYZa2N22Z0r0vc",
                        "Nq7QDDZ72U4738E64c",
                    ],
                )
            ],
        )
        """
        _response = self._raw_client.upload_codes(request=request, request_options=request_options)
        return _response.data

    def download_codes(
        self, *, denomination: PackDenomination, amount: int, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.Set[Code]:
        """
        Extract codes from the database

        Parameters
        ----------
        denomination : PackDenomination

        amount : int
            Amount of codes to extract

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Set[Code]

        Examples
        --------
        from kokos_activator_api import KokosApi
        from kokos_activator_api.environment import KokosApiEnvironment

        client = KokosApi(
            token="YOUR_TOKEN",
            environment=KokosApiEnvironment.PRODUCTION,
        )
        client.database.download_codes(
            denomination=60,
            amount=5,
        )
        """
        _response = self._raw_client.download_codes(
            denomination=denomination, amount=amount, request_options=request_options
        )
        return _response.data


class AsyncDatabaseClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._raw_client = AsyncRawDatabaseClient(client_wrapper=client_wrapper)

    @property
    def with_raw_response(self) -> AsyncRawDatabaseClient:
        """
        Retrieves a raw implementation of this client that returns raw responses.

        Returns
        -------
        AsyncRawDatabaseClient
        """
        return self._raw_client

    async def get_inventory(self, *, request_options: typing.Optional[RequestOptions] = None) -> DatabaseInventory:
        """
        Get the amount of codes in the database for each pack

        Parameters
        ----------
        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        DatabaseInventory

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
            await client.database.get_inventory()


        asyncio.run(main())
        """
        _response = await self._raw_client.get_inventory(request_options=request_options)
        return _response.data

    async def upload_codes(
        self, *, request: typing.Sequence[UploadPack], request_options: typing.Optional[RequestOptions] = None
    ) -> UploadCodesResponse:
        """
        Add codes to the database

        Parameters
        ----------
        request : typing.Sequence[UploadPack]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        UploadCodesResponse

        Examples
        --------
        import asyncio

        from kokos_activator_api import AsyncKokosApi
        from kokos_activator_api.database import UploadPack
        from kokos_activator_api.environment import KokosApiEnvironment

        client = AsyncKokosApi(
            token="YOUR_TOKEN",
            environment=KokosApiEnvironment.PRODUCTION,
        )


        async def main() -> None:
            await client.database.upload_codes(
                request=[
                    UploadPack(
                        denomination=60,
                        codes=[
                            "r3h4x2Jh2W2853g9g4",
                            "Nq7QDWZw2F2eZ4ndZd",
                            "Nq7QDHZA2Q2cZ7rdw3",
                            "Nq7QDYZa2N22Z0r0vc",
                            "Nq7QDDZ72U4738E64c",
                        ],
                    )
                ],
            )


        asyncio.run(main())
        """
        _response = await self._raw_client.upload_codes(request=request, request_options=request_options)
        return _response.data

    async def download_codes(
        self, *, denomination: PackDenomination, amount: int, request_options: typing.Optional[RequestOptions] = None
    ) -> typing.Set[Code]:
        """
        Extract codes from the database

        Parameters
        ----------
        denomination : PackDenomination

        amount : int
            Amount of codes to extract

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.Set[Code]

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
            await client.database.download_codes(
                denomination=60,
                amount=5,
            )


        asyncio.run(main())
        """
        _response = await self._raw_client.download_codes(
            denomination=denomination, amount=amount, request_options=request_options
        )
        return _response.data
