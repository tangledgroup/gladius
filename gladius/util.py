__all__ = [
    'make_page',
    'install_npm_package',
    'compile_npm_package',
    'install_compile_npm_packages',
    'exec_npm_post_bundle',
    'get_gladius_cache',
]

import os
import json
import shutil
import hashlib
from subprocess import PIPE
from typing import Any, Union, Optional
from tempfile import TemporaryDirectory

import json5
from tqdm import tqdm
from deepmerge import always_merger

try:
    from nodejs_wheel import npm, npx
except ImportError:
    pass

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
        with g.head() as head: # noqa
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

        with g.body() as body: # noqa
            pass

    return el


#
# npm packages
#
def install_npm_package(static_path: str, build_dir: str, pkg_name: str, pkg_info: Union[list[str], dict[str, Any]], workspace_name: Optional[str]):
    name, ver = split_name_and_version(pkg_name)
    pkg_name_ver = f'{name}@{ver}'
    print(f'{pkg_name_ver=}')

    if workspace_name:
        cmd = [
            '--workspace',
            workspace_name,
            'install',
            '--save',
            pkg_name_ver,
        ]
    else:
        cmd = [
            'install',
            '--save',
            pkg_name_ver,
        ]

    p = npm( # type: ignore
        cmd,
        cwd=build_dir,
        stdout=PIPE,
        stderr=PIPE,
        return_completed_process=True,
    )

    if p.returncode != 0:
        print('install_npm_package:', p)
        print('stdout:')
        print(p.stdout)
        print('stderr:')
        print(p.stderr)

    assert p.returncode == 0
    # print(f'install_npm_package {p=}')


def copy_npm_package(static_path: str, build_dir: str, pkg_name: str, pkg_info: Union[list[str], dict[str, Any]], pkg_copy: Union[list, dict], workspace_name: str):
    # print(f'{pkg_copy=}')
    name, ver = split_name_and_version(pkg_name)
    dest_paths: list[str] = []

    if isinstance(pkg_copy, list):
        pkg_copy = {k: os.path.join(pkg_name, k) for k in pkg_copy}
        # print(f'new {pkg_copy=}')

    if isinstance(pkg_copy, dict):
        for k, v in pkg_copy.items():
            # try first workspace dir
            src_path = os.path.join(build_dir, workspace_name, 'node_modules', name, k)

            # then temp project dir
            if not os.path.exists(src_path):
                src_path = os.path.join(build_dir, 'node_modules', name, k)

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


def bundle_npm_package(static_path: str, build_dir: str, pkg_name: str, pkg_info: Union[list[str], dict[str, Any]], pkg_bundle: Union[list, dict], workspace_name: str):
    # print(f'{pkg_bundle=}')
    name, ver = split_name_and_version(pkg_name)
    dest_paths: list[str] = []

    if isinstance(pkg_bundle, list):
        pkg_bundle = {k: os.path.join(name, k) for k in pkg_bundle}

    if isinstance(pkg_bundle, dict):
        for k, v in pkg_bundle.items():
            # try first workspace dir
            src_path = os.path.join(build_dir,workspace_name, 'node_modules', name, k)

            # then temp project dir
            if not os.path.exists(src_path):
                src_path = os.path.join(build_dir, 'node_modules', name, k)

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

            # ???
            if ext in ('.wasm',):
                # copy instead of bundle
                pkg_copy = {src_path: dest_path}
                copy_npm_package(static_path, build_dir, pkg_name, pkg_info, pkg_copy, workspace_name)
            else:
                assert isinstance(pkg_info, dict)

                p = npx( # type: ignore
                    [
                        'esbuild',
                        src_path,
                        '--bundle',
                        '--minify',
                        '--sourcemap',
                        f'--outfile={dest_path}',
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
                    paths = copy_npm_package(static_path, build_dir, pkg_name, pkg_info, pkg_copy, workspace_name)
                    paths = [os.path.relpath(dest_path) for dest_path in paths]
                    dest_paths.extend(paths)

                # print(f'compile_npm_package {p=}')
    else:
        raise ValueError(pkg_bundle)

    return dest_paths


def compile_npm_package(static_path: str, build_dir: str, pkg_name: str, pkg_info: Union[list[str], dict[str, Any]], workspace_name: str) -> list[str]:
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
            paths = copy_npm_package(static_path, build_dir, pkg_name, pkg_info, pkg_copy, workspace_name)
            dest_paths.extend(paths)

        if pkg_bundle := pkg_info.get('bundle'):
            paths = bundle_npm_package(static_path, build_dir, pkg_name, pkg_info, pkg_bundle, workspace_name)
            dest_paths.extend(paths)

    return dest_paths


def install_compile_npm_packages(
    static_path: str,
    npm_packages: dict[str, Union[list[str], dict[str, Any]]]={},
    npm_post_bundle: list[list[str]]=[],
) -> tuple[dict[str, list[str]], list[str | dict], list[str | dict]]:
    build_dir: Optional[str] = None
    page_paths: dict[str, list[str]] = {}
    page_links: list[str | dict] = []
    page_scripts: list[str | dict] = []
    dest_paths: list[str] = []

    # load gladius cache
    gladius_cache_path, gladius_cache = get_gladius_cache()
    build_dir = gladius_cache.get('build_dir', None)
    print('loaded gladius cache', gladius_cache_path)

    if build_dir and os.path.exists(build_dir):
        pass
    else:
        td = TemporaryDirectory(prefix='gladius-', delete=False)
        build_dir = td.name

    print(f'{build_dir=}')
    ignore = shutil.ignore_patterns('.gladius', '__npm__', '__app__')
    shutil.copytree(os.getcwd(), build_dir, ignore=ignore, dirs_exist_ok=True)

    if not os.path.exists(os.path.join(build_dir, 'package.json')):
        p = npm( # type: ignore
            ['init', '-y'],
            cwd=build_dir,
            stdout=PIPE,
            stderr=PIPE,
            return_completed_process=True,
        )

        if p.returncode != 0:
            print('install_npm_package:', p)
            print('stdout:')
            print(p.stdout)
            print('stderr:')
            print(p.stderr)

        assert p.returncode == 0
        # print(f'create_aiohttp_app {p=}')

    workspace_name: str = f'workspace-{hash_npm_packages(npm_packages)}'
    print(f'{workspace_name=}')

    total = 0

    if not os.path.exists(os.path.join(build_dir, 'node_modules', 'esbuild')):
        total += 1

    if not os.path.exists(os.path.join(build_dir, workspace_name)):
        total += len(npm_packages)

    total += len(npm_packages) # compile

    t = tqdm(total=total)

    if not os.path.exists(os.path.join(build_dir, 'node_modules', 'esbuild')):
        t.set_description('Install esbuild')
        install_npm_package(static_path, build_dir, 'esbuild', {'version': '*'}, None)

    t.update(1)

    if not os.path.exists(os.path.join(build_dir, workspace_name)):
        p = npm( # type: ignore
            ['--workspace', workspace_name, 'init', '-y'],
            cwd=build_dir,
            stdout=PIPE,
            stderr=PIPE,
            return_completed_process=True,
        )

        if p.returncode != 0:
            print('install_npm_package:', p)
            print('stdout:')
            print(p.stdout)
            print('stderr:')
            print(p.stderr)

        assert p.returncode == 0

        for pkg_name, pkg_info in npm_packages.items():
            t.set_description(f'Install {pkg_name}')
            install_npm_package(static_path, build_dir, pkg_name, pkg_info, workspace_name)
            t.update(1)

    for pkg_name, pkg_info in npm_packages.items():
        t.set_description(f'Compile {pkg_name}')
        paths = compile_npm_package(static_path, build_dir, pkg_name, pkg_info, workspace_name)
        page_paths[pkg_name] = paths
        dest_paths.extend(paths)
        t.update(1)

    # post bundle commands/scripts
    exec_npm_post_bundle(build_dir, npm_post_bundle)

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

    # save gladius cache
    gladius_cache = {
        'build_dir': build_dir,
        'npm_packages': npm_packages,
        'page_paths': page_paths,
        'page_links': page_links,
        'page_scripts': page_scripts,
    }

    gladius_cache_path = save_gladius_cache(gladius_cache)
    print('saved gladius cache', gladius_cache_path)

    tsconfig_path = create_or_update_tsconfig({
        'compilerOptions': {
            'baseUrl': os.path.join(build_dir, 'node_modules')
        }
    })
    print('create/update tsconfig', tsconfig_path)

    return page_paths, page_links, page_scripts


def exec_npm_post_bundle(build_dir: str, npm_post_bundle: list[list[str]]):
    for cmd in npm_post_bundle:
        # print(f'{build_dir=} {cmd=}')

        p = npx( # type: ignore
            cmd,
            cwd=build_dir,
            stdout=PIPE,
            stderr=PIPE,
            return_completed_process=True,
        )

        if p.returncode != 0:
            print('install_npm_package:', p)
            print('stdout:')
            print(p.stdout)
            print('stderr:')
            print(p.stderr)

        assert p.returncode == 0


def get_gladius_cache() -> tuple[str, dict]:
    gladius_cache_path = '.gladius'
    gladius_cache: dict

    if os.path.exists(gladius_cache_path):
        with open(gladius_cache_path, 'r') as f:
            gladius_cache = json.load(f)
    else:
        gladius_cache = {}
        gladius_cache_path = save_gladius_cache(gladius_cache)

    return gladius_cache_path, gladius_cache


def save_gladius_cache(gladius_cache: dict) -> str:
    gladius_cache_path = '.gladius'

    with open(gladius_cache_path, 'w') as f:
        json.dump(gladius_cache, f, indent=2)

    return gladius_cache_path


def split_name_and_version(pkg_name: str) -> tuple[str, str]:
    if pkg_name.startswith('@'):
        if pkg_name.count('@') == 1:
            name = pkg_name
            ver = 'latest'
        else:
            name, ver = pkg_name.rsplit('@', maxsplit=1)
    else:
        if '@' in pkg_name:
            name, ver = pkg_name.split('@')
        else:
            name = pkg_name
            ver = 'latest'

    return name, ver


def create_or_update_tsconfig(tsconfig: dict) -> str:
    tsconfig_path = 'tsconfig.json'

    if os.path.exists(tsconfig_path):
        #  update
        with open(tsconfig_path, 'r') as f:
            current_tsconfig = json5.load(f)

        final_tsconfig = always_merger.merge(current_tsconfig, tsconfig)
    else:
        # create
        assert 'compilerOptions' in tsconfig and 'baseUrl' in tsconfig['compilerOptions']

        default_tsconfig = {
            "compilerOptions": {
                # NOTE: key/value for "baseUrl" should be in tsconfig
                # "baseUrl": "/tmp/gladius-bpqnncpq/node_modules",
                "jsx": "preserve",
                "jsxFactory": "h",
                "jsxFragmentFactory": "Fragment"
            },
            "include": ["**/*.ts", "**/*.tsx"]
        }

        final_tsconfig = always_merger.merge(default_tsconfig, tsconfig)

    with open(tsconfig_path, 'w') as f:
        json.dump(final_tsconfig, f, indent=2)

    return tsconfig_path


def hash_npm_packages(npm_packages: dict[str, Any]) -> str:
    m = hashlib.sha256()
    m.update(json.dumps(npm_packages).encode())
    h = m.hexdigest()
    h = h[:7] # inspired by git which uses first 7 characters
    return h
