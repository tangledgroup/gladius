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
    # ready
    #
    def embed_module(n):
        global h

        if isinstance(n, (JsModuleType, TsModuleType, JsxModuleType, TsxModuleType)):
            embed_js_module(n)
        else:
            h.script({'type': 'text/python', 'defer': None}, n)

    def embed_callable(n):
        global h
        h.script({'type': 'text/python', 'defer': None}, n)

    def embed_js_module(n):
        global h
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

        exec_esbuild_command(build_dir, path, outfile)
        bundle_path: str = '/' + os.path.relpath(outfile)

        with page['head']:
            h.script(
                {'type': 'text/javascript'},
                '''
                    const observers = [];

                    function h(type, props, ...children) {
                        return { type, props, children };
                    }

                    function effect(fn) {
                        const execute = () => {
                        observers.push(execute);

                        try {
                            fn();
                        } finally {
                            observers.pop();
                        }
                        };

                        execute();
                    }

                    function signal(value) {
                        const subscribers = new Set();

                        const getValue = () => {
                        const current = observers[observers.length - 1];

                        if (current) {
                            subscribers.add(current);
                        }

                        return value;
                        };

                        const setValue = (newValue) => {
                        value = newValue;

                        for (const subscriber of subscribers) {
                            subscriber();
                        }
                        };

                        return [getValue, setValue];
                    }

                    /*
                    function render(vnode, container) {
                        // Clear container before rendering new content
                        container.innerHTML = '';

                        // Create DOM elements from vnode recursively
                        const createElement = (node) => {
                            if (typeof node === 'string' || typeof node === 'number') {
                                return document.createTextNode(node.toString());
                            }

                            if (typeof node.type === 'function') {
                                // Handle component functions
                                const props = { ...node.props, children: node.children };
                                const componentVnode = node.type(props);
                                return createElement(componentVnode);
                            }

                            // Create regular DOM element
                            const element = document.createElement(node.type);

                            // Set attributes and event handlers
                            if (node.props) {
                                Object.entries(node.props).forEach(([key, value]) => {
                                    if (key.startsWith('on')) {
                                        // Handle events (e.g., onClick)
                                        element[key.toLowerCase()] = value;
                                    } else {
                                        element.setAttribute(key, value);
                                    }
                                });
                            }

                            // Recursively render children
                            node.children.forEach(child => {
                                element.appendChild(createElement(child));
                            });

                            return element;
                        };

                        // Start rendering process
                        const element = createElement(vnode);
                        container.appendChild(element);
                    }
                    */

                    function render(vnode, container) {
                        const newNode = createElement(vnode);
                        const oldNode = container.firstChild;
                        if (oldNode) {
                            morph(oldNode, newNode);
                        } else {
                            container.appendChild(newNode);
                        }
                    }

                    function createElement(node) {
                        if (typeof node === 'string' || typeof node === 'number') {
                            return document.createTextNode(node.toString());
                        }
                        if (typeof node.type === 'function') {
                            const props = { ...node.props, children: node.children };
                            const componentVnode = node.type(props);
                            return createElement(componentVnode);
                        }
                        const element = document.createElement(node.type);
                        if (node.props) {
                            Object.entries(node.props).forEach(([key, value]) => {
                                if (key.startsWith('on')) {
                                    element[key.toLowerCase()] = value;
                                } else {
                                    element.setAttribute(key, value);
                                }
                            });
                        }
                        element._props = node.props; // Store props for morphing
                        node.children.forEach(child => element.appendChild(createElement(child)));
                        return element;
                    }

                    function morph(oldNode, newNode) {
                        if (oldNode.nodeType !== newNode.nodeType ||
                            (oldNode.nodeType === Node.ELEMENT_NODE && oldNode.tagName !== newNode.tagName)) {
                            oldNode.replaceWith(newNode);
                            return;
                        }
                        if (oldNode.nodeType === Node.TEXT_NODE) {
                            if (oldNode.textContent !== newNode.textContent) {
                                oldNode.textContent = newNode.textContent;
                            }
                            return;
                        }
                        // Update attributes
                        const oldAttrs = oldNode.attributes;
                        const newAttrs = newNode.attributes;
                        for (let i = oldAttrs.length - 1; i >= 0; i--) {
                            const { name } = oldAttrs[i];
                            if (!newAttrs[name]) oldNode.removeAttribute(name);
                        }
                        for (const { name, value } of newAttrs) {
                            if (oldNode.getAttribute(name) !== value) oldNode.setAttribute(name, value);
                        }
                        // Update event handlers from props
                        const oldProps = oldNode._props || {};
                        const newProps = newNode._props || {};
                        Object.keys(oldProps).forEach(key => {
                            if (key.startsWith('on') && !newProps[key]) {
                                oldNode[key.toLowerCase()] = null;
                            }
                        });
                        Object.keys(newProps).forEach(key => {
                            if (key.startsWith('on')) {
                                const newValue = newProps[key];
                                const oldValue = oldProps[key];
                                if (newValue !== oldValue) {
                                    oldNode[key.toLowerCase()] = newValue;
                                }
                            }
                        });
                        // Morph children
                        const oldChildren = Array.from(oldNode.childNodes);
                        const newChildren = Array.from(newNode.childNodes);
                        const maxLength = Math.max(oldChildren.length, newChildren.length);
                        for (let i = 0; i < maxLength; i++) {
                            const oldChild = oldChildren[i];
                            const newChild = newChildren[i];
                            if (oldChild && newChild) {
                                morph(oldChild, newChild);
                            } else if (newChild) {
                                oldNode.appendChild(newChild);
                            } else if (oldChild) {
                                oldNode.removeChild(oldChild);
                            }
                        }
                    }
                '''
            )

            h.script(
                {'type': 'module', 'defer': None},
                f"import * as _ from '{bundle_path}?v={randint(0, 2 ** 32)}';"
            )

    if isinstance(ready, ModuleType):
        embed_module(ready)
    elif isinstance(ready, Callable):
        embed_callable(ready)
    elif isinstance(ready, list):
        assert all([isinstance(n, ModuleType) for n in ready])

        for n in ready:
            embed_module(n)

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
