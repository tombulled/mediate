from dataclasses import dataclass, field
from functools import wraps
from typing import Callable, Generic, SupportsIndex

from roster import Record

from .partial import PartialMiddlewareCallable
from .protocols import MiddlewareCallable
from .typing import PS, RT


@dataclass
class Middleware(Generic[PS, RT]):
    record: Record[MiddlewareCallable[PS, RT]] = field(default_factory=Record)

    def __call__(
        self, middleware: MiddlewareCallable[PS, RT], /
    ) -> MiddlewareCallable[PS, RT]:
        self.add(middleware)

        return middleware

    def add(self, middleware: MiddlewareCallable[PS, RT], /) -> None:
        if middleware not in self.record:
            self.record.record(middleware)

    def remove(self, middleware: MiddlewareCallable[PS, RT], /) -> None:
        self.record.remove(middleware)

    def contains(self, middleware: MiddlewareCallable[PS, RT], /) -> bool:
        return middleware in self.record

    def insert(self, index: SupportsIndex, middleware: MiddlewareCallable[PS, RT], /):
        self.record.insert(index, middleware)

    def compose(self, sinc: Callable[PS, RT], /) -> Callable[PS, RT]:
        call_next: Callable[PS, RT] = sinc

        middleware: MiddlewareCallable[PS, RT]
        for middleware in self.record:
            call_next = PartialMiddlewareCallable(middleware, call_next)

        return call_next

    def bind(self, sinc: Callable[PS, RT], /) -> Callable[PS, RT]:
        @wraps(sinc)
        def wrapper(*args: PS.args, **kwargs: PS.kwargs):
            return self.compose(sinc)(*args, **kwargs)

        return wrapper
