__all__ = [
    # 'capture_imports',
    'local_import_tracker',
]

import sys
import importlib.util
from pathlib import Path


project_root = Path.cwd()


class LocalImportTracker:
    def __init__(self):
        self.local_imports = {}


    def find_spec(self, fullname, path, target=None):
        # Temporary removal to prevent recursion
        if self in sys.meta_path:
            sys.meta_path.remove(self)

            try:
                spec = importlib.util.find_spec(fullname, path)
            finally:
                sys.meta_path.insert(0, self)
        else:
            spec = importlib.util.find_spec(fullname, path)

        if spec and spec.origin:
            try:
                origin_path = Path(spec.origin).resolve()

                # Check if it's a package with __init__.py
                if (spec.submodule_search_locations is not None and
                    origin_path.name == '__init__.py'):
                    # For packages, keep the __init__.py path
                    module_path = origin_path
                else:
                    # For regular modules, use the file path directly
                    module_path = origin_path

                if project_root in module_path.parents:
                    self.local_imports[fullname] = str(module_path)
            except (ValueError, AttributeError):
                pass

        return None # Defer to other finders


# Install the hook
local_import_tracker = LocalImportTracker()
sys.meta_path.insert(0, local_import_tracker)
