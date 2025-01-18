__all__ = [
    'make_page',
    'install_npm_package',
    'compile_npm_package',
]

import os
import shutil
from typing import Union
from pathlib import Path

from nodejs_wheel import npm, npx

from .element import Element
from .gladius import Gladius


def make_page(
    g: Gladius,
    lang: str='en',
    title: str='Gladius',
    description: str='Gladius',
    favicon: str | tuple | list | dict | Element='/static/img/favicon.png',
    links: list[str | tuple | list | dict | Element]=[],
    scripts: list[str | tuple | list | dict | Element]=[],
) -> Element:
    el: Element

    with g.html(lang=lang) as el:
        with g.head() as head:
            g.meta(charset='utf-8')
            g.meta(name='viewport', content='width=device-width, initial-scale=1')
            g.title(title)
            g.meta(name='description', content=description)

            # favicon
            if isinstance(favicon, str):
                g.link(rel='icon', href=favicon, type='image/png')
            elif isinstance(favicon, (tuple, list)):
                assert 1 <= len(favicon) <= 2

                if len(favicon) == 1:
                    href = favicon[0]
                    g.link(rel='icon', href=href, type='image/png')
                elif len(favicon) == 2:
                    href, type_ = favicon
                    g.link(rel='icon', href=href, type=type_)
            elif isinstance(favicon, dict):
                g.link(**favicon)
            elif isinstance(favicon, Element):
                head.add(favicon)

            # links
            for n in links:
                if isinstance(n, str):
                    g.link(rel='stylesheet', href=n)
                elif isinstance(n, (tuple, list)):
                    assert 1 <= len(n) <= 2

                    if len(n) == 1:
                        href = n[0]
                        g.link(rel='stylesheet', href=href)
                    elif len(n) == 2:
                        rel, href = n
                        g.link(rel=rel, href=href)
                elif isinstance(n, dict):
                    g.link(**n)
                elif isinstance(n, Element):
                    head.add(n)

            # scripts
            for n in scripts:
                if isinstance(n, str):
                    g.script(src=n)
                elif isinstance(n, (tuple, list)):
                    assert 1 <= len(n) <= 2

                    if len(n) == 1:
                        src = n[0]
                        g.script(src=src)
                    elif len(n) == 2:
                        src, defer = n
                        g.script(src=src, defer=defer)
                elif isinstance(n, dict):
                    g.script(**n)
                elif isinstance(n, Element):
                    head.add(n)

    return el


def install_npm_package(build_dir: Union[str, Path], pkg_name: str, pkg_info: str | dict):
    if isinstance(pkg_info, str):
        pkg_ver = pkg_info

        if pkg_ver == '*':
            pkg_name_ver = pkg_name
        else:
            pkg_name_ver = f'{pkg_name}@{pkg_ver}'
    elif isinstance(pkg_info, dict):
        pkg_ver = pkg_info['version']

        if pkg_ver == '*':
            pkg_name_ver = pkg_name
        else:
            pkg_name_ver = f'{pkg_name}@{pkg_ver}'
    else:
        raise ValueError(pkg_info)

    p = npm(['install', '--save', pkg_name_ver], cwd=build_dir, return_completed_process=True)
    print(f'install_npm_package {p=}')


def compile_npm_package(build_dir: Union[str, Path], pkg_name: str, pkg_info: dict) -> Union[str, Path]:
    static_path: str = './static/'

    # create static directory if does not exist
    if not (os.path.exists(static_path) and os.path.isdir(static_path)):
        os.makedirs(static_path, exist_ok=True)

    if pkg_copy := pkg_info.get('copy'):
        print(f'{pkg_copy=}')

        if isinstance(pkg_copy, dict):
            for k, v in pkg_copy.items():
                src_path = os.path.join(build_dir, 'node_modules', pkg_name, k)
                dest_path = os.path.join(static_path, v)

                if not (os.path.exists(src_path) and os.path.isfile(src_path)):
                    raise FileNotFoundError(src_path)

                if dest_path.endswith('/'):
                    # dir ends with "/"
                    if not (os.path.exists(dest_path) and os.path.isdir(dest_path)):
                        os.makedirs(dest_path, exist_ok=True)
                else:
                    # otherwise, it is file path
                    dest_dirpath, dest_filename = os.path.split(dest_path)

                    if not (os.path.exists(dest_dirpath) and os.path.isdir(dest_dirpath)):
                        os.makedirs(dest_dirpath, exist_ok=True)

                shutil.copy(src_path, dest_path)
        else:
            raise ValueError(pkg_copy)
    elif pkg_bundle := pkg_info.get('bundle'):
        print(f'{pkg_bundle=}')

        if isinstance(pkg_bundle, dict):
            for k, v in pkg_bundle.items():
                src_path = os.path.join(build_dir, 'node_modules', pkg_name, k)
                dest_path = os.path.join(static_path, v)

                if not (os.path.exists(src_path) and os.path.isfile(src_path)):
                    raise FileNotFoundError(src_path)

                if dest_path.endswith('/'):
                    # dir ends with "/"
                    if not (os.path.exists(dest_path) and os.path.isdir(dest_path)):
                        os.makedirs(dest_path, exist_ok=True)

                    _, dest_filename = os.path.split(src_path)
                    dest_dirpath = dest_path
                    dest_path = os.path.join(dest_dirpath, dest_filename)
                else:
                    # otherwise, it is file path
                    dest_dirpath, dest_filename = os.path.split(dest_path)

                    if not (os.path.exists(dest_dirpath) and os.path.isdir(dest_dirpath)):
                        os.makedirs(dest_dirpath, exist_ok=True)

                dest_path = os.path.abspath(dest_path)

                global_name = pkg_bundle.get('global-name')
                global_name_cmd = []

                if global_name:
                    global_name_cmd.append(f'--global-name="{global_name}"')

                p = npx(
                    [
                        'esbuild',
                        src_path,
                        '--bundle',
                        '--minify',
                        '--sourcemap',
                        f'--outfile={dest_path}',
                        '--format=iife',
                        '--platform=node',
                        '--loader:.ts=ts',
                        '--loader:.woff=file',
                        '--loader:.woff2=file',
                        '--loader:.ttf=file',
                        '--loader:.svg=file',
                        *global_name_cmd,
                    ],
                    cwd=build_dir,
                    return_completed_process=True,
                )

                print(f'compile_npm_package {p=}')
        else:
            raise ValueError(pkg_bundle)

    else:
        raise ValueError('One of "copy" or "bundle" is required')

    return ''
