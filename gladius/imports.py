"""
import os
import ast
import inspect
from types import ModuleType
from typing import Optional, Callable, Dict


def generate_module_map(obj: ModuleType | Callable | str, processed_paths: Optional[set]=None, root_dir: Optional[str]=None) -> Dict[str, str]:
    if processed_paths is None:
        processed_paths = set()

    current_path = None
    if isinstance(obj, ModuleType):
        current_path = os.path.relpath(inspect.getfile(obj), start=os.getcwd())
    elif isinstance(obj, Callable):
        current_path = os.path.relpath(inspect.getfile(obj), start=os.getcwd())
    elif isinstance(obj, str):
        current_path = obj
    else:
        raise ValueError(f"Unsupported type: {type(obj)}")

    # Normalize and check if already processed
    # current_path = os.path.abspath(current_path).replace(os.path.sep, '/')
    # current_path = current_path.replace(os.path.sep, '/')

    if current_path in processed_paths:
        return {}

    processed_paths.add(current_path)

    # Determine current directory and root directory
    if root_dir is None:
        root_dir = os.path.dirname(current_path) if not os.path.isdir(current_path) else current_path

    current_directory = os.path.dirname(current_path) if not os.path.isdir(current_path) else current_path

    # Handle package directories
    if os.path.isdir(current_path):
        init_path = os.path.join(current_path, '__init__.py')
        if not os.path.exists(init_path):
            return {}
        with open(init_path, 'r') as f:
            source_code = f.read()
    else:
        with open(current_path, 'r') as f:
            source_code = f.read()

    # Parse AST
    try:
        source = ast.parse(source_code)
    except SyntaxError:
        return {}

    module_map = {}
    # module_map[obj.__name__] = current_path

    def process_module_parts(base_dir: str, module_name: str) -> None:
        parts = module_name.split('.')
        accumulated = []
        for part in parts:
            accumulated.append(part)
            current_module = '.'.join(accumulated)
            current_path_part = os.path.join(base_dir, *accumulated)
            init_path = os.path.join(current_path_part, '__init__.py')
            absolute_path = None

            # Check for package
            if os.path.isdir(current_path_part) and os.path.exists(init_path):
                absolute_path = init_path
            # Check for module
            elif os.path.isfile(f"{current_path_part}.py"):
                absolute_path = f"{current_path_part}.py"

            if absolute_path:
                relative_path = os.path.relpath(absolute_path, root_dir).replace(os.path.sep, '/')
                module_map[current_module] = relative_path

    def analyze_import(node):
        if isinstance(node, ast.Import):
            for alias in node.names:
                process_module_parts(current_directory, alias.name)
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module or ''
            if node.level > 0:  # Relative import
                base_dir = current_directory
                for _ in range(node.level - 1):
                    base_dir = os.path.dirname(base_dir)
                if module_name:
                    process_module_parts(base_dir, module_name)
                for alias in node.names:
                    full_module = f"{module_name}.{alias.name}" if module_name else alias.name
                    process_module_parts(base_dir, full_module)
            else:  # Absolute import
                if module_name:
                    process_module_parts(current_directory, module_name)
                for alias in node.names:
                    full_module = f"{module_name}.{alias.name}" if module_name else alias.name
                    process_module_parts(current_directory, full_module)

    # Process all import nodes
    for node in ast.walk(source):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            analyze_import(node)

    # Recursively process all found modules
    for path in list(module_map.values()):
        # Convert relative path to absolute for processing
        absolute_path = os.path.normpath(os.path.join(root_dir, path)).replace(os.path.sep, '/')
        if absolute_path not in processed_paths and os.path.exists(absolute_path):
            sub_map = generate_module_map(
                absolute_path,
                processed_paths=processed_paths.copy(),
                root_dir=root_dir
            )
            module_map.update(sub_map)

    return module_map
"""

"""
def generate_module_map(obj: ModuleType | str, processed_paths: Optional[set]=None, root_dir: Optional[str]=None) -> Dict[str, str]:
    assert isinstance(obj, (str, ModuleType)), obj

    if processed_paths is None:
        processed_paths = set()

    current_path: str

    if isinstance(obj, ModuleType):
        current_path = os.path.relpath(inspect.getfile(obj), start=os.getcwd())
    elif isinstance(obj, Callable):
        current_path = os.path.relpath(inspect.getfile(obj), start=os.getcwd())
    elif isinstance(obj, str):
        current_path = obj
    else:
        raise ValueError(f"Unsupported type: {type(obj)}")

    # Normalize and check if already processed
    # current_path = os.path.abspath(current_path).replace(os.path.sep, '/')
    # current_path = current_path.replace(os.path.sep, '/')

    if current_path in processed_paths:
        return {}

    processed_paths.add(current_path)

    # Determine current directory and root directory
    if root_dir is None:
        root_dir = os.path.dirname(current_path) if not os.path.isdir(current_path) else current_path

    current_directory = os.path.dirname(current_path) if not os.path.isdir(current_path) else current_path

    # Handle package directories
    if os.path.isdir(current_path):
        init_path = os.path.join(current_path, '__init__.py')

        if not os.path.exists(init_path):
            return {}

        with open(init_path, 'r') as f:
            source_code = f.read()
    else:
        with open(current_path, 'r') as f:
            source_code = f.read()

    # Parse AST
    try:
        source = ast.parse(source_code)
    except SyntaxError:
        return {}

    module_map = {}

    if isinstance(obj, ModuleType):
        module_map[obj.__name__] = current_path
    else:
        module_map[obj] = current_path

    def process_module_parts(base_dir: str, module_name: str) -> None:
        print(f'process_module_parts: {base_dir=}, {module_name=}')
        parts = module_name.split('.')
        accumulated = []

        for part in parts:
            accumulated.append(part)
            current_module = '.'.join(accumulated)
            current_path_part = os.path.join(base_dir, *accumulated)
            init_path = os.path.join(current_path_part, '__init__.py')
            absolute_path = None

            # Check for package
            if os.path.isdir(current_path_part) and os.path.exists(init_path):
                absolute_path = init_path

            # Check for module
            elif os.path.isfile(f"{current_path_part}.py"):
                absolute_path = f"{current_path_part}.py"

            if absolute_path:
                # relative_path = os.path.relpath(absolute_path, root_dir).replace(os.path.sep, '/')
                # module_map[current_module] = relative_path
                relative_path = absolute_path.replace(os.path.sep, '/')
                # module_name = '.'.join([base_dir, module_name])
                # module_map[module_name] = relative_path
                module_map[current_module] = relative_path

    def analyze_import(node):
        if isinstance(node, ast.Import):
            for alias in node.names:
                process_module_parts(current_directory, alias.name)
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module or ''

            if node.level > 0:  # Relative import
                base_dir = current_directory

                for _ in range(node.level - 1):
                    base_dir = os.path.dirname(base_dir)

                if module_name:
                    process_module_parts(base_dir, module_name)

                for alias in node.names:
                    full_module = f"{module_name}.{alias.name}" if module_name else alias.name
                    process_module_parts(base_dir, full_module)
            else:  # Absolute import
                if module_name:
                    process_module_parts(current_directory, module_name)

                for alias in node.names:
                    full_module = f"{module_name}.{alias.name}" if module_name else alias.name
                    process_module_parts(current_directory, full_module)

    # Process all import nodes
    for node in ast.walk(source):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            analyze_import(node)

    # Recursively process all found modules
    for path in list(module_map.values()):
        # Convert relative path to absolute for processing
        absolute_path = os.path.normpath(os.path.join(root_dir, path)).replace(os.path.sep, '/')

        if absolute_path not in processed_paths and os.path.exists(absolute_path):
            sub_map = generate_module_map(
                absolute_path,
                processed_paths=processed_paths.copy(),
                root_dir=root_dir
            )

            module_map.update(sub_map)

    return module_map
"""

"""
import os
import ast
import inspect
from types import ModuleType
from typing import Optional, Callable, Set

def generate_module_map(obj: ModuleType | Callable | str, processed_paths: Optional[Set[str]] = None, root_dir: Optional[str] = None) -> Set[str]:
    # Initialize processed_paths if not provided
    if processed_paths is None:
        processed_paths = set()

    # Determine the current path based on input type
    current_path = None
    if isinstance(obj, ModuleType):
        current_path = os.path.relpath(inspect.getfile(obj), start=os.getcwd())
    elif isinstance(obj, Callable):
        current_path = os.path.relpath(inspect.getfile(obj), start=os.getcwd())
    elif isinstance(obj, str):
        current_path = obj
    else:
        raise ValueError(f"Unsupported type: {type(obj)}")

    # Skip if already processed to prevent infinite recursion
    if current_path in processed_paths:
        return set()

    processed_paths.add(current_path)

    # Set root_dir and current_directory
    if root_dir is None:
        root_dir = os.path.dirname(current_path) if not os.path.isdir(current_path) else current_path
    current_directory = os.path.dirname(current_path) if not os.path.isdir(current_path) else current_path

    # Read source code, handling packages and modules
    if os.path.isdir(current_path):
        init_path = os.path.join(current_path, '__init__.py')
        if not os.path.exists(init_path):
            return set()
        with open(init_path, 'r') as f:
            source_code = f.read()
    else:
        with open(current_path, 'r') as f:
            source_code = f.read()

    # Parse the source code into an AST
    try:
        source = ast.parse(source_code)
    except SyntaxError:
        return set()

    # Initialize set to store paths of imported modules
    imported_paths = set()

    # Helper function to collect paths of modules and their parent packages
    def collect_module_paths(base_dir: str, module_name: str, root_dir: str) -> Set[str]:
        paths = set()
        parts = module_name.split('.')
        current_path = base_dir
        for i, part in enumerate(parts):
            current_path = os.path.join(current_path, part)
            init_path = os.path.join(current_path, '__init__.py')
            if os.path.exists(init_path):
                relative_path = os.path.relpath(init_path, root_dir).replace(os.path.sep, '/')
                paths.add(relative_path)
            else:
                module_file = current_path + '.py'
                if os.path.exists(module_file) and i == len(parts) - 1:
                    relative_path = os.path.relpath(module_file, root_dir).replace(os.path.sep, '/')
                    paths.add(relative_path)
                break  # Stop if module not found
        return paths

    # Helper function to analyze import statements
    def analyze_import(node):
        if isinstance(node, ast.Import):
            for alias in node.names:
                paths = collect_module_paths(current_directory, alias.name, root_dir)
                imported_paths.update(paths)
        elif isinstance(node, ast.ImportFrom):
            base_dir = current_directory
            if node.level > 0:  # Relative import
                for _ in range(node.level - 1):
                    base_dir = os.path.dirname(base_dir)
            if node.module:
                # Include the module itself
                paths = collect_module_paths(base_dir, node.module, root_dir)
                imported_paths.update(paths)
                # Include potential submodules
                for alias in node.names:
                    full_name = f"{node.module}.{alias.name}"
                    paths = collect_module_paths(base_dir, full_name, root_dir)
                    imported_paths.update(paths)
            else:
                # Handle imports like 'from . import module'
                for alias in node.names:
                    paths = collect_module_paths(base_dir, alias.name, root_dir)
                    imported_paths.update(paths)

    # Process all import nodes in the AST
    for node in ast.walk(source):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            analyze_import(node)

    # Recursively process all imported module paths
    for path in list(imported_paths):
        absolute_path = os.path.normpath(os.path.join(root_dir, path)).replace(os.path.sep, '/')
        if absolute_path not in processed_paths and os.path.exists(absolute_path):
            sub_paths = generate_module_map(absolute_path, processed_paths=processed_paths.copy(), root_dir=root_dir)
            imported_paths.update(sub_paths)

    return imported_paths
"""

import sys
from contextlib import contextmanager


@contextmanager
def capture_imports():
    ignored_modules_names: set[str] = set(sys.builtin_module_names) | set(sys.stdlib_module_names)

    cur_modules: dict[str, str] = {
        m.__name__: m.__file__
        for m in sys.modules.values() # type: ignore
        if [n for n in m.__name__.split('.') if n][0] not in ignored_modules_names and
            hasattr(m, '__file__')
    }

    # NOTE: module_map is mutable object, and it is required to be to capture all imports
    module_map: dict[str, str] = {}
    yield module_map

    new_modules = {
        m.__name__: m.__file__
        for m in sys.modules.values()
        if [n for n in m.__name__.split('.') if n][0] not in ignored_modules_names and
            hasattr(m, '__file__')
    }

    module_map.update({
        name: path
        for name, path in new_modules.items() # type: ignore
        if name not in cur_modules
    })
