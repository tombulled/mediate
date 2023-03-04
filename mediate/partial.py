from dataclasses import dataclass
from typing import Generic, Sequence

from .protocols import Function, MiddlewareCallable
from .typing import In, Out

__all__: Sequence[str] = ("PartialMiddlewareCallable",)


@dataclass
class PartialMiddlewareCallable(Generic[In, Out]):
    middleware: MiddlewareCallable[In, Out]
    call_next: Function[In, Out]

    def __call__(self, in_: In, /) -> Out:
        return self.middleware(self.call_next, in_)
