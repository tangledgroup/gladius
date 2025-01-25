__all__ = [
    'create_aiohttp_app',
]

import os
import shutil
from copy import deepcopy
from subprocess import PIPE
from typing import Any, Optional, Union
# from tempfile import TemporaryDirectory

# from tqdm import tqdm
from aiohttp import web
# from nodejs_wheel import npm

from . import gladius
from .element import Element
from .gladius import Gladius
from .aiohttp import aiohttp_middlewares
# from .util import make_page, install_npm_package, compile_npm_package, install_compile_npm_packages
from .util import make_page, install_compile_npm_packages


"""
def create_aiohttp_app(
    root_dir: Optional[str]=None,
    lang: str='en',
    title: str='Gladius',
    description: str='Gladius',
    static_path: str='./static/',
    favicon: str='img/favicon.png',
    links: list[str | dict | Element]=[],
    scripts: list[str | dict | Element]=[],
    npm_packages: dict[str, Union[dict[str, Any], list[str]]]={},
) -> tuple[Gladius, Element, web.Application]:
    g = Gladius()
    app = web.Application(middlewares=aiohttp_middlewares)
    page_links = deepcopy(links)
    page_scripts = deepcopy(scripts)
    dest_paths: list[Union[str, Path]] = []

    with TemporaryDirectory() as build_dir:
        # print(f'{build_dir=}')

        p = npm(
            ['init', '-y'],
            cwd=build_dir,
            stdout=PIPE,
            stderr=PIPE,
            return_completed_process=True,
        )

        assert p.returncode == 0
        # print(f'create_aiohttp_app {p=}')

        total = 1 + len(npm_packages) + len(npm_packages)
        t = tqdm(total=total)
        t.set_description('Install esbuild')
        install_npm_package(static_path, build_dir, 'esbuild', {'version': '*'})
        t.update(1)

        for pkg_name, pkg_info in npm_packages.items():
            t.set_description(f'Install {pkg_name}')
            install_npm_package(static_path, build_dir, pkg_name, pkg_info)
            t.update(1)

        for pkg_name, pkg_info in npm_packages.items():
            t.set_description(f'Compile {pkg_name}')
            paths = compile_npm_package(static_path, build_dir, pkg_name, pkg_info)
            dest_paths.extend(paths)
            t.update(1)

    for path in dest_paths:
        _, ext = os.path.splitext(path)

        if ext == '.css':
            page_links.append('/' + path)
        elif ext == '.js':
            src = f'/{path}'
            page_script = {'type': 'module', 'src': src, 'defer': None}
            page_scripts.append(page_script)

    print(f'{dest_paths=}')
    favicon_path = os.path.join('/', 'static', favicon)
    print(f'{favicon_path=}')

    page = make_page(
        g,
        title=title,
        description=description,
        favicon=favicon_path,
        links=page_links,
        scripts=page_scripts,
    )

    async def page_handler(request):
        return page.render()

    app.router.add_routes([
        web.get('/{tail:.*}', page_handler),
    ])

    app.router.add_static('/static', static_path)

    # favicon
    favicon_dest_path = os.path.join(static_path, favicon)
    print(f'{favicon_dest_path=}')

    if not os.path.exists(favicon_dest_path):
        favicon_src_path = os.path.join(
            os.path.split(gladius.__file__)[0],
            'static',
            'favicon.png',
        )
        print(f'{favicon_src_path=}')

        favicon_dest_dirpath = os.path.split(favicon_dest_path)[0]
        os.makedirs(favicon_dest_dirpath, exist_ok=True)
        shutil.copy(favicon_src_path, favicon_dest_path)

    return g, page, app
"""
def create_aiohttp_app(
    root_dir: Optional[str]=None,
    lang: str='en',
    title: str='Gladius',
    description: str='Gladius',
    static_path: str='./static/',
    favicon: str='img/favicon.png',
    links: list[str | dict | Element]=[],
    scripts: list[str | dict | Element]=[],
    npm_packages: dict[str, Union[dict[str, Any], list[str]]]={},
) -> tuple[Gladius, Element, web.Application]:
    g = Gladius()
    app = web.Application(middlewares=aiohttp_middlewares)

    # install and compile npm packages
    page_links = deepcopy(links)
    page_scripts = deepcopy(scripts)
    npm_links, npm_scripts = install_compile_npm_packages(static_path, npm_packages)
    page_links.extend(npm_links)
    page_scripts.extend(npm_scripts)

    favicon_path = os.path.join('/', 'static', favicon)
    # print(f'{favicon_path=}')

    page = make_page(
        g,
        title=title,
        description=description,
        favicon=favicon_path,
        links=page_links,
        scripts=page_scripts,
    )

    async def page_handler(request):
        return page.render()

    app.router.add_routes([
        web.get('/{tail:.*}', page_handler),
    ])

    app.router.add_static('/static', static_path)

    # favicon
    favicon_dest_path = os.path.join(static_path, favicon)
    # print(f'{favicon_dest_path=}')

    if not os.path.exists(favicon_dest_path):
        favicon_src_path = os.path.join(
            os.path.split(gladius.__file__)[0],
            'static',
            'favicon.png',
        )
        # print(f'{favicon_src_path=}')

        favicon_dest_dirpath = os.path.split(favicon_dest_path)[0]
        os.makedirs(favicon_dest_dirpath, exist_ok=True)
        shutil.copy(favicon_src_path, favicon_dest_path)

    return g, page, app
