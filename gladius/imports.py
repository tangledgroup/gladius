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
        current_path = inspect.getfile(obj)
    elif isinstance(obj, Callable):
        current_path = inspect.getfile(obj)
    elif isinstance(obj, str):
        current_path = obj
    else:
        raise ValueError(f"Unsupported type: {type(obj)}")

    # Normalize and check if already processed
    current_path = os.path.abspath(current_path).replace(os.path.sep, '/')
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
