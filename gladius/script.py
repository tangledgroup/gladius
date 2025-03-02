__all__ = ['get_function_body']

import inspect
import textwrap
from types import ModuleType
from typing import Callable

# FIXME: rename `get_function_body` to `get_object_source`
def get_function_body(func: ModuleType | Callable) -> str:
    # Get the full source code of the function
    source = inspect.getsource(func)

    if isinstance(func, ModuleType):
        body = source
    elif isinstance(func, Callable):
        # Split the source at the first occurrence of the colon that starts the body
        try:
            _, body = source.split(':\n', 1)  # Split at first colon followed by newline
        except ValueError:
            # Handle single-line functions (e.g., 'def f(): return')
            _, _, body = source.partition(":")
            body = body.lstrip()  # Remove any leading whitespace after colon
    else:
        raise ValueError(func)

    # Remove common leading whitespace from all lines
    dedented_body = textwrap.dedent(body)

    # Strip empty lines from start/end and return
    return dedented_body.strip("\n")
