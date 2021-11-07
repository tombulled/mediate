import dataclasses
import functools
import typing

# MiddlewareCallable = typing.Callable[[typing.Callable, ...], typing.Any]

@dataclasses.dataclass
class Middleware:
    middleware: typing.List[typing.Callable] = dataclasses.field(default_factory = list)

    def __call__(self, func):
        self.middleware.append(func)

        return func

    def bind(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            call_next = func

            for middleware in reversed(self.middleware):
                call_next = functools.partial(middleware, call_next)

            return call_next(*args, **kwargs)

        return wrapper
