from pprint import pprint
from typing import Callable

from httpx import Client, Request, Response

from mediate import Middleware

RequestMiddleware = Callable[[Request], Response]

middleware: Middleware[Request, Response] = Middleware()


@middleware
def add_message(call_next: RequestMiddleware, request: Request, /) -> Response:
    request.url = request.url.copy_set_param("message", "Hello, World!")

    return call_next(request)


@middleware
def raise_for_status(call_next: RequestMiddleware, request: Request, /) -> Response:
    response: Response = call_next(request)

    response.raise_for_status()

    return response


@middleware.bind
def send_request(request: Request, /) -> Response:
    return Client().send(request)


response: Response = send_request(Request("GET", "https://httpbin.org/get"))

pprint(response.json())
