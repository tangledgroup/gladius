import sys
from . import mock_module
sys.modules['browser'] = mock_module
sys.modules['javascript'] = mock_module

from .gladius import * # noqa
from .element import * # noqa
