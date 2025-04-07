__all__ = ['create_app']

import os
import sys
import shutil
from copy import deepcopy
from types import ModuleType
from typing import Any, Optional, Union, Callable

from aiohttp import web

from . import gladius
from .element import Element
from .gladius import Gladius
from .aiohttp import aiohttp_middlewares
from .util import make_page, install_compile_npm_packages
from . import client


def create_app(
    lang: str='en',
    title: str='Gladius',
    description: str='Gladius',
    static_path: str='static',
    favicon: str | dict='img/favicon.png',
    links: list[str | dict]=[],
    scripts: list[str | dict]=[],
    npm_packages: dict[str, Union[dict[str, Any], list[str]]]={},
    module_map: Optional[dict[str, str]]=None,
    ready: Optional[ModuleType | Callable]=None,
    app_init_args: dict | None=None,
) -> tuple[Gladius, Element, web.Application]:
    g = Gladius()

    if not app_init_args:
        app_init_args = {}

    app = web.Application(middlewares=aiohttp_middlewares, **app_init_args)

    # install and compile npm packages
    page_links = deepcopy(links)
    page_scripts = deepcopy(scripts)
    npm_packages = deepcopy(npm_packages)

    # NOTE: https://github.com/tangledgroup/gladius/commit/b019ddea7fbc41074bdd7da921cdbcf612f8da13
    npm_packages['brython'] = {
        'version': '3.13.1',
        'copy': {
            'brython.js': 'brython/',
            'brython_stdlib.js': 'brython/',
        },
    }

    root_npm_dir: str = os.path.join(os.getcwd(), static_path, '__npm__')
    # print(f'{root_npm_dir=}')

    npm_paths, npm_links, npm_scripts = install_compile_npm_packages(root_npm_dir, npm_packages)
    page_links.extend(npm_links)
    page_scripts.extend(npm_scripts)

    if isinstance(favicon, str):
        favicon_path = os.path.join('/', 'static', favicon)
    elif isinstance(favicon, dict):
        favicon_path = os.path.join('/', 'static', favicon['href'])
    else:
        raise ValueError(favicon)
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
        web.get('/{tail:.*}', page_handler), # type: ignore
    ])

    app.router.add_static('/static', static_path)

    # favicon
    if isinstance(favicon, str):
        favicon_dest_path = os.path.join(static_path, favicon)
    elif isinstance(favicon, dict):
        favicon_dest_path = os.path.join(static_path, favicon['href'])
    else:
        raise ValueError(favicon)
    # print(f'{favicon_dest_path=}')

    # copy favicon if doesn't exist
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

    bpy_config_js_modules_main_content: dict[str, str] | str = {}

    with page['head']:
        g.script(src=os.path.join('/', 'static', '__npm__', 'brython', 'brython.js'))
        g.script(src=os.path.join('/', 'static', '__npm__', 'brython', 'brython_stdlib.js'))

    root_app_dir: str = os.path.join(os.getcwd(), static_path, '__app__')
    # print(f'{root_app_dir=}')

    # remove "__app__" directory, and copy with new content
    shutil.rmtree(root_app_dir, ignore_errors=True)
    os.makedirs(root_app_dir, exist_ok=True)

    # copy gladius client-side libs
    src_path: str = client.__file__
    dest_path: str = os.path.join(static_path, root_app_dir, 'gladius.py')
    shutil.copy(src_path, dest_path)

    # if ready is path to file, copy it into __app__, and include it in config
    if isinstance(ready, str) and os.path.exists(ready):
        # make sure parent directory of dest file exists
        module_app_path: str = os.path.join(static_path, root_app_dir, ready)
        d, _ = os.path.split(module_app_path)
        os.makedirs(d, exist_ok=True)
        shutil.copy(ready, module_app_path)

    ignored_modules_names: set[str] = set(sys.builtin_module_names) | set(sys.stdlib_module_names) | {'browser', 'javascript'}

    if module_map:
        for k, v in module_map.items():
            skip_module = False

            for m in ignored_modules_names:
                if k.startswith(m):
                    skip_module = True
                    break

            if skip_module:
                continue

            src_path: str = os.path.relpath(v)
            dest_path: str = os.path.join(static_path, root_app_dir, src_path)

            dest_dirpath, _ = os.path.split(dest_path)
            os.makedirs(dest_dirpath, exist_ok=True)
            shutil.copy(src_path, dest_path)

    for k, v in npm_paths.items():
        # print(f'npm_paths {k=}: {v=}')

        if k in ['brython']:
            continue

        for n in v:
            _, ext = os.path.split(n)

            js_module_name: str = k
            js_module_name = js_module_name.replace('@', '')
            js_module_name = js_module_name.replace('/', '_')
            js_module_name = js_module_name.replace('-', '_')
            js_module_name = js_module_name.replace('.', '_')
            bpy_config_js_modules_main_content[n] = js_module_name

    # print(f'{bpy_config_js_modules_main_content=}')

    with page['head']:
        for k, v in bpy_config_js_modules_main_content.items():
            # print(f'{k=}: {v=}')

            if os.path.splitext(k)[1] in ('.js', '.mjs'):
                g.script(f"import * as {v} from '/{k}'; window.{v} = {v};", type='module')

        if isinstance(ready, (ModuleType, Callable)):
            g.script(ready, type='text/python', defer=None)
        elif isinstance(ready, str):
            ready_module_name, _ = os.path.splitext(ready)

            g.script(
                f'\nimport sys; sys.path = ["static/__app__"]\nimport {ready_module_name}\n',
                type='text/python',
                defer=None,
            )
        else:
            raise ValueError(ready)

    return g, page, app
