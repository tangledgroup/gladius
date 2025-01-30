import os
import ast
import inspect
from typing import Callable


def generate_module_map(func: Callable | str) -> dict[str, str]:
    # Convert the function to an AST for analysis
    if isinstance(func, Callable):
        source = ast.parse(inspect.getsource(func))
        current_directory = os.path.dirname(inspect.getfile(func))
    elif isinstance(func, str):
        path = func

        with open(path, 'r') as f:
            source = ast.parse(f.read())

        current_directory, _ = os.path.split(path)
    else:
        raise ValueError(func)

    module_map = {}

    def analyze_import(node):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module_name = alias.name
                if '.' in module_name:
                    path = module_name.replace('.', '/') + '.py'
                else:
                    path = module_name + '.py'
                module_map[module_name] = path
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module or ''
            if node.level > 0:  # Relative import
                module_name = '.' * node.level + module_name
                # Handle relative paths
                parts = module_name.split('.')
                while parts and parts[0] == '':
                    parts.pop(0)
                    current_directory = os.path.dirname(current_directory)
                base_path = os.path.join(current_directory, *parts)
                if module_name:
                    full_name = module_name
                    if os.path.isdir(base_path):
                        module_map[full_name] = os.path.join(base_path, '__init__.py').replace(os.path.sep, '/')
                    else:
                        module_map[full_name] = f"{base_path}.py".replace(os.path.sep, '/')
            else:  # Absolute import
                if module_name:
                    module_map[module_name] = module_name.replace('.', '/') + '.py'

    # Traverse through all nodes in the AST
    for node in ast.walk(source):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            analyze_import(node)

    return module_map
