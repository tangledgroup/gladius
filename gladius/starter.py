__all__ = [
    'create_aiohttp_app',
]

import os
import json
import shutil
import urllib.request
from copy import deepcopy
from subprocess import PIPE
from typing import Any, Optional, Union

from aiohttp import web

from . import gladius
from .element import Element
from .gladius import Gladius
from .aiohttp import aiohttp_middlewares
from .util import make_page, install_compile_npm_packages


def create_aiohttp_app(
    root_dir: Optional[str]=None,
    lang: str='en',
    title: str='Gladius',
    description: str='Gladius',
    static_path: str='./static/',
    favicon: str | dict='img/favicon.png',
    links: list[str | dict]=[],
    scripts: list[str | dict]=[],
    npm_packages: dict[str, Union[dict[str, Any], list[str]]]={},
    use_pyscript: bool=True,
    use_micropython: bool=True,
) -> tuple[Gladius, Element, web.Application]:
    g = Gladius()
    app = web.Application(middlewares=aiohttp_middlewares)

    # install and compile npm packages
    page_links = deepcopy(links)
    page_scripts = deepcopy(scripts)
    npm_packages = deepcopy(npm_packages)

    if use_pyscript:
        if use_micropython:
            npm_packages['@pyscript/core'] = [
                'dist/core.js',
                'dist/core.css',
            ]

            npm_packages['@micropython/micropython-webassembly-pyscript'] = [
                'micropython.mjs',
                'micropython.wasm',
            ]

    npm_paths, npm_links, npm_scripts = install_compile_npm_packages(static_path, npm_packages)
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

    # pyscript
    if use_pyscript:
        if use_micropython:
            # print(f'{npm_paths=}')
            mpy_config_content: list[str] | str = []
            mpy_config_files: dict[str, str] | str = {}
            mpy_config_js_modules_main_content: dict[str, str] | str = {}

            # download micropython-stubs - typing
            url = 'https://raw.githubusercontent.com/Josverl/micropython-stubs/refs/heads/main/mip/typing.py'
            dir = 'micropython'
            filename = 'typing.py'
            dirpath = os.path.join(static_path, dir)
            os.makedirs(dirpath, exist_ok=True)
            path = os.path.join(dirpath, filename)

            if not os.path.exists(path):
                urllib.request.urlretrieve(url, path)

            # mpy_config_files[filename] = path
            mpy_config_files[path] = filename

            # download micropython-stubs - typing_extensions
            url = 'https://raw.githubusercontent.com/Josverl/micropython-stubs/refs/heads/main/mip/typing_extensions.py'
            dir = 'micropython'
            filename = 'typing_extensions.py'
            dirpath = os.path.join(static_path, dir)
            os.makedirs(dirpath, exist_ok=True)
            path = os.path.join(dirpath, filename)

            if not os.path.exists(path):
                urllib.request.urlretrieve(url, path)

            # mpy_config_files[filename] = path
            mpy_config_files[path] = filename

            mpy_config_files = '\n'.join(
                f'{json.dumps("/" + k)} = {json.dumps(v)}'
                for k, v in mpy_config_files.items()
            )
            # print(mpy_config_files)

            # include pyscript and micropython
            for k, v in npm_paths.items():
                if k in ('@pyscript/core', '@micropython/micropython-webassembly-pyscript'):
                    continue

                for n in v:
                    _, ext = os.path.split(n)

                    js_module_name: str = k
                    js_module_name = js_module_name.replace('@', '')
                    js_module_name = js_module_name.replace('/', '_')
                    js_module_name = js_module_name.replace('-', '_')
                    js_module_name = js_module_name.replace('.', '_')

                    mpy_config_js_modules_main_content[n] = js_module_name

            mpy_config_js_modules_main_content = '\n'.join(
                f'{json.dumps(k)} = {json.dumps(v)}'
                for k, v in mpy_config_js_modules_main_content.items()
            )

            # print(f'{mpy_config_js_modules_main_content=}')

            mpy_config_content = '\n'.join([
                '\n',

                '[files]',
                mpy_config_files,

                '[js_modules.main]',
                mpy_config_js_modules_main_content,
            ])

            with page['head']:
                g.mpy_config(mpy_config_content)
        else:
            raise ValueError('micropython is only supported')

    return g, page, app
