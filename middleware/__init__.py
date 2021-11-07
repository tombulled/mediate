import collections
import dataclasses
import functools
import queue
import typing

# MiddlewareCallable = typing.Callable[[typing.Callable, ...], typing.Any]

# Note: import and use 'register'?
# Note: Offload LIFO, FIFO nonsense to 'register'?
@dataclasses.dataclass
class Middleware:
    middleware: typing.Deque[typing.Callable] = dataclasses.field(default_factory = collections.deque)

    def add(self, func):
        self.middleware.append(func)

    def __call__(self, func):
        self.add(func)

        return func

    # TODO: Find better name
    def reduce(self, func):
        call_next = func

        for middleware in self.middleware:
            call_next = functools.partial(middleware, call_next)

        return call_next

    def bind(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return self.reduce(func)(*args, **kwargs)

        return wrapper
