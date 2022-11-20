from dataclasses import dataclass, field
from functools import wraps
from typing import Callable, Generic, Sequence, SupportsIndex

from roster import Record

from .partial import PartialMiddlewareCallable
from .protocols import MiddlewareCallable
from .typing import In, Out

__all__: Sequence[str] = ("Middleware",)


@dataclass
class Middleware(Generic[In, Out]):
    record: Record[MiddlewareCallable[In, Out]] = field(default_factory=Record)

    def __call__(
        self, middleware: MiddlewareCallable[In, Out], /
    ) -> MiddlewareCallable[In, Out]:
        self.add(middleware)

        return middleware

    def add(self, middleware: MiddlewareCallable[In, Out], /) -> None:
        if middleware not in self.record:
            self.record.record(middleware)

    def remove(self, middleware: MiddlewareCallable[In, Out], /) -> None:
        self.record.remove(middleware)

    def contains(self, middleware: MiddlewareCallable[In, Out], /) -> bool:
        return middleware in self.record

    def insert(self, index: SupportsIndex, middleware: MiddlewareCallable[In, Out], /):
        self.record.insert(index, middleware)

    def compose(self, sinc: Callable[[In], Out], /) -> Callable[[In], Out]:
        call_next: Callable[[In], Out] = sinc

        middleware: MiddlewareCallable[In, Out]
        for middleware in self.record:
            call_next = PartialMiddlewareCallable(middleware, call_next)

        return call_next

    def bind(self, sinc: Callable[[In], Out], /) -> Callable[[In], Out]:
        @wraps(sinc)
        def wrapper(in_: In, /) -> Out:
            return self.compose(sinc)(in_)

        return wrapper
