__all__ = [
    'element_middleware',
    'html_middleware',
    'json_middleware',
    'aiohttp_middlewares',
    'run_app',
]

from aiohttp import web
from aiohttp.web import middleware
from .element import Element


@middleware
async def element_middleware(request, handler):
    resp = await handler(request)

    if isinstance(resp, Element):
        text: str = resp.render()
        headers = {'content-type': 'text/html'}
        resp = web.Response(status=200, text=text, headers=headers)

    return resp


@middleware
async def html_middleware(request, handler):
    resp = await handler(request)

    if isinstance(resp, str):
        headers = {'content-type': 'text/html'}
        resp = web.Response(status=200, text=resp, headers=headers)

    return resp


@middleware
async def json_middleware(request, handler):
    resp = await handler(request)

    if isinstance(resp, (list, dict)):
        resp = web.json_response(resp)

    return resp


aiohttp_middlewares = [
    element_middleware,
    html_middleware,
    json_middleware,
]


def run_app(*args, **kwargs):
    web.run_app(*args, **kwargs)
