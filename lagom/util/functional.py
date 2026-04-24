"""Code to help understand functions
"""

import inspect
from typing import Callable, TypeVar, Generic, Iterator


def arity(func: Callable) -> int:
    """Returns the arity(number of args)
    Given a callable this function returns the number of arguments it expects
    >>> arity(lambda: 5)
    0
    >>> arity(lambda x: x)
    1

    :param func:
    :return:
    """
    raise NotImplementedError


F = TypeVar("F", bound=Callable)


class FunctionCollection(Generic[F]):
    """
    Represents a collection of functions that is hashable.
    """

    def __init__(self, *checkers: F):
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __contains__(self, item) -> bool:
        raise NotImplementedError

    def __iter__(self) -> Iterator[F]:
        raise NotImplementedError

    def __hash__(self):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError
