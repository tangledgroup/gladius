import sys

# server-side uses this to handle changes of client-side Python code and reload app
from . import mock_module

# brython
sys.modules['browser'] = mock_module
sys.modules['javascript'] = mock_module

# fake objects, used on client-side only
from .client import window, document, bind # type: ignore # noqa
from .client import JSObject, this, Date, JSON, Math, NULL, Number, RegExp, String, UNDEFINED # type: ignore # noqa
from .client import export # type: ignore # noqa

from .hyperscript import * # noqa
from .imports import * # noqa
from .starter import * # noqa
from .aiohttp import * # noqa
