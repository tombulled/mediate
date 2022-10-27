from dataclasses import dataclass
from typing import Callable, Generic

from .protocols import MiddlewareCallable
from .typing import PS, RT


@dataclass
class PartialMiddlewareCallable(Generic[PS, RT]):
    middleware: MiddlewareCallable[PS, RT]
    call_next: Callable[PS, RT]

    def __call__(self, *args: PS.args, **kwargs: PS.kwargs) -> RT:
        return self.middleware(self.call_next, *args, **kwargs)
