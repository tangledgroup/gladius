import sys

# server-side uses this to handle changes of client-side Python code and reload app
from . import mock_module

# brython
sys.modules['browser'] = mock_module
sys.modules['javascript'] = mock_module

from .aiohttp import run_app # noqa

from .gladius import * # noqa
from .element import * # noqa
from .imports import * # noqa
from .starter import * # noqa
