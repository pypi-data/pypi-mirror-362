# Kokos Python Library

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com?utm_source=github&utm_medium=github&utm_campaign=readme&utm_source=Kokos%2FPython)
[![pypi](https://img.shields.io/pypi/v/kokos_activator_api)](https://pypi.python.org/pypi/kokos_activator_api)

The Kokos Python library provides convenient access to the Kokos API from Python.

## Installation

```sh
pip install kokos_activator_api
```

## Reference

A full reference for this library is available [here](./reference.md).

## Usage

Instantiate and use the client with the following:

```python
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
```

## Async Client

The SDK also exports an `async` client so that you can make non-blocking calls to our API.

```python
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
```

## Exception Handling

When the API returns a non-success status code (4xx or 5xx response), a subclass of the following error
will be thrown.

```python
from kokos_activator_api.core.api_error import ApiError

try:
    client.database.upload_codes(...)
except ApiError as e:
    print(e.status_code)
    print(e.body)
```

## Advanced

### Access Raw Response Data

The SDK provides access to raw response data, including headers, through the `.with_raw_response` property.
The `.with_raw_response` property returns a "raw" client that can be used to access the `.headers` and `.data` attributes.

```python
from kokos_activator_api import KokosApi

client = KokosApi(
    ...,
)
response = client.database.with_raw_response.upload_codes(...)
print(response.headers)  # access the response headers
print(response.data)  # access the underlying object
```

### Retries

The SDK is instrumented with automatic retries with exponential backoff. A request will be retried as long
as the request is deemed retryable and the number of retry attempts has not grown larger than the configured
retry limit (default: 2).

A request is deemed retryable when any of the following HTTP status codes is returned:

- [408](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/408) (Timeout)
- [429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) (Too Many Requests)
- [5XX](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500) (Internal Server Errors)

Use the `max_retries` request option to configure this behavior.

```python
client.database.upload_codes(..., request_options={
    "max_retries": 1
})
```

### Timeouts

The SDK defaults to a 60 second timeout. You can configure this with a timeout option at the client or request level.

```python

from kokos_activator_api import KokosApi

client = KokosApi(
    ...,
    timeout=20.0,
)


# Override timeout for a specific method
client.database.upload_codes(..., request_options={
    "timeout_in_seconds": 1
})
```

### Custom Client

You can override the `httpx` client to customize it for your use-case. Some common use-cases include support for proxies
and transports.

```python
import httpx
from kokos_activator_api import KokosApi

client = KokosApi(
    ...,
    httpx_client=httpx.Client(
        proxies="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically.
Additions made directly to this library would have to be moved over to our generation code,
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as
a proof of concept, but know that we will not be able to merge it as-is. We suggest opening
an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
