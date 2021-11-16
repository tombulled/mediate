import functools

import registrate

class Middleware(registrate.Record):
    def compose(self, func):
        call_next = func

        for middleware in self:
            call_next = functools.partial(middleware, call_next)

        return call_next

    def bind(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return self.compose(func)(*args, **kwargs)

        return wrapper
