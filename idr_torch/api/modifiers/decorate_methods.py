#! /usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Callable, Type

from ...config import __all__ as all_API_methods
from .. import API


def decorate_methods(cls: Type[API], func_to_apply: Callable) -> Type[API]:
    for obj_name in dir(cls):
        if obj_name in all_API_methods:
            decorated = func_to_apply(getattr(cls, obj_name))
            setattr(cls, obj_name, decorated)

    return cls
