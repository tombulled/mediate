from dataclasses import dataclass, field
from functools import wraps
from typing import Callable, Generic

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
        return self.record(middleware)

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
