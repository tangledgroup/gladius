__all__ = [
    'make_page',
    'install_npm_package',
    'compile_npm_package',
]

import os
import shutil
from pathlib import Path
from subprocess import PIPE
from typing import Any, Optional, Union

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


#
# npm packages
#

def install_npm_package(static_path: str, build_dir: Union[str, Path], pkg_name: str, pkg_info: Union[str, dict[str, Any], list[str]]):
    if isinstance(pkg_info, str):
        pkg_ver = pkg_info

        if pkg_ver == '*':
            pkg_name_ver = pkg_name
        else:
            pkg_name_ver = f'{pkg_name}@{pkg_ver}'
    elif isinstance(pkg_info, dict):
        pkg_ver = pkg_info.get('version', '*')

        if pkg_ver == '*':
            pkg_name_ver = pkg_name
        else:
            pkg_name_ver = f'{pkg_name}@{pkg_ver}'
    elif isinstance(pkg_info, list):
        pkg_ver = '*'

        if pkg_ver == '*':
            pkg_name_ver = pkg_name
        else:
            pkg_name_ver = f'{pkg_name}@{pkg_ver}'
    else:
        raise ValueError(pkg_info)

    p = npm(
        ['install', '--save', pkg_name_ver],
        cwd=build_dir,
        stdout=PIPE,
        stderr=PIPE,
        return_completed_process=True,
    )

    assert p.returncode == 0
    # print(f'install_npm_package {p=}')


def copy_npm_package(static_path: str, build_dir: Union[str, Path], pkg_name: str, pkg_info: Union[dict, list], pkg_copy: Union[dict, list]):
    # print(f'{pkg_copy=}')
    dest_paths: list[Union[str, Path]] = []

    if isinstance(pkg_copy, list):
        pkg_copy = {k: os.path.join(pkg_name, k) for k in pkg_copy}
        # print(f'new {pkg_copy=}')

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

            dest_path = os.path.relpath(dest_path)
            dest_paths.append(dest_path)
    else:
        raise ValueError(pkg_copy)

    return dest_paths


def bundle_npm_package(static_path: str, build_dir: Union[str, Path], pkg_name: str, pkg_info: Union[dict[str, Any], list[str]], pkg_bundle: Union[dict, list]):
    # print(f'{pkg_bundle=}')
    dest_paths: list[Union[str, Path]] = []

    if isinstance(pkg_bundle, list):
        pkg_bundle = {k: os.path.join(pkg_name, k) for k in pkg_bundle}
        # print(f'new {pkg_bundle=}')

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
            _, ext = os.path.splitext(src_path)

            if ext in ('.wasm',):
                # copy instead of bundle
                pkg_copy = {src_path: dest_path}
                copy_npm_package(static_path, build_dir, pkg_name, pkg_info, pkg_copy)
            else:
                assert isinstance(pkg_info, dict)
                global_name: Optional[str] = pkg_info.get('global-name')
                global_name_cmd = []

                if global_name:
                    global_name_cmd.append(f'--global-name={global_name}')

                p = npx(
                    [
                        'esbuild',
                        src_path,
                        '--bundle',
                        '--minify',
                        '--sourcemap',
                        f'--outfile={dest_path}',
                        '--format=iife',
                        # '--format=esm',
                        '--platform=node',
                        '--loader:.js=js',
                        '--loader:.ts=ts',
                        '--loader:.woff=file',
                        '--loader:.woff2=file',
                        '--loader:.ttf=file',
                        '--loader:.svg=file',
                        '--loader:.wasm=file',
                        *global_name_cmd,
                    ],
                    cwd=build_dir,
                    stdout=PIPE,
                    stderr=PIPE,
                    return_completed_process=True,
                )

                # print(f'compile_npm_package {p=}')

                if p.returncode == 0:
                    dest_path = os.path.relpath(dest_path)
                    dest_paths.append(dest_path)
                else:
                    # copy if bundle failed
                    pkg_copy = {src_path: dest_path}
                    paths = copy_npm_package(static_path, build_dir, pkg_name, pkg_info, pkg_copy)
                    paths = [os.path.relpath(dest_path) for dest_path in paths]
                    dest_paths.extend(paths)

                # print(f'compile_npm_package {p=}')
    else:
        raise ValueError(pkg_bundle)

    return dest_paths


def compile_npm_package(static_path: str, build_dir: Union[str, Path], pkg_name: str, pkg_info: Union[dict[str, Any], list[str]]) -> list[Union[str, Path]]:
    # print(f'{pkg_info=}')
    dest_paths: list[Union[str, Path]] = []

    # create static directory if does not exist
    if not (os.path.exists(static_path) and os.path.isdir(static_path)):
        os.makedirs(static_path, exist_ok=True)

    if isinstance(pkg_info, list):
        # print(f'new {pkg_info=}')
        pkg_info = {'bundle': pkg_info}

    if isinstance(pkg_info, dict):
        if pkg_copy := pkg_info.get('copy'):
            paths = copy_npm_package(static_path, build_dir, pkg_name, pkg_info, pkg_copy)
            dest_paths.extend(paths)

        if pkg_bundle := pkg_info.get('bundle'):
            paths = bundle_npm_package(static_path, build_dir, pkg_name, pkg_info, pkg_bundle)
            dest_paths.extend(paths)

    return dest_paths
