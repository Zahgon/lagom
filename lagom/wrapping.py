"""
Code in this module is used to wrap and decorate functions that have been
bound to a container
"""

import functools
import inspect

from .exceptions import UnableToInvokeBoundFunction
from .util.reflection import FunctionSpec


def apply_argument_updater(
    func, argument_updater, spec: FunctionSpec, catch_errors=False
):
    async def _bound_func():
        raise NotImplementedError

    raise NotImplementedError


def _wrap_func_in_error_handling(func, spec: FunctionSpec):
    """
    Takes a func and its spec and returns a function that's the same
    but with more useful TypeError messages
    :param func:
    :param spec:
    :return:
    """

    def _error_handling_func():
        raise NotImplementedError

    raise NotImplementedError
