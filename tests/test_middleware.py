import pytest
from typing import Callable
from mediate import Middleware


@pytest.fixture
def middleware() -> Middleware:
    middleware: Middleware = Middleware()

    @middleware
    def shout(call_next, name):
        return call_next(name.upper())

    @middleware
    def exclaim(call_next, name):
        return call_next(name + "!")

    return middleware


def test_compose(middleware: Middleware) -> None:
    def hello(name):
        return f"Hello, {name}"

    composition: Callable = middleware.compose(hello)

    assert composition("bob") == "Hello, BOB!"


def test_bind(middleware: Middleware) -> None:
    @middleware.bind
    def hello(name):
        return f"Hello, {name}"

    assert hello("bob") == "Hello, BOB!"


def test_call(middleware: Middleware) -> None:
    assert middleware.call("bob") == "BOB!"
