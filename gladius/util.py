__all__ = [
    'make_page',
    'install_npm_package',
    'compile_npm_package',
    'install_compile_npm_packages',
]

import os
import json
import shutil
from subprocess import PIPE
from typing import Any, Union
from tempfile import TemporaryDirectory

from tqdm import tqdm
from nodejs_wheel import npm, npx

from .element import Element
from .gladius import Gladius


def make_page(
    g: Gladius,
    lang: str='en',
    title: str='Gladius',
    description: str='Gladius',
    favicon: str | dict='/static/img/favicon.png',
    links: list[str | dict]=[],
    scripts: list[str | dict]=[],
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
            elif isinstance(favicon, dict):
                g.link(**favicon)
            else:
                raise ValueError(favicon)

            # links
            for n in links:
                if isinstance(n, str):
                    g.link(rel='stylesheet', href=n)
                elif isinstance(n, dict):
                    g.link(**n)
                else:
                    raise ValueError(n)

            # scripts
            for n in scripts:
                if isinstance(n, str):
                    g.script(src=n)
                elif isinstance(n, dict):
                    g.script(**n)
                else:
                    raise ValueError(n)

    return el


#
# npm packages
#
def install_npm_package(static_path: str, build_dir: str, pkg_name: str, pkg_info: Union[str, dict[str, Any], list[str]]):
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


def copy_npm_package(static_path: str, build_dir: str, pkg_name: str, pkg_info: Union[dict, list], pkg_copy: Union[dict, list]):
    # print(f'{pkg_copy=}')
    dest_paths: list[str] = []

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


def bundle_npm_package(static_path: str, build_dir: str, pkg_name: str, pkg_info: Union[dict[str, Any], list[str]], pkg_bundle: Union[dict, list]):
    # print(f'{pkg_bundle=}')
    dest_paths: list[str] = []

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
                # global_name: Optional[str] = pkg_info.get('global-name')
                # global_name_cmd = []
                #
                # if global_name:
                #     global_name_cmd.append(f'--global-name={global_name}')

                p = npx(
                    [
                        'esbuild',
                        src_path,
                        '--bundle',
                        # '--minify',
                        '--sourcemap',
                        f'--outfile={dest_path}',
                        # '--format=iife',
                        '--format=esm',
                        '--platform=node',
                        '--loader:.css=css',
                        '--loader:.js=js',
                        '--loader:.ts=ts',
                        '--loader:.woff=file',
                        '--loader:.woff2=file',
                        '--loader:.ttf=file',
                        '--loader:.svg=file',
                        '--loader:.wasm=file',
                        # *global_name_cmd,
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


def compile_npm_package(static_path: str, build_dir: str, pkg_name: str, pkg_info: Union[dict[str, Any], list[str]]) -> list[str]:
    # print(f'{pkg_info=}')
    dest_paths: list[str] = []

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


def install_compile_npm_packages(
    static_path: str,
    npm_packages: dict[str, Union[dict[str, Any], list[str]]]={},
) -> tuple[dict[str, list[str]], list[str | dict], list[str | dict]]:
    page_paths: dict[str, list[str]]
    page_links: list[str | dict]
    page_scripts: list[str | dict]

    # try to load npm cache
    cache_dir = '.cache'
    cache_file = 'npm_packages.json'
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, cache_file)

    if os.path.exists(cache_path):
        with open(cache_path, 'r') as f:
            cached_npm_packages = json.load(f)

        if cached_npm_packages['npm_packages'] == npm_packages:
            page_paths = cached_npm_packages['page_paths']
            page_links = cached_npm_packages['page_links']
            page_scripts = cached_npm_packages['page_scripts']
            print('loaded npm cache', cache_path)
            return page_paths, page_links, page_scripts

    page_paths = {}
    page_links = []
    page_scripts = []
    dest_paths: list[str] = []

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
            page_paths[pkg_name] = paths
            dest_paths.extend(paths)
            t.update(1)

    # print(f'{dest_paths=}')

    for path in dest_paths:
        _, ext = os.path.splitext(path)

        if ext == '.css':
            href = f'/{path}'
            page_link = {'rel': 'stylesheet', 'href': href}
            page_links.append(page_link)
        elif ext == '.js':
            src = f'/{path}'
            page_script = {'type': 'module', 'src': src, 'defer': None}
            page_scripts.append(page_script)

    # save npm cache
    if os.path.exists(cache_path):
        os.remove(cache_path)

    with open(cache_path, 'w') as f:
        cached_npm_packages = {
            'npm_packages': npm_packages,
            'page_paths': page_paths,
            'page_links': page_links,
            'page_scripts': page_scripts,
        }

        json.dump(cached_npm_packages, f, indent=2)
        print('saved npm cache', cache_path)

    return page_paths, page_links, page_scripts
