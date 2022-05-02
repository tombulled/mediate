import functools
from typing import Any, Callable

import registrate

from . import utils


class Middleware(registrate.Record):
    def compose(self, func: Callable) -> Callable:
        call_next: Callable = func

        for middleware in self:
            call_next = functools.partial(middleware, call_next)

        return call_next

    def bind(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return self.compose(func)(*args, **kwargs)

        return wrapper

    def call(self, argument: Any, /) -> Any:
        return self.compose(utils.identity)(argument)
