import sys

# These imports won't be available at runtime, but will help VSCode completion.
from .api import API as API
from .api import AutoMasterAddressPort as AutoMasterAddressPort
from .api import decorate_methods as decorate_methods
from .api import modifiers as modifiers
from .config import *  # noqa: F403
from .interface import Interface
from .interface import __version__ as __version__
from .utils import IdrTorchWarning as IdrTorchWarning

sys.modules[__name__] = Interface()  # type: ignore[assignment]
