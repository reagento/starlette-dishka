import pytest

from .common import AppProvider, WebSocketAppProvider


@pytest.fixture
def app_provider() -> AppProvider:
    return AppProvider()


@pytest.fixture
def ws_app_provider() -> WebSocketAppProvider:
    return WebSocketAppProvider()
