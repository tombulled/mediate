from dataclasses import dataclass
from typing import Callable, Generic, Sequence

from .protocols import MiddlewareCallable
from .typing import In, Out

__all__: Sequence[str] = ("PartialMiddlewareCallable",)


@dataclass
class PartialMiddlewareCallable(Generic[In, Out]):
    middleware: MiddlewareCallable[In, Out]
    call_next: Callable[[In], Out]

    def __call__(self, in_: In, /) -> Out:
        return self.middleware(self.call_next, in_)
