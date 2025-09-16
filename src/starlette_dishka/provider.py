from dishka import Provider, Scope, from_context
from starlette.requests import Request
from starlette.websockets import WebSocket


class StarletteProvider(Provider):
    request = from_context(Request, scope=Scope.REQUEST)
    websocket = from_context(WebSocket, scope=Scope.SESSION)
