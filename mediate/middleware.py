import functools
from dataclasses import dataclass, field
from typing import Callable, Generic, Protocol, TypeVar

from roster import Record
from typing_extensions import ParamSpec

PS = ParamSpec("PS")
RT = TypeVar("RT")


class MiddlewareCallable(Protocol[PS, RT]):
    def __call__(
        self, call_next: Callable[PS, RT], /, *args: PS.args, **kwargs: PS.kwargs
    ) -> RT:
        ...


@dataclass
class PartialMiddlewareCallable(Generic[PS, RT]):
    middleware: MiddlewareCallable[PS, RT]
    call_next: Callable[PS, RT]

    def __call__(self, *args: PS.args, **kwargs: PS.kwargs) -> RT:
        return self.middleware(self.call_next, *args, **kwargs)


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
        @functools.wraps(sinc)
        def wrapper(*args: PS.args, **kwargs: PS.kwargs):
            return self.compose(sinc)(*args, **kwargs)

        return wrapper
