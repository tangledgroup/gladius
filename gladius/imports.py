__all__ = [
    'JsModuleType',
    'TsModuleType',
    'JsxModuleType',
    'TsxModuleType',
    'WasmModuleType',
    'CssModuleType',
    'local_import_tracker',
]

import sys
import importlib.util
import importlib.machinery
from pathlib import Path
from types import ModuleType


project_root = Path.cwd().resolve()


#
# Module type implementations
#
class JsModuleType(ModuleType):
    def __init__(self, name, path):
        super().__init__(name)
        self.path = path


class TsModuleType(ModuleType):
    def __init__(self, name, path):
        super().__init__(name)
        self.path = path


class JsxModuleType(ModuleType):
    def __init__(self, name, path):
        super().__init__(name)
        self.path = path


class TsxModuleType(ModuleType):
    def __init__(self, name, path):
        super().__init__(name)
        self.path = path


class WasmModuleType(ModuleType):
    def __init__(self, name, path):
        super().__init__(name)
        self.path = path


class CssModuleType(ModuleType):
    def __init__(self, name, path):
        super().__init__(name)
        self.path = path

#
# Loader implementations
#
class BaseLoader:
    def __init__(self, path, module_type):
        self.path = path
        self.module_type = module_type


    def create_module(self, spec):
        return self.module_type(spec.name, str(self.path))


    def exec_module(self, module):
        # Implement execution logic for different module types
        pass


class JsLoader(BaseLoader):
    def __init__(self, path):
        super().__init__(path, JsModuleType)


class TsLoader(BaseLoader):
    def __init__(self, path):
        super().__init__(path, TsModuleType)


class JsxLoader(BaseLoader):
    def __init__(self, path):
        super().__init__(path, JsxModuleType)


class TsxLoader(BaseLoader):
    def __init__(self, path):
        super().__init__(path, TsxModuleType)


class WasmLoader(BaseLoader):
    def __init__(self, path):
        super().__init__(path, WasmModuleType)


class CssLoader(BaseLoader):
    def __init__(self, path):
        super().__init__(path, CssModuleType)


#
# LocalImportTracker
#
class LocalImportTracker:
    EXTENSIONS = ['.tsx', '.ts', '.jsx', '.js', '.wasm', '.css']

    LOADER_MAP = {
        '.js': JsLoader,
        '.ts': TsLoader,
        '.jsx': JsxLoader,
        '.tsx': TsxLoader,
        '.wasm': WasmLoader,
        '.css': CssLoader,
    }

    def __init__(self):
        self.local_imports = {}

    def find_spec(self, fullname, path, target=None):
        # Check for custom extensions first
        for ext in self.EXTENSIONS:
            module_path = self._get_module_path(fullname, ext)
            if module_path.exists():
                self._create_parent_namespaces(fullname)
                self.local_imports[fullname] = str(module_path)
                return importlib.util.spec_from_loader(
                    fullname,
                    self.LOADER_MAP[ext](module_path),
                    origin=str(module_path)
                )

        # Fall back to Python modules
        return self._track_python_module(fullname, path)

    def _get_module_path(self, fullname, ext):
        return (project_root / '/'.join(fullname.split('.'))).with_suffix(ext)

    def _create_parent_namespaces(self, fullname):
        # Existing implementation remains the same
        parts = fullname.split('.')
        for i in range(len(parts) - 1):
            parent_name = '.'.join(parts[:i+1])
            parent_dir = project_root / '/'.join(parts[:i+1])

            if parent_dir.is_dir() and parent_name not in sys.modules:
                spec = importlib.machinery.ModuleSpec(
                    parent_name,
                    None,
                    is_package=True,
                    submodule_search_locations=[str(parent_dir)]
                )
                module = importlib.util.module_from_spec(spec)
                sys.modules[parent_name] = module
                self.local_imports[parent_name] = str(parent_dir)

    def _track_python_module(self, fullname, path):
        # Existing implementation remains the same
        if self in sys.meta_path:
            sys.meta_path.remove(self)
            try:
                spec = importlib.util.find_spec(fullname, path)
            finally:
                sys.meta_path.insert(0, self)
        else:
            spec = importlib.util.find_spec(fullname, path)

        if spec and getattr(spec, 'origin', None):
            try:
                origin_path = Path(spec.origin).resolve()
                if project_root in origin_path.parents:
                    self.local_imports[fullname] = str(origin_path)
            except (ValueError, AttributeError):
                pass
        return None


# Install the hook
local_import_tracker = LocalImportTracker()
sys.meta_path.insert(0, local_import_tracker)
