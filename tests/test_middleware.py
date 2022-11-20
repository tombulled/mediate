from typing import Callable

from typing_extensions import TypeAlias

from mediate import Middleware

Greeter: TypeAlias = Callable[[str], str]

middleware: Middleware[str, str] = Middleware()


@middleware
def shout(call_next: Greeter, /, name: str) -> str:
    return call_next(name.upper())


@middleware
def exclaim(call_next: Greeter, /, name: str) -> str:
    return call_next(name + "!")


def test_compose() -> None:
    def hello(name: str) -> str:
        return f"Hello, {name}"

    composition: Greeter = middleware.compose(hello)

    assert composition("bob") == "Hello, BOB!"


def test_bind() -> None:
    @middleware.bind
    def hello(name: str) -> str:
        return f"Hello, {name}"

    assert hello("bob") == "Hello, BOB!"
