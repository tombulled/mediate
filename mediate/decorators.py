from typing import Sequence

from roster import Record

from .middleware import Middleware
from .protocols import Decorator, Function, MiddlewareCallable
from .typing import In, Out

__all__: Sequence[str] = ("middleware",)


def middleware(
    *middlewares: MiddlewareCallable[In, Out]
) -> Decorator[Function[In, Out]]:
    def decorate(callable: Function[In, Out], /) -> Function[In, Out]:
        middleware: Middleware[In, Out] = Middleware(record=Record(middlewares))

        return middleware.compose(callable)

    return decorate
