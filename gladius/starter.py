import os
import sys
import shutil
from random import randint
from types import ModuleType
from typing import Any, Union, Callable

from aiohttp import web

from .aiohttp import aiohttp_middlewares
from .hyperscript import h, HNode
from .utils import get_gladius_cache, split_name_and_version
from .npm import install_npm_packages, exec_esbuild_command
from .imports import (
    JsModuleType,
    TsModuleType,
    JsxModuleType,
    TsxModuleType,
    # CssModuleType,
    # WasmModuleType,
    local_import_tracker,
)
from . import _client_gladius


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

    # check npm
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

    # remove/create "__app__" directory
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

    # remove/create "__npm__" directory
    dest_npm_path: str = os.path.join(root_path, static_path, '__npm__')
    shutil.rmtree(dest_npm_path, ignore_errors=True)
    os.makedirs(dest_npm_path, exist_ok=True)
    copy_paths, compile_paths = install_npm_packages(dest_npm_path, npm)

    # gladius cache and tsconfig exist after `install_npm_packages`
    gladius_cache_path, gladius_cache = get_gladius_cache()
    build_dir: str = gladius_cache['build_dir']
    # print(f'{gladius_cache=} {build_dir=}')

    # copied
    # print(f'{copy_paths=}')
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
    # print(f'{compile_paths=}')
    for pkg_name, src_dest_path_map in compile_paths.items():
        for src_path, dest_path in src_dest_path_map.items():
            name, ver = split_name_and_version(pkg_name)
            dirpath, filename = os.path.split(dest_path)
            basename, ext = os.path.splitext(filename)

            with page['head']:
                if ext == '.js':
                    v: str = (
                        name.replace('@', '')
                            .replace('/', '_')
                            .replace('-', '_')
                            .replace('.', '_')
                    )

                    k: str = dest_path
                    h.script({'type': 'module', 'defer': None}, f"import * as {v} from '/{k}'; window.{v} = {v};")
                elif ext == '.css':
                    h.link({'rel': 'stylesheet', 'href': '/' + dest_path})

    # copy gladius python client-side module
    src_path: str = _client_gladius.__file__
    dest_path: str = os.path.join(app_path, 'gladius.py')
    shutil.copy(src_path, dest_path)

    # copy gladius.js client-side library in build_dir
    src_path: str = os.path.join(os.path.split(_client_gladius.__file__)[0], '_client_gladius.ts')
    dest_path: str = os.path.join(build_dir, '_client_gladius.ts')
    shutil.copy(src_path, dest_path)

    # compile _client_gladius.ts as iife (compatible old style javascript)
    # it is expected that _client_gladius.ts is in build_dir
    # assert os.path.exists(os.path.join(build_dir, '_client_gladius.ts'))
    # src_path: str = '_client_gladius.ts'
    # dest_path: str = os.path.join(app_path, '_client_gladius.js')
    # exec_esbuild_command(build_dir, src_path, dest_path, format='iife')
    # bundle_path: str = '/' + os.path.relpath(dest_path)
    #
    # with page['head']:
    #     h.script({'src': bundle_path})

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
    # ready
    #
    def embed_module(n):
        global h

        if isinstance(n, (JsModuleType, TsModuleType, JsxModuleType, TsxModuleType)):
            embed_js_module(n)
        else:
            with page['head']:
                source = f'import sys\nsys.path = ["static/__app__"]\nimport {n.__name__}'
                h.script({'type': 'text/python', 'defer': None}, source)

    def embed_js_module(n):
        global h

        path: str = os.path.relpath(n.path)
        outfile: str = os.path.join(os.getcwd(), 'static', '__app__', path)
        ext: str = os.path.splitext(path)[1]

        if ext in {'.js', '.ts', '.jsx', '.tsx'}:
            outfile = os.path.splitext(outfile)[0] + '.js'
        else:
            raise ValueError(f'Unsupported extension: {ext}')

        exec_esbuild_command(build_dir, path, outfile)
        bundle_path: str = '/' + os.path.relpath(outfile)

        with page['head']:
            # h.script({'type': 'module', 'defer': None}, "import * as gladius from '/static/__app__/gladius.js'; window.gladius = gladius;")

            h.script(
                {'type': 'module', 'defer': None},
                f"import * as _ from '{bundle_path}?v={randint(0, 2 ** 32)}';"
            )

    '''
    if isinstance(ready, ModuleType):
        embed_module(ready)
    elif isinstance(ready, list):
        assert all([isinstance(n, ModuleType) for n in ready])

        for n in ready:
            embed_module(n)
    '''
    assert all([isinstance(n, ModuleType) for n in ready])

    for n in ready:
        embed_module(n)

    #
    # app
    #
    app = web.Application(middlewares=aiohttp_middlewares, **app_init_args)

    async def favicon_handler(request):
        return web.FileResponse(os.path.join(os.path.split(_client_gladius.__file__)[0], 'favicon.png'))

    async def page_handler(request):
        return page

    app.router.add_routes([
        web.get('/favicon.ico', favicon_handler), # type: ignore
        web.get('/{tail:.*}', page_handler), # type: ignore
    ])

    app.router.add_static('/static', static_path)
    return page, app
