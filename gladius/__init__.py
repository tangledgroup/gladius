import sys

# server-side uses this to handle changes of client-side Python code and reload app
from . import mock_module

# brython
sys.modules['browser'] = mock_module
sys.modules['javascript'] = mock_module

# pyscript
sys.modules['pyscript'] = mock_module

from .gladius import * # noqa
from .element import * # noqa
