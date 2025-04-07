__all__ = [
    'window',
    'document',
    'bind',
    'JSObject',
    'this',
    'Date',
    'JSON',
    'Math',
    'NULL',
    'Number',
    'RegExp',
    'String',
    'UNDEFINED',
    'export',
]

from browser import window, document, bind # type: ignore # noqa
from javascript import JSObject, this, Date, JSON, Math, NULL, Number, RegExp, String, UNDEFINED # type: ignore # noqa
from functools import wraps


def export(func):
    global window
    setattr(window, func.__name__, func) # type: ignore

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
