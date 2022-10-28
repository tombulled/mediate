from typing import Callable

from typing_extensions import TypeAlias

from mediate import middleware

Greeter: TypeAlias = Callable[[str], str]


def shout(call_next: Greeter, name: str, /) -> str:
    return call_next(name.upper())


def exclaim(call_next: Greeter, name: str, /) -> str:
    return call_next(name + "!")


def test_middleware() -> None:
    @middleware(shout, exclaim)
    def hello(name: str, /) -> str:
        return f"Hello, {name}"

    assert hello("sam") == "Hello, SAM!"
