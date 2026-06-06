<div align="center">
    
# Starlette integration for Dishka

<a href="https://pypi.org/project/starlette-dishka"><img alt="Python version" src="https://shieldcn.dev/pypi/starlette-dishka.svg?variant=branded&font=geist-mono&size=xs"></a>
<a href="https://pypi.org/project/starlette-dishka"><img alt="Python version" src="https://shieldcn.dev/pypi/python/starlette-dishka.svg?variant=branded&font=geist-mono&size=xs"></a>
<a href="https://pypi.org/project/starlette-dishka"><img alt="Monthly downloads" src="https://shieldcn.dev/pypi/dm/starlette-dishka.svg?variant=branded&font=geist-mono&size=xs"></a>

<a href="https://github.com/reagento/starlette-dishka/actions?query=branch%3Amain"><picture><source media="(prefers-color-scheme: dark)" srcset="https://shieldcn.dev/github/ci/reagento/starlette-dishka.svg?variant=outline&font=geist-mono&size=xs&animate=pulse&mode=dark"><img alt="CI" src="https://shieldcn.dev/github/ci/reagento/starlette-dishka.svg?variant=outline&font=geist-mono&size=xs&animate=pulse&mode=light"></picture></a>
<a href="https://github.com/reagento/starlette-dishka/blob/main/LICENSE"><picture><source media="(prefers-color-scheme: dark)" srcset="https://shieldcn.dev/github/reagento/starlette-dishka/license.svg?variant=outline&font=geist-mono&size=xs&mode=dark"><img alt="License" src="https://shieldcn.dev/github/reagento/starlette-dishka/license.svg?variant=outline&font=geist-mono&size=xs&mode=light"></picture></a>
<a href="https://t.me/reagento_ru"><picture><source media="(prefers-color-scheme: dark)" srcset="https://shieldcn.dev/badge/dynamic/json.svg?url=https%3A%2F%2Ftg.chirizxc.workers.dev%2Freagento_ru&query=%24.members&suffix=+members&variant=outline&size=xs&mode=dark&logo=telegram&logoColor=24A1DE&label=Telegram"/><img alt="Telegram members" src="https://shieldcn.dev/badge/dynamic/json.svg?url=https%3A%2F%2Ftg.chirizxc.workers.dev%2Freagento_ru&query=%24.members&suffix=+members&variant=outline&size=xs&mode=light&logo=telegram&logoColor=24A1DE&label=Telegram"/></picture></a>

</div>

This package provides integration of [Dishka](http://github.com/reagento/dishka/) dependency injection framework and [Starlette](https://github.com/encode/starlette), a lightweight ASGI framework.

## Installation

Via [pip](https://github.com/pypa/pip):

```bash
pip install toml-rs
```

Via [uv](https://github.com/astral-sh/uv):

```bash
uv pip install toml-rs
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
