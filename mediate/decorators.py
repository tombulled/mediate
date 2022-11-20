from typing import Callable, Sequence

from roster import Record

from .middleware import Middleware
from .typing import In, Out

__all__: Sequence[str] = ("middleware",)


def middleware(
    *middlewares: Callable[[Callable[[In], Out], In], Out]
) -> Callable[[Callable[[In], Out]], Callable[[In], Out]]:
    def decorate(callable: Callable[[In], Out], /) -> Callable[[In], Out]:
        middleware: Middleware[In, Out] = Middleware(record=Record(middlewares))

        return middleware.compose(callable)

    return decorate
