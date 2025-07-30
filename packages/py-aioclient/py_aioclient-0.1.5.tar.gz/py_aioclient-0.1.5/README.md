# Async Request

[](https://pypi.org/project/py-aioclient/)
[](https://opensource.org/licenses/MIT)

A lightweight and robust Python library for asynchronous HTTP requests, featuring a high-level API for simple and batch calls, plus a client class for advanced control. Built on top of `aiohttp` and `asyncio`.

## Key Features

  * ** Dual API**: Use simple, direct functions (`request`, `batch_requests`) for common tasks, or leverage the `PyAioClient` class with a context manager (`async with`) for full control over the session, cookies, and connections.
  * ** Concurrency Control**: Efficiently run hundreds of batch requests with a customizable concurrency limit to avoid server overload.
  * ** Flexible Returns**: Specify exactly which response attributes you want (`status`, `json`, `text`, `headers`, etc.), optimizing memory usage and code clarity.
  * ** Safe and Robust**: Context manager support ensures that connection sessions are always closed correctly, preventing resource leaks.
  * ** Fully Typed**: 100% type-hinted codebase for a better development experience with IDEs and static analysis tools.

## Installation

Install the package directly from PyPI:

```bash
pip install py-aioclient
```

## Usage

The library offers two primary ways of usage: high-level functions for convenience and a client class for advanced control.

### 1\. High-Level Functions (Standard Usage)

This is the easiest and recommended way for most use cases.

#### Simple Request (`request`)

To make a single `GET` call to fetch a specific post and get its title.

```python
import asyncio
from py_aioclient import request

async def main():
    # Fetches the post with ID = 1 and asks for the JSON response body
    post_data = await request(
        url="https://jsonplaceholder.typicode.com/posts/1",
        method="get",
        return_attrs=["json"]
    )
    
    print(f"Post Title: {post_data.get('title')}")

asyncio.run(main())
```

#### Batch Requests (`batch_requests`)

Run multiple requests concurrently to fetch several posts simultaneously.

```python
import asyncio
from py_aioclient import batch_requests

async def main():
    # Defines the requests to fetch posts 1 through 5
    tasks_params = [
        {
            'url': f'https://jsonplaceholder.typicode.com/posts/{i}',
            'return_attrs': ['json']
        }
        for i in range(1, 6)
    ]

    # Executes all tasks with a concurrency limit of 10
    list_of_posts = await batch_requests(
        requests_params=tasks_params,
        limit=10
    )

    print("Posts found:")
    for post in list_of_posts:
        # Prints the ID and title of each received post
        print(f"  - ID {post.get('id')}: {post.get('title')}")

asyncio.run(main())
```

### 2\. Advanced Usage with the `PyAioClient` Class

Use the `PyAioClient` class directly when you need more control, such as sharing a session, cookies, or headers across multiple calls.

```python
import asyncio
from py_aioclient import PyAioClient

async def main():
    # Shared headers and cookies for all requests in this session
    headers = {"X-Client-ID": "my-app-123"}
    cookies = {"session_id": "abc-xyz"}

    async with PyAioClient(cookies=cookies) as client:
        # First call using the session to fetch a user
        user = await client.client(
            url="https://jsonplaceholder.typicode.com/users/1",
            headers=headers,
            return_attrs=['json']
        )
        print(f"User's name: {user.get('name')}")

        # Second call, in the same session, re-using the connection
        albums = await client.client(
            url=f"https://jsonplaceholder.typicode.com/users/1/albums",
            headers=headers,
            return_attrs=['json']
        )
        print(f"{user.get('name')} has {len(albums)} albums.")

asyncio.run(main())
```

-----

## Practical Example: Querying Addresses with the ViaCEP API

This example demonstrates a real-world use case: concurrently querying multiple Brazilian postal codes (CEPs) from the free and public ViaCEP API and formatting the results.

```python
import asyncio
from py_aioclient import batch_requests

async def fetch_addresses():
    # A list of Brazilian postal codes to query
    ceps_to_query = [
        "01001-000",  # Praça da Sé, São Paulo
        "20040-004",  # Av. Rio Branco, Rio de Janeiro
        "60810-050",  # Av. Washington Soares, Fortaleza
        "99999-999"   # Invalid CEP to test error handling
    ]

    print(f"Querying {len(ceps_to_query)} postal codes...")

    # Create the list of parameters for the batch function
    tasks = [
        {
            'url': f'https://viacep.com.br/ws/{cep}/json/',
            'return_attrs': ['json']
        }
        for cep in ceps_to_query
    ]

    # Execute the batch query
    results = await batch_requests(requests_params=tasks, limit=4)

    print("\n--- Addresses Found ---")
    for cep, data in zip(ceps_to_query, results):
        # The ViaCEP API returns a JSON with the key 'erro' for unfound CEPs
        if data.get('erro'):
            print(f"CEP {cep}: Not found.")
        else:
            # The API returns keys in Portuguese
            address = (
                f"{data.get('logradouro', '')}, "
                f"{data.get('bairro', '')} - "
                f"{data.get('localidade', '')}/{data.get('uf', '')}"
            )
            print(f"CEP {cep}: {address}")

asyncio.run(fetch_addresses())
```

## API Reference

### High-Level Functions

  * **`request(url, method='get', return_attrs=None, **kwargs)`**: For single requests.
  * **`batch_requests(requests_params, limit=10, common_return_attrs=None)`**: For batch requests.

### `PyAioClient` Class

  * **`PyAioClient(limit_connector=0, cookies=None)`**: The class constructor.
  * **`async client(method='get', return_attrs=None, **kwargs)`**: The main method for making requests within an `async with` block.
  * **`async limiter(limit, tasks)`**: Executes awaitable tasks with a concurrency limit.

For more details on parameters, please refer to the docstrings in the source code.

## License

This project is licensed under the MIT License.