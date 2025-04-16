import os
import shutil
from subprocess import PIPE
from typing import Any, Optional, Union
from tempfile import TemporaryDirectory

from tqdm import tqdm
from nodejs_wheel import npm, npx

from .utils import get_gladius_cache, save_gladius_cache, create_or_update_tsconfig
from .utils import split_name_and_version, hash_npm_packages


def install_npm_packages(dest_npm_path: str, npm_packages: dict[str, Any]) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    gladius_cache_path: str
    gladius_cache: dict[str, Any]
    build_dir: Optional[str]
    copy_paths: dict[str, dict[str, str]] = {}
    compile_paths: dict[str, dict[str, str]] = {}

    # load gladius cache
    gladius_cache_path, gladius_cache = get_gladius_cache()
    print('loaded gladius cache', gladius_cache_path)

    # prepare build dir
    build_dir = gladius_cache.get('build_dir')

    if build_dir and os.path.exists(build_dir):
        pass
    else:
        td = TemporaryDirectory(prefix='gladius-', delete=False)
        build_dir = td.name

    print(f'{build_dir=}')
    ignore = shutil.ignore_patterns('.gladius', '__npm__', '__app__')
    shutil.copytree(os.getcwd(), build_dir, ignore=ignore, dirs_exist_ok=True)

    # package.json
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

    # workspace
    workspace_name: str = f'workspace-{hash_npm_packages(npm_packages)}'
    print(f'{workspace_name=}')

    # check npm_packages
    for pkg_name, pkg_info in list(npm_packages.items()):
        name, ver = split_name_and_version(pkg_name)

        if name == 'tailwindcss':
            has_tailwindcss_cli = False

            for pkg_name2, pkg_info2 in list(npm_packages.items()):
                name2, ver2 = split_name_and_version(pkg_name2)

                if pkg_name2 == '@tailwindcss/cli':
                    has_tailwindcss_cli = True
                    break

            if not has_tailwindcss_cli:
                npm_packages['@tailwindcss/cli'] = []

    # progress
    total = 0

    # install packages in workspace
    if not os.path.exists(os.path.join(build_dir, workspace_name)):
        total += len(npm_packages)

    # compile / copy
    for pkg_name, pkg_info in npm_packages.items():
        if not pkg_info:
            continue

        if isinstance(pkg_info, list):
            for n in pkg_info:
                if isinstance(n, str):
                    total += 1 # compile
                elif isinstance(n, dict) and 'copy' in n:
                    total += 1 # copy
                elif isinstance(n, dict) and 'compile' in n:
                    total += 1 # compile
                else:
                    raise ValueError(f'Unsupported "npm" package definition {pkg_name!r}: {pkg_info!r}')

    t = tqdm(total=total)

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
            install_npm_package(dest_npm_path, build_dir, workspace_name, pkg_name, pkg_info)
            t.update(1)

    # copy packages
    for pkg_name, pkg_info in npm_packages.items():
        if pkg_info and isinstance(pkg_info, list):
            for n in pkg_info:
                if isinstance(n, dict) and 'copy' in n:
                    # copy package file
                    t.set_description(f'Copy {pkg_name!r} {n!r}')

                    copy_paths.update(
                        copy_npm_package(dest_npm_path, build_dir, workspace_name, pkg_name, pkg_info)
                    )

                    t.update(1)

    # compile packages
    for pkg_name, pkg_info in npm_packages.items():
        if pkg_info and isinstance(pkg_info, list):
            for n in pkg_info:
                if isinstance(n, str) or (isinstance(n, dict) and 'compile' in n):
                    # compile packages
                    t.set_description(f'Compile {pkg_name!r} {n!r}')

                    compile_paths.update(
                        compile_npm_package(dest_npm_path, build_dir, workspace_name, pkg_name, pkg_info)
                    )

                    t.update(1)

    # save gladius cache
    gladius_cache['build_dir'] = build_dir
    gladius_cache['npm_packages'] = npm_packages
    save_gladius_cache(gladius_cache)

    return copy_paths, compile_paths


def install_npm_package(dest_npm_path: str, build_dir: str, workspace_name: str, pkg_name: str, pkg_info: list[Any]):
    name, ver = split_name_and_version(pkg_name)
    pkg_name_ver = f'{name}@{ver}'
    # print(f'install_npm_package: {pkg_name_ver=}')

    cmd = [
        '--workspace',
        workspace_name,
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


def copy_npm_package(dest_npm_path: str, build_dir: str, workspace_name: str, pkg_name: str, pkg_info: list[Any]) -> dict[str, dict[str, str]]:
    name, ver = split_name_and_version(pkg_name)
    paths: dict[str, dict[str, str]] = {}

    for n in pkg_info:
        assert 'copy' in n
        n = n['copy']
        assert isinstance(n, str)

        # try first workspace dir
        src_path = os.path.join(build_dir, workspace_name, 'node_modules', name, n)

        # then temp project dir
        if not os.path.exists(src_path):
            src_path = os.path.join(build_dir, 'node_modules', name, n)

        if not (os.path.exists(src_path) and os.path.isfile(src_path)):
            raise FileNotFoundError(src_path)

        dest_dirpath = os.path.join(dest_npm_path, name)

        if not (os.path.exists(dest_dirpath) and os.path.isdir(dest_dirpath)):
            os.makedirs(dest_dirpath, exist_ok=True)

        dest_path = os.path.join(dest_dirpath, n)
        shutil.copy(src_path, dest_path)

        if pkg_name not in paths:
            paths[pkg_name] = {}

        paths[pkg_name][os.path.join(name, n)] = os.path.relpath(dest_path)

    return paths


def compile_npm_package(dest_npm_path: str, build_dir: str, workspace_name: str, pkg_name: str, pkg_info: list[Any]) -> dict[str, dict[str, str]]:
    paths: dict[str, dict[str, str]] = {}
    name, ver = split_name_and_version(pkg_name)

    for n in pkg_info:
        if 'compile' in n:
            n = n['compile']

        assert isinstance(n, str)

        # try first workspace dir
        src_path = os.path.join(build_dir, workspace_name, 'node_modules', name, n)

        # then temp project dir
        if not os.path.exists(src_path):
            src_path = os.path.join(build_dir, 'node_modules', name, n)

        if not (os.path.exists(src_path) and os.path.isfile(src_path)):
            raise FileNotFoundError(src_path)

        dest_dirpath = os.path.join(dest_npm_path, name)

        if not (os.path.exists(dest_dirpath) and os.path.isdir(dest_dirpath)):
            os.makedirs(dest_dirpath, exist_ok=True)

        dest_path = os.path.join(dest_dirpath, n)

        cmd = [
            'esbuild',
            src_path,
            '--bundle',
            '--minify',
            '--sourcemap',
            f'--outfile={dest_path}',
            '--format=esm',
            '--platform=node',
            '--loader:.js=js',
            '--loader:.ts=ts',
            '--loader:.css=css',
            '--loader:.woff=file',
            '--loader:.woff2=file',
            '--loader:.ttf=file',
            '--loader:.svg=file',
            '--loader:.wasm=file',
        ]

        p = npx( # type: ignore
            cmd,
            cwd=build_dir,
            stdout=PIPE,
            stderr=PIPE,
            return_completed_process=True,
        )

        if p.returncode != 0:
            print('compile_npm_package:', p)
            print('stdout:')
            print(p.stdout)
            print('stderr:')
            print(p.stderr)

        assert p.returncode == 0

        if pkg_name not in paths:
            paths[pkg_name] = {}

        paths[pkg_name][os.path.join(name, n)] = os.path.relpath(dest_path)

    return paths
