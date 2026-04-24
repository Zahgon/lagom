"""Extra information about the reflection API
"""

import inspect
from functools import lru_cache
from typing import (
    Dict,
    Type,
    Callable,
    get_type_hints,
    Optional,
    Awaitable,
    Any,
    Mapping,
    Sequence,
)

import typing

RETURN_ANNOTATION = "return"


_TYPE_AWAITABLE = type(typing.Awaitable)


class FunctionSpec:
    """
    Describes the arguments of a function
    """

    args: Sequence[str]
    annotations: Mapping[str, Type]
    defaults: Mapping[str, Any]
    return_type: Optional[Type]
    arity: int

    def __init__(self, args, annotations, defaults, return_type):
        raise NotImplementedError

    def __repr__(self):
        def _arg_type_string(arg):
            raise NotImplementedError

        raise NotImplementedError

    def without_argument(self, arg_to_remove: str):
        """
        Returns the function spec with the specified argument removed
        :param arg_to_remove:
        :return:
        """
        raise NotImplementedError


class CachingReflector:
    """
    Takes a function and returns an object representing
    the function's type signature. Results are cached
    so subsequent calls do not need to call the reflection
    API.
    """

    @property
    def overview_of_cache(self) -> Dict[str, str]:
        """
        Gives a humanish readable representation of what has been reflected on.
        Removed since lru cache is now used
        :return:
        """
        pass

    @lru_cache(maxsize=1024)
    def get_function_spec(self, func) -> FunctionSpec:
        """
        Returns details about the function's signature
        :param func:
        :return:
        """
        raise NotImplementedError


def reflect(func: Callable) -> FunctionSpec:
    """
    Extension to inspect.getfullargspec with a little more.
    :param func:
    :return:
    """
    raise NotImplementedError


def _get_default_args(func):
    raise NotImplementedError


def remove_optional_type(dep_type) -> Optional[Type]:
    """if the Type is Optional[T] returns T else None

    :param dep_type:
    :return:
    """
    raise NotImplementedError


def remove_awaitable_type(dep_type) -> Optional[Type]:
    """if the Type is Awaitable[T] returns T else None

    :param dep_type:
    :return:
    """
    raise NotImplementedError
