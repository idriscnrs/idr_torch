#! /usr/bin/env python
# -*- coding: utf-8 -*-

import warnings
from typing import List, Set, Tuple, Type, Union


class IdrTorchWarning(RuntimeWarning):
    """
    Type (subtype of RuntimeWarning) of all warnings raised by idr_torch.
    You can use it to customize warning filters.
    """

    pass


class WarningFilter:
    def __init__(self):
        self.registry: Set[Tuple[str, Union[Type[str], Type[Warning]]]] = set()

    def block(self, warning: Union[str, Warning]) -> bool:
        text = str(warning)
        category = warning.__class__
        if not isinstance(warning, IdrTorchWarning):
            return False
        message = (text, category)
        if message not in self.registry:
            self.registry.add(message)
            return False
        return True

    def warn(self, warning_list: List[warnings.WarningMessage]):
        for warning in warning_list:
            if not self.block(warning.message):
                category = (
                    warning.message.__class__
                    if isinstance(warning.message, Warning)
                    else Warning
                )
                warnings.warn(
                    message=str(warning.message),
                    category=category,
                    stacklevel=3,
                )


warning_filter = WarningFilter()
