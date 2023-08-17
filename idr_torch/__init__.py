import sys

from .interface import Interface

# These imports won't be available at runtime, but will help VSCode completion.
from .api import (
    modifiers as modifiers,
    API as API,
    AutoMasterAddressPort as AutoMasterAddressPort,
    decorate_methods as decorate_methods,
)
from .config import *
from .utils import IdrTorchWarning as IdrTorchWarning

sys.modules[__name__] = Interface()
