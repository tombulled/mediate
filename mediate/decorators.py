from typing import Callable

from roster import Record
from typing_extensions import Concatenate

from .middleware import Middleware
from .typing import PS, RT


def middleware(
    *middlewares: Callable[Concatenate[Callable[PS, RT], PS], RT]
) -> Callable[[Callable[PS, RT]], Callable[PS, RT]]:
    def decorate(callable: Callable[PS, RT], /) -> Callable[PS, RT]:
        middleware: Middleware[PS, RT] = Middleware(record=Record(middlewares))

        return middleware.compose(callable)

    return decorate
