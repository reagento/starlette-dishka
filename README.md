# Starlette integration for Dishka

[![PyPI version](https://badge.fury.io/py/starlette-dishka.svg)](https://pypi.python.org/pypi/starlette-dishka)
[![Supported versions](https://img.shields.io/pypi/pyversions/starlette-dishka.svg)](https://pypi.python.org/pypi/starlette-dishka)
[![Downloads](https://img.shields.io/pypi/dm/starlette-dishka.svg)](https://pypistats.org/packages/starlette-dishka)
[![License](https://img.shields.io/github/license/reagento/starlette-dishka)](https://github.com/reagento/starlette-dishka/blob/main/LICENSE)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/reagento/starlette-dishka/setup.yml)](https://github.com/reagento/starlette-dishka/actions)
[![Telegram](https://img.shields.io/badge/💬-Telegram-blue)](https://t.me/reagento_ru)

This package provides integration of [Dishka](http://github.com/reagento/dishka/) dependency injection framework and [Starlette](https://github.com/encode/starlette), a lightweight ASGI framework.

## Installation

```sh
pip install starlette-dishka
```

## Features

* automatic *REQUEST* and *SESSION* scope management using middleware
* passing ``Request`` object as a context data to providers for both **Websockets** and **HTTP** requests
* automatic injection of dependencies into handler function.

## How to use

1. Import
```python
from starlette_dishka import (
    FromDishka,
    StarletteProvider,
    inject,
    setup_dishka,
)
from dishka import make_async_container, Provider, provide, Scope
```

2. Create provider. You can use ``starlette.requests.Request`` as a factory parameter to access on *REQUEST-scope*, and ``starlette.websockets.WebSocket`` on *SESSION*-scope

```python
class YourProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def create_x(self, request: Request) -> X:
         ...
```

3. Mark those of your handlers parameters which are to be injected with ``FromDishka[]`` and decorate them using ``@inject``

```python
@inject
async def endpoint(
    request: Request,
    *,
    gateway: FromDishka[Gateway],
) -> ResponseModel:
    ...
```

4. *(optional)* Use ``StarletteProvider()`` when creating container if you are going to use ``starlette.Request`` or ``starlette.WebSocket`` in providers

```python
container = make_async_container(YourProvider(), StarletteProvider())
```

5. Setup ``dishka`` integration.

```python
setup_dishka(container=container, app=app)
```

## Websockets

In starlette your view function is called once per connection and then you retrieve messages in loop.
So, ``inject`` decorator can be only used to retrieve *SESSION*-scoped objects.
To achieve *REQUEST*-scope you can enter in manually:

```python
@inject
async def get_with_request(
    websocket: WebSocket,
    a: FromDishka[A],  # object with Scope.SESSION
    container: FromDishka[AsyncContainer],  # container for Scope.SESSION
) -> None:
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # enter the nested scope, which is Scope.REQUEST
        async with container() as request_container:
            b = await request_container.get(B)  # object with Scope.REQUEST
```
