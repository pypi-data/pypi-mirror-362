# This file was auto-generated from our API Definition.

import datetime as dt
import typing

from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ..core.request_options import RequestOptions
from ..redeem.types.full_receipt_or_error import FullReceiptOrError
from .raw_client import AsyncRawHistoryClient, RawHistoryClient
from .types.get_activation_history_response import GetActivationHistoryResponse
from .types.stats_response import StatsResponse


class HistoryClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._raw_client = RawHistoryClient(client_wrapper=client_wrapper)

    @property
    def with_raw_response(self) -> RawHistoryClient:
        """
        Retrieves a raw implementation of this client that returns raw responses.

        Returns
        -------
        RawHistoryClient
        """
        return self._raw_client

    def get_stats(
        self, *, date: typing.Optional[dt.date] = None, request_options: typing.Optional[RequestOptions] = None
    ) -> StatsResponse:
        """
        Get statistics about the number of redemptions for each pack on a given date. `0` in the `activations` field means that the activation was successful, but was performed with `codeOverride` and `requireReceipt` set to `false`, and so the amount is unknown. `0` in the `errors` field means that the activation was unsuccessful, and the amount is unknown.

        Parameters
        ----------
        date : typing.Optional[dt.date]
            The date to get statistics for. Defaults to the current date.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        StatsResponse

        Examples
        --------
        import datetime

        from kokos_activator_api import KokosApi
        from kokos_activator_api.environment import KokosApiEnvironment

        client = KokosApi(
            token="YOUR_TOKEN",
            environment=KokosApiEnvironment.PRODUCTION,
        )
        client.history.get_stats(
            date=datetime.date.fromisoformat(
                "2025-05-12",
            ),
        )
        """
        _response = self._raw_client.get_stats(date=date, request_options=request_options)
        return _response.data

    def get_activation_history(
        self,
        *,
        before: typing.Optional[dt.datetime] = None,
        after: typing.Optional[dt.datetime] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> GetActivationHistoryResponse:
        """
        Get the list of recent activations

        Parameters
        ----------
        before : typing.Optional[dt.datetime]
            Get activations before this timestamp (sorted newest first)

        after : typing.Optional[dt.datetime]
            Get activations after this timestamp (sorted oldest first)

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        GetActivationHistoryResponse

        Examples
        --------
        from kokos_activator_api import KokosApi
        from kokos_activator_api.environment import KokosApiEnvironment

        client = KokosApi(
            token="YOUR_TOKEN",
            environment=KokosApiEnvironment.PRODUCTION,
        )
        client.history.get_activation_history()
        """
        _response = self._raw_client.get_activation_history(before=before, after=after, request_options=request_options)
        return _response.data

    def get_receipt(self, id: int, *, request_options: typing.Optional[RequestOptions] = None) -> FullReceiptOrError:
        """
        Get the full receipt for an existing activation

        Parameters
        ----------
        id : int
            Activation ID

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        FullReceiptOrError

        Examples
        --------
        from kokos_activator_api import KokosApi
        from kokos_activator_api.environment import KokosApiEnvironment

        client = KokosApi(
            token="YOUR_TOKEN",
            environment=KokosApiEnvironment.PRODUCTION,
        )
        client.history.get_receipt(
            id=100407,
        )
        """
        _response = self._raw_client.get_receipt(id, request_options=request_options)
        return _response.data


class AsyncHistoryClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._raw_client = AsyncRawHistoryClient(client_wrapper=client_wrapper)

    @property
    def with_raw_response(self) -> AsyncRawHistoryClient:
        """
        Retrieves a raw implementation of this client that returns raw responses.

        Returns
        -------
        AsyncRawHistoryClient
        """
        return self._raw_client

    async def get_stats(
        self, *, date: typing.Optional[dt.date] = None, request_options: typing.Optional[RequestOptions] = None
    ) -> StatsResponse:
        """
        Get statistics about the number of redemptions for each pack on a given date. `0` in the `activations` field means that the activation was successful, but was performed with `codeOverride` and `requireReceipt` set to `false`, and so the amount is unknown. `0` in the `errors` field means that the activation was unsuccessful, and the amount is unknown.

        Parameters
        ----------
        date : typing.Optional[dt.date]
            The date to get statistics for. Defaults to the current date.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        StatsResponse

        Examples
        --------
        import asyncio
        import datetime

        from kokos_activator_api import AsyncKokosApi
        from kokos_activator_api.environment import KokosApiEnvironment

        client = AsyncKokosApi(
            token="YOUR_TOKEN",
            environment=KokosApiEnvironment.PRODUCTION,
        )


        async def main() -> None:
            await client.history.get_stats(
                date=datetime.date.fromisoformat(
                    "2025-05-12",
                ),
            )


        asyncio.run(main())
        """
        _response = await self._raw_client.get_stats(date=date, request_options=request_options)
        return _response.data

    async def get_activation_history(
        self,
        *,
        before: typing.Optional[dt.datetime] = None,
        after: typing.Optional[dt.datetime] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> GetActivationHistoryResponse:
        """
        Get the list of recent activations

        Parameters
        ----------
        before : typing.Optional[dt.datetime]
            Get activations before this timestamp (sorted newest first)

        after : typing.Optional[dt.datetime]
            Get activations after this timestamp (sorted oldest first)

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        GetActivationHistoryResponse

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
            await client.history.get_activation_history()


        asyncio.run(main())
        """
        _response = await self._raw_client.get_activation_history(
            before=before, after=after, request_options=request_options
        )
        return _response.data

    async def get_receipt(
        self, id: int, *, request_options: typing.Optional[RequestOptions] = None
    ) -> FullReceiptOrError:
        """
        Get the full receipt for an existing activation

        Parameters
        ----------
        id : int
            Activation ID

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        FullReceiptOrError

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
            await client.history.get_receipt(
                id=100407,
            )


        asyncio.run(main())
        """
        _response = await self._raw_client.get_receipt(id, request_options=request_options)
        return _response.data
