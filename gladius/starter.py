__all__ = [
    'make_mpy_pico',
    'create_aiohttp_app',
]

from typing import Optional, Union
from tempfile import TemporaryDirectory

from aiohttp import web
from nodejs_wheel import npm

from .element import Element
from .gladius import Gladius
from .aiohttp import make_app
from .util import make_page, install_npm_package, compile_npm_package


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
    npm_packages: dict[str, dict]={},
) -> tuple[Gladius, Element, web.Application]:
    with TemporaryDirectory() as build_dir:
        print(f'{build_dir=}')
        p = npm(['init', '-y'], cwd=build_dir, return_completed_process=True)
        print(f'create_aiohttp_app {p=}')

        install_npm_package(build_dir, 'esbuild', {'version': '*'})

        for pkg_name, pkg_info in npm_packages.items():
            install_npm_package(build_dir, pkg_name, pkg_info)

        for pkg_name, pkg_info in npm_packages.items():
            r = compile_npm_package(build_dir, pkg_name, pkg_info)
            print(f'{r=}')

    return None, None, None
