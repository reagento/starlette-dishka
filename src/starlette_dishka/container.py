from dishka import Scope
from starlette.requests import Request
from starlette.types import (
    ASGIApp,
    Receive,
    Scope as StarletteScope,
    Send,
)
from starlette.websockets import WebSocket


class ContainerMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(
        self,
        scope: StarletteScope,
        receive: Receive,
        send: Send,
    ) -> None:
        scope_type = scope["type"]
        request: Request | WebSocket
        context: dict[type[Request | WebSocket], Request | WebSocket]

        if scope_type == "http":
            request = Request(scope, receive, send)
            context = {Request: request}
            di_scope = Scope.REQUEST
        elif scope_type == "websocket":
            request = WebSocket(scope, receive, send)
            context = {WebSocket: request}
            di_scope = Scope.SESSION
        else:
            return await self.app(scope, receive, send)

        async with request.app.state.dishka_container(
            context,
            scope=di_scope,
        ) as request_container:
            request.state.dishka_container = request_container
            return await self.app(scope, receive, send)


class SyncContainerMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(
        self,
        scope: StarletteScope,
        receive: Receive,
        send: Send,
    ) -> None:
        scope_type = scope["type"]
        request: Request | WebSocket
        context: dict[type[Request | WebSocket], Request | WebSocket]

        if scope_type == "http":
            request = Request(scope, receive, send)
            context = {Request: request}
            di_scope = Scope.REQUEST
        elif scope_type == "websocket":
            request = WebSocket(scope, receive, send)
            context = {WebSocket: request}
            di_scope = Scope.SESSION
        else:
            return await self.app(scope, receive, send)

        with request.app.state.dishka_container(
            context,
            scope=di_scope,
        ) as request_container:
            request.state.dishka_container = request_container
            return await self.app(scope, receive, send)
