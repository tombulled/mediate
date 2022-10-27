from typing import Callable, Protocol

from .typing import PS, RT


class MiddlewareCallable(Protocol[PS, RT]):
    def __call__(
        self, call_next: Callable[PS, RT], /, *args: PS.args, **kwargs: PS.kwargs
    ) -> RT:
        ...
