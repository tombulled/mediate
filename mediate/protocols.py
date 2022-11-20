from typing import Callable, Protocol, Sequence

from .typing import In, Out

__all__: Sequence[str] = ("MiddlewareCallable",)


class MiddlewareCallable(Protocol[In, Out]):
    def __call__(self, call_next: Callable[[In], Out], in_: In, /) -> Out:
        ...
