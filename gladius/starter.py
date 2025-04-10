__all__ = ['create_app']

import os
import sys
import shutil
from copy import deepcopy
from random import randint
from types import ModuleType
from typing import Any, Optional, Union, Callable, Mapping

from aiohttp import web

from . import gladius
from .element import Element
from .gladius import Gladius
from .imports import (
    JsModuleType,
    TsModuleType,
    JsxModuleType,
    TsxModuleType,
    CssModuleType,
    WasmModuleType,
    local_import_tracker,
)
from .aiohttp import aiohttp_middlewares
from .util import make_page, install_compile_npm_packages, exec_npm_post_bundle, get_gladius_cache
from . import client


DEFAULT_APP_INIT_ARGS = {
    'client_max_size': 1024 ** 3,
}


def create_app(
    lang: str='en',
    title: str='Gladius',
    description: str='Gladius',
    static_path: str='static',
    favicon: str | dict='img/favicon.png',
    links: list[str | dict]=[],
    scripts: list[str | dict]=[],
    npm_packages: Mapping[str, Union[list[str], dict[str, Any]]]={},
    npm_post_bundle: list[list[str]]=[],
    ready: Optional[ModuleType | Callable | list[ModuleType]]=None,
    app_init_args: dict=DEFAULT_APP_INIT_ARGS,
) -> tuple[Gladius, Element, web.Application]:
    # local scope gladius instance
    g = Gladius()

    # aiohttp app
    app = web.Application(middlewares=aiohttp_middlewares, **app_init_args)

    # install and compile npm packages
    page_links = deepcopy(links)
    page_scripts = deepcopy(scripts)
    npm_packages = deepcopy(npm_packages)

    npm_packages['brython'] = { # type: ignore
        'copy': {
            'brython.js': 'brython/',
            'brython_stdlib.js': 'brython/',
        },
    }

    # npm_packages['vhtml'] = { # type: ignore
    #     'copy': {
    #         'dist/vhtml.js': 'vhtml/',
    #     },
    # }

    # npm_packages['@types/vhtml'] = [] # type: ignore

    root_app_dir: str = os.path.join(os.getcwd(), static_path, '__app__')
    # print(f'{root_app_dir=}')

    # remove "__app__" directory, and copy with new content
    shutil.rmtree(root_app_dir, ignore_errors=True)
    os.makedirs(root_app_dir, exist_ok=True)

    # root_npm_dir: str = os.path.join(os.getcwd(), static_path, '__npm__')
    # print(f'{root_npm_dir=}')
    dest_static_path: str = os.path.join(os.getcwd(), static_path)

    npm_paths, npm_links, npm_scripts = install_compile_npm_packages(
        # root_npm_dir,
        dest_static_path,
        npm_packages, # type: ignore
        npm_post_bundle,
        ready,
    )

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
        # print('page_handler', request.path)
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
        # g.script(src=os.path.join('/', 'static', '__npm__', 'vhtml', 'vhtml.js'))
        # g.script("window.h = window.vhtml;")
        g.script('''
            function h(type, props, ...children) {
              return { type, props, children };
            }

            function render(vnode, container) {
              if (typeof vnode === "string" || typeof vnode === "number") {
                // Text node
                return container.appendChild(document.createTextNode(vnode));
              }

              const { type, props, children } = vnode;
              const element = document.createElement(type);

              // Set attributes and event handlers
              Object.entries(props || {}).forEach(([key, value]) => {
                if (key.startsWith("on")) {
                  // Handle events (e.g., "onClick" → "click")
                  element.addEventListener(key.slice(2).toLowerCase(), value);
                } else {
                  element.setAttribute(key, value);
                }
              });

              // Render children recursively
              (children || []).forEach((child) => render(child, element));
              return container.appendChild(element);
            }

            window.h = h;
            window.render = render;
        ''')

    # copy gladius client-side libs
    src_path: str = client.__file__
    dest_path: str = os.path.join(static_path, root_app_dir, 'gladius.py')
    shutil.copy(src_path, dest_path)

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
    # print(f'{module_map=}')

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

        def embed_module(n):
            if isinstance(n, (JsModuleType, TsModuleType, JsxModuleType, TsxModuleType)):
                embed_js_module(n)
            else:
                g.script(n, type='text/python', defer=None)

        def embed_callable(n):
            g.script(n, type='text/python', defer=None)

        def embed_js_module(n):
            gladius_cache_path, gladius_cache = get_gladius_cache()
            build_dir: str = gladius_cache['build_dir']
            # print(f'{gladius_cache=} {build_dir=}')

            path: str = os.path.relpath(n.path)
            outfile: str = os.path.join(os.getcwd(), 'static', '__app__', path)
            ext: str = os.path.splitext(path)[1]

            if ext in {'.js', '.ts', '.jsx', '.tsx'}:
                outfile = os.path.splitext(outfile)[0] + '.js'
            else:
                raise ValueError(f'Unsupported extension: {ext}')

            cmds = [
                [
                    'esbuild',
                    path,
                    '--jsx-factory=h',
                    # '--jsx-fragment=Fragment',
                    '--format=esm',
                    '--platform=node',
                    '--bundle',
                    '--sourcemap',
                    '--loader:.jsx=jsx',
                    '--loader:.tsx=tsx',
                    f'--outfile={outfile}',
                ]
            ]

            exec_npm_post_bundle(build_dir, cmds)

            bundle_path: str = '/' + os.path.relpath(outfile)

            with page['head']:
                g.script(f'''
                    import * as _ from '{bundle_path}?v={randint(0, 2 ** 32)}';
                ''', type='module', defer=None)

        if isinstance(ready, ModuleType):
            embed_module(ready)
        elif isinstance(ready, Callable):
            embed_callable(ready)
        elif isinstance(ready, list):
            assert all([isinstance(n, ModuleType) for n in ready])

            for n in ready:
                embed_module(n)

    return g, page, app
