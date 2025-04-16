import os
import sys
import shutil
from types import ModuleType
from typing import Any, Union

from aiohttp import web

from .aiohttp import aiohttp_middlewares
from .hyperscript import h, HNode
from .imports import local_import_tracker
from .utils import split_name_and_version
from .npm import install_npm_packages
from . import client


DEFAULT_APP_INIT_ARGS = {
    'client_max_size': 1024 ** 3,
}


def create_app(
    lang: str='en',
    title: str='Gladius',
    description: str='Gladius',
    static_path: str='static',
    npm: Union[dict[str, Any], list[str]]={},
    ready: list[ModuleType] | ModuleType=[],
    app_init_args: dict=DEFAULT_APP_INIT_ARGS,
) -> tuple[HNode, web.Application]:
    assert isinstance(npm, dict) or isinstance(npm, list)
    assert isinstance(ready, list) or isinstance(ready, ModuleType)
    copy_paths: dict[str, dict[str, str]]
    compile_paths: dict[str, dict[str, str]]

    if isinstance(npm, list):
        npm = {k: [] for k in npm}

    # check if brython in npm packages
    for k, v in npm.items():
        n, v = split_name_and_version(k)

        if n == 'brython':
            break
    else:
        npm['brython'] = [
            {'copy': 'brython.js'},
            {'copy': 'brython_stdlib.js'},
        ]

    # check if esbuild in npm packages
    for k, v in npm.items():
        n, v = split_name_and_version(k)

        if n == 'esbuild':
            break
    else:
        npm['esbuild'] = []

    if isinstance(ready, ModuleType):
        ready = [ready]

    root_path: str = os.getcwd()

    # remove "__app__" directory, and copy with new content
    app_path: str = os.path.join(root_path, static_path, '__app__')
    shutil.rmtree(app_path, ignore_errors=True)
    os.makedirs(app_path, exist_ok=True)

    with h.html({'lang': lang}) as page:
        with h.head():
            h.meta({'charset': 'utf-8'})
            h.meta({'name': 'viewport', 'content': 'width=device-width, initial-scale=1'})
            h.title({}, title)
            h.meta({'name': 'description', 'content': description})

        with h.body():
            pass

    # npm
    dest_npm_path: str = os.path.join(root_path, static_path, '__npm__')
    shutil.rmtree(dest_npm_path, ignore_errors=True)
    os.makedirs(dest_npm_path, exist_ok=True)
    copy_paths, compile_paths = install_npm_packages(dest_npm_path, npm)

    # copied
    print(f'{copy_paths=}')

    for pkg_name, src_dest_path_map in copy_paths.items():
        for src_path, dest_path in src_dest_path_map.items():
            dirpath, filename = os.path.split(dest_path)
            basename, ext = os.path.splitext(filename)

            with page['head']:
                if ext == '.js':
                    h.script({'type': 'text/javascript', 'src': '/' + dest_path})
                elif ext == '.css':
                    h.link({'rel': 'stylesheet', 'href': '/' + dest_path})

    # compiled
    print(f'{compile_paths=}')

    for pkg_name, src_dest_path_map in compile_paths.items():
        for src_path, dest_path in src_dest_path_map.items():
            name, ver = split_name_and_version(pkg_name)
            dirpath, filename = os.path.split(dest_path)
            basename, ext = os.path.splitext(filename)

            with page['head']:
                if ext == '.js':
                    v: str = name.replace('@', '').replace('/', '_').replace('-', '_').replace('.', '_')
                    k: str = dest_path
                    h.script({'type': 'module'}, f"import * as {v} from '/{k}'; window.{v} = {v};")
                elif ext == '.css':
                    h.link({'rel': 'stylesheet', 'href': '/' + dest_path})

    # copy gladius client-side libs
    src_path: str = client.__file__
    dest_path: str = os.path.join(app_path, 'gladius.py')
    shutil.copy(src_path, dest_path)

    # copy client app modules
    ignored_modules_names: set[str] = (
        set(sys.builtin_module_names) |
        set(sys.stdlib_module_names) |
        {'browser', 'javascript'}
    )

    module_map = {
        k: v
        for k, v in local_import_tracker.local_imports.items()
        if not os.path.isdir(v)
    }

    for k, v in module_map.items():
        _, ext = os.path.splitext(v)

        if ext != '.py':
            continue

        skip_module = False

        for m in ignored_modules_names:
            if k.startswith(m):
                skip_module = True
                break

        if skip_module:
            continue

        src_path: str = os.path.relpath(v)
        dest_path: str = os.path.join(app_path, src_path)
        dest_dirpath, _ = os.path.split(dest_path)
        os.makedirs(dest_dirpath, exist_ok=True)
        shutil.copy(src_path, dest_path)

    #
    # app
    #
    app = web.Application(middlewares=aiohttp_middlewares, **app_init_args)

    async def page_handler(request):
        return page

    app.router.add_routes([
        web.get('/{tail:.*}', page_handler), # type: ignore
    ])

    app.router.add_static('/static', static_path)
    return page, app
