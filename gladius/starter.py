__all__ = [
    'make_mpy_pico',
    'create_aiohttp_app',
]

from typing import Optional, Union

from aiohttp import web

from .element import Element
from .gladius import Gladius
from .aiohttp import make_app
from .util import make_page


# FIXME: remove
def make_mpy_pico(
    root_dir: str,
    lang: str='en',
    title: str='Gladius',
    description: str='Gladius',
    favicon: str | tuple | list | dict | Element='/static/img/favicon.png',
    links: list[str | tuple | list | dict | Element]=[],
    scripts: list[str | tuple | list | dict | Element]=[],
) -> tuple[Gladius, web.Application, web.RouteTableDef, Element]:
    g, app, routes = make_app(root_dir)

    page = make_page(
        g,
        title=title,
        description=description,
        favicon=favicon,
        links=[
            '/static/pico/pico.min.css',
            '/static/nprogress/nprogress.css',
            '/static/pyscript/core.css',
            *links,
        ],
        scripts=[
            dict(src='/static/nprogress/nprogress.js', defer=None),
            dict(src='/static/pyscript/core.js', type='module', defer=None),
            dict(type='mpy', src='/static/app.py', config='/static/pyscript.toml'),
            *scripts,
        ],
    )

    @routes.get('/{tail:.*}') # type: ignore
    async def index(request):
        return page.render()

    return g, app, routes, page


def create_aiohttp_app(
    root_dir: Optional[str]=None,
    lang: str='en',
    title: str='Gladius',
    description: str='Gladius',
    favicon: str | tuple | list | dict | Element='/static/img/favicon.png',
    links: list[str | tuple | list | dict | Element]=[],
    scripts: list[str | tuple | list | dict | Element]=[],
    npm_packages: dict[str, Union[str, list, dict]]={},
) -> tuple[Gladius, Element, web.Application]:
    pass
