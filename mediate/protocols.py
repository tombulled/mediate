from typing import Protocol, Sequence, TypeVar

from .typing import In, Out

__all__: Sequence[str] = (
    "Decorator",
    "Function",
    "MiddlewareCallable",
)

T = TypeVar("T", contravariant=True)
R = TypeVar("R", covariant=True)
V = TypeVar("V")


class Function(Protocol[T, R]):
    def __call__(self, t: T, /) -> R:
        ...


class Decorator(Protocol[V]):
    def __call__(self, v: V, /) -> V:
        ...


class MiddlewareCallable(Protocol[In, Out]):
    def __call__(self, call_next: Function[In, Out], in_: In, /) -> Out:
        ...
