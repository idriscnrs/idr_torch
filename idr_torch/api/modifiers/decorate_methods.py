#! /usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Callable

from .. import API
from ...config import __all__ as all_API_methods


def decorate_methods(cls: API, func_to_apply: Callable) -> Callable:

    for obj_name in dir(cls):
        if obj_name in all_API_methods:
            decorated = func_to_apply(getattr(cls, obj_name))
            setattr(cls, obj_name, decorated)

    return cls
