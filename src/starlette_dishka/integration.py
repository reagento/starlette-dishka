from collections.abc import Callable
from typing import ParamSpec, TypeVar

from dishka import AsyncContainer
from dishka.integrations.base import wrap_injection
from starlette.applications import Starlette

from .container import ContainerMiddleware

T = TypeVar("T")
P = ParamSpec("P")


def inject(func: Callable[P, T]) -> Callable[P, T]:
    return wrap_injection(
        func=func,
        is_async=True,
        container_getter=lambda r, _: r[0].scope["state"]["dishka_container"],
    )


def setup_dishka(container: AsyncContainer, app: Starlette) -> None:
    app.add_middleware(ContainerMiddleware)
    app.state.dishka_container = container
