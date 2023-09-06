#! /usr/bin/env python
# -*- coding: utf-8 -*-

import warnings
from collections.abc import Iterable
from importlib.metadata import version
from inspect import isclass
from pathlib import Path
from typing import Any, List

from . import __name__, __path__
from .api import API, AutoMasterAddressPort, DefaultAPI, decorate_methods
from .utils import IdrTorchWarning, warning_filter

__version__ = version(__name__)


class EmptyClass(object):
    pass


class Interface(object):
    def __init__(self):
        self._available_APIs: List[API] = []
        self.crawl_shipped_APIs()
        self.add_other_object_for_easy_access()
        self.add_API_functions()
        self.make_dir()

    @classmethod
    def add_attribute(cls, name, attribute) -> None:
        setattr(cls, name, attribute)

    def add_API_functions(self) -> None:
        from . import config

        for method_name in config.__all__:
            self.add_attribute(
                method_name, self.make_new_func(getattr(config, method_name).__name__)
            )

    def make_dir(self):
        from . import config

        self.__dir: List[str] = []
        self.__dir += dir(EmptyClass())
        self.__dir += config.__all__
        self.__dir += self.__all__
        self.__dir += [
            "__version__",
        ]

    def crawl_shipped_APIs(self) -> None:
        from . import api

        self.crawl_module_for_APIs(api)

    def add_other_object_for_easy_access(self) -> None:
        from . import api
        from .api import modifiers

        self.api = api
        self.API = API
        self.AutoMasterAddressPort = AutoMasterAddressPort
        self.decorate_methods = decorate_methods
        self.IdrTorchWarning = IdrTorchWarning
        self.modifiers = modifiers
        self.__file__ = str(Path(__file__).parent / "__init__.py")
        self.__path__ = __path__
        self.__name__ = __name__
        self.__version__ = __version__
        self.__all__ = [
            "api",
            "API",
            "AutoMasterAddressPort",
            "decorate_methods",
            "IdrTorchWarning",
            "modifiers",
            "register_API",
            "get_launcher_API",
            "current_API",
            "all_APIs",
            "crawl_module_for_APIs",
        ]

    def __repr__(self) -> str:
        return f"<module '{self.__name__}' from '{self.__file__}'"

    def __dir__(self) -> Iterable[str]:
        return self.__dir

    def make_new_func(self, dest_name: str) -> property:
        def redirect(self: Interface) -> Any:
            with warnings.catch_warnings(record=True) as warning_list:
                api = self.get_launcher_API()
                output = getattr(api, dest_name)()
            if warning_list:
                warning_filter.warn(warning_list)
            return output

        return property(redirect)

    def register_API(self, new_API: API) -> None:
        for i, api in enumerate(self._available_APIs):
            if api.priority > new_API.priority:
                continue
            else:
                self._available_APIs.insert(i, new_API)
                break
        else:
            self._available_APIs.append(new_API)

    def get_launcher_API(self) -> API:
        for api in self._available_APIs:
            if api.is_launcher():
                return api
        return DefaultAPI()

    @property
    def current_API(self) -> str:
        return self.get_launcher_API().name

    @property
    def all_APIs(self) -> List[API]:
        return self._available_APIs

    def crawl_module_for_APIs(self, module) -> None:
        for obj_name in dir(module):
            obj = getattr(module, obj_name)
            if isclass(obj) and issubclass(obj, API) and obj is not API:
                # obj is the class so we instanciate it
                self.register_API(obj())
            elif isinstance(obj, API) and obj.__class__ is not API:
                # obj is already the instance
                self.register_API(obj)
