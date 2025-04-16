import os
import json
import hashlib
from typing import Any

import json5
from deepmerge import always_merger


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


def hash_npm_packages(npm_packages: dict[str, Any]) -> str:
    m = hashlib.sha256()
    m.update(json.dumps(npm_packages).encode())
    h = m.hexdigest()
    h = h[:7] # inspired by git which uses first 7 characters
    return h
