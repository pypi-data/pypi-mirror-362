# This file was auto-generated from our API Definition.

import typing

import httpx
from .core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from .database.client import AsyncDatabaseClient, DatabaseClient
from .environment import KokosApiEnvironment
from .history.client import AsyncHistoryClient, HistoryClient
from .redeem.client import AsyncRedeemClient, RedeemClient


class KokosApi:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : typing.Optional[KokosApiEnvironment]
        The environment to use for requests from the client.

    token : typing.Union[str, typing.Callable[[], str]]
    headers : typing.Optional[typing.Dict[str, str]]
        Additional headers to send with every request.

    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 60 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.Client]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from kokos_activator_api import KokosApi
    from kokos_activator_api.environment import KokosApiEnvironment

    client = KokosApi(
        token="YOUR_TOKEN",
        environment=KokosApiEnvironment.PRODUCTION,
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: typing.Optional[KokosApiEnvironment] = None,
        token: typing.Union[str, typing.Callable[[], str]],
        headers: typing.Optional[typing.Dict[str, str]] = None,
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.Client] = None,
    ):
        _defaulted_timeout = (
            timeout if timeout is not None else 60 if httpx_client is None else httpx_client.timeout.read
        )
        self._client_wrapper = SyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            token=token,
            headers=headers,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.Client(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.Client(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )
        self.database = DatabaseClient(client_wrapper=self._client_wrapper)
        self.history = HistoryClient(client_wrapper=self._client_wrapper)
        self.redeem = RedeemClient(client_wrapper=self._client_wrapper)


class AsyncKokosApi:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : typing.Optional[KokosApiEnvironment]
        The environment to use for requests from the client.

    token : typing.Union[str, typing.Callable[[], str]]
    headers : typing.Optional[typing.Dict[str, str]]
        Additional headers to send with every request.

    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 60 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.AsyncClient]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from kokos_activator_api import AsyncKokosApi
    from kokos_activator_api.environment import KokosApiEnvironment

    client = AsyncKokosApi(
        token="YOUR_TOKEN",
        environment=KokosApiEnvironment.PRODUCTION,
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: typing.Optional[KokosApiEnvironment] = None,
        token: typing.Union[str, typing.Callable[[], str]],
        headers: typing.Optional[typing.Dict[str, str]] = None,
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
    ):
        _defaulted_timeout = (
            timeout if timeout is not None else 60 if httpx_client is None else httpx_client.timeout.read
        )
        self._client_wrapper = AsyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            token=token,
            headers=headers,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )
        self.database = AsyncDatabaseClient(client_wrapper=self._client_wrapper)
        self.history = AsyncHistoryClient(client_wrapper=self._client_wrapper)
        self.redeem = AsyncRedeemClient(client_wrapper=self._client_wrapper)


def _get_base_url(
    *, base_url: typing.Optional[str] = None, environment: typing.Optional[KokosApiEnvironment] = None
) -> str:
    if base_url is not None:
        return base_url
    elif environment is not None:
        return environment.value
    else:
        raise Exception("Please pass in either base_url or environment to construct the client")
