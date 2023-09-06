#! /usr/bin/env python
# -*- coding: utf-8 -*-

import warnings
from functools import wraps
from typing import Type

from ...utils import IdrTorchWarning
from .. import API
from .decorate_methods import decorate_methods


def warn(func):
    @wraps(func)
    def wrapper(self):
        warnings.warn(
            message=(
                "Calling idr_torch only makes sense within a distributed execution "
                "but none was detected. You may have forgotten to use a launcher "
                "(such as srun). Back to default (non distributed) values"
            ),
            category=IdrTorchWarning,
            stacklevel=4,
        )
        return func(self)

    return wrapper


def UndistributedWarning(cls: Type[API]) -> Type[API]:
    return decorate_methods(cls, func_to_apply=warn)
