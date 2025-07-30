from .client import PyAioClient
from typing import Any, Awaitable


async def request(
    url: str,
    method: str = 'get',
    ssl_verify: str | None = None,
    limit_connector: int | None = None,
    cookies: dict[str, Any] | None = None,
    return_attrs: list[str] | None = None,
    **kwargs: Any
) -> Any:
    """Executes a single asynchronous HTTP request.

    A high-level wrapper for making a single request. It automatically
    manages the client session, making it ideal for one-off calls.

    Args:
        url: The target URL for the request.
        method: The HTTP method, e.g., 'get' or 'post'.
        ssl_verify: Path to a CA bundle file for SSL verification.
        limit_connector: The total number of simultaneous connections.
        cookies: A dictionary of cookies to include in the request.
        return_attrs: A list of response attributes to return.
            If None, defaults to `['status']`.
        **kwargs: Additional arguments for the request, such as `params`,
            `json`, `data`, `headers`, or `timeout`.

    Returns:
        The requested attribute(s) from the response. The type depends
        on the `return_attrs` list.
    """

    async with PyAioClient(
        ssl_verify=ssl_verify,
        limit_connector=limit_connector or 0,
        cookies=cookies or {}
    ) as client:
        return await client.client(
            url=url,
            method=method,
            return_attrs=return_attrs,
            **kwargs
        )


async def batch_requests(
    requests_params: list[dict[str, Any]],
    limit: int = 10,
    ssl_verify: str | None = None,
    limit_connector: int | None = None,
    cookies: dict[str, Any] | None = None,
    common_return_attrs: list[str] | None = None
) -> list[Any]:
    """Executes multiple asynchronous HTTP requests concurrently.

    Designed for high-throughput, this function runs a batch of requests
    with a concurrency limit to avoid overwhelming the server. It uses a
    single client session for all requests.

    Args:
        requests_params: A list of dicts, where each dict contains the
            parameters for a single request (e.g., `{'url': '...'}`).
        limit: The maximum number of concurrent requests.
        ssl_verify: Path to a CA bundle file for SSL verification.
        limit_connector: The total number of simultaneous connections for
            the session.
        cookies: A dictionary of cookies to share across all requests.
        common_return_attrs: Default `return_attrs` for all requests.
            Can be overridden by a `return_attrs` key within an
            individual request's parameter dict.

    Returns:
        A list with the results for each request, in the same order
        as the input `requests_params`.
    """

    async with PyAioClient(
        ssl_verify=ssl_verify,
        limit_connector=limit_connector or 0,
        cookies=cookies or {}
    ) as client:

        tasks: list[Awaitable[Any]] = []
        for params in requests_params:
            # Set the return attributes for the task, using the common
            # one as a fallback.
            params['return_attrs'] = params.get(
                'return_attrs', common_return_attrs
            )
            tasks.append(client.client(**params))

        return await client.limiter(limit=limit, tasks=tasks)
