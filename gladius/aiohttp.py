__all__ = [
    'element_middleware',
    'html_middleware',
    'json_middleware',
    'aiohttp_middlewares',
]

import os
from typing import Optional

from aiohttp import web
from aiohttp.web import middleware
from .element import Element
from .gladius import Gladius


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


"""
def make_app(
    root_dir: Optional[str]=None,
    static_dirs: list[str]=['static'], middlewares=middlewares,
) -> tuple[Gladius, web.Application, web.RouteTableDef]:
    g = Gladius()
    app = web.Application(middlewares=middlewares)
    routes = web.RouteTableDef()

    # @routes.get('/{tail:.*}')
    # async def index(request):
    #     el = app_page
    #     return el.render()

    # static
    if root_dir is None:
        root_dir = os.path.split(__file__)[0]

    for n in static_dirs:
        routes.static(f'/{n}', os.path.join(root_dir, n))

    return g, app, routes
"""

"""
def make_app(
    root_dir: Optional[str]=None,
    static_dirs: list[str]=['static'],
    middlewares=middlewares,
) -> tuple[Gladius, web.Application]:
    g = Gladius()
    app = web.Application(middlewares=middlewares)

    # static
    if root_dir is None:
        root_dir = os.path.split(__file__)[0]

    for n in static_dirs:
        app.router.static(f'/{n}', os.path.join(root_dir, n))

    return g, app
"""
