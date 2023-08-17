#! /usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps
import os

from .decorate_methods import decorate_methods
from .. import API


env_variables_set: bool = False

def set_master_addr_port_env_variables(func):
    @wraps(func)
    def wrapper(self):
        global env_variables_set
        if not env_variables_set:
            env_variables_set = True  # must be done before actually setting the variable to prevent stackoverflow
            os.environ["MASTER_ADDR"] = self.master_address()
            os.environ["MASTER_PORT"] = str(self.port())
        return func(self)
    return wrapper


def AutoMasterAddressPort(cls: API) -> API:
    return decorate_methods(cls, func_to_apply=set_master_addr_port_env_variables)
