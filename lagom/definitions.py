"""
Classes representing specific ways of representing dependencies
"""

import asyncio
import inspect
from threading import Lock
from typing import (
    Union,
    Type,
    Optional,
    Callable,
    TypeVar,
    NoReturn,
    Iterator,
    Awaitable,
)

from .exceptions import (
    InvalidDependencyDefinition,
    TypeResolutionBlocked,
)
from .interfaces import SpecialDepDefinition, ReadableContainer, TypeResolver
from .util.functional import arity

X = TypeVar("X")
AX = Awaitable[X]


class AsyncConstructionWithoutContainer(SpecialDepDefinition[AX]):
    """Wraps an awaitable for constructing a type"""

    def __init__(self, constructor: Callable[[], AX]):
        raise NotImplementedError

    def get_instance(self, container: ReadableContainer) -> AX:
        raise NotImplementedError

    def __copy__(self):
        raise NotImplementedError


class AsyncConstructionWithContainer(SpecialDepDefinition[AX]):
    """Wraps an awaitable for constructing a type"""

    def __init__(self, constructor: Callable[[ReadableContainer], AX]):
        raise NotImplementedError

    def get_instance(self, container: ReadableContainer) -> Awaitable[AX]:
        raise NotImplementedError

    def __copy__(self):
        raise NotImplementedError


class ConstructionWithoutContainer(SpecialDepDefinition[X]):
    """Wraps a callable for constructing a type"""

    def __init__(self, constructor: Callable[[], X]):
        raise NotImplementedError

    def get_instance(self, container: ReadableContainer) -> X:
        raise NotImplementedError

    def __copy__(self):
        raise NotImplementedError


class ConstructionWithContainer(SpecialDepDefinition[X]):
    """Wraps a callable for constructing a type"""

    def __init__(self, constructor: Callable[[ReadableContainer], X]):
        raise NotImplementedError

    def get_instance(self, container: ReadableContainer) -> X:
        raise NotImplementedError

    def __copy__(self):
        raise NotImplementedError


class YieldWithoutContainer(SpecialDepDefinition[X]):
    """Wraps a callable for constructing a type"""

    def __init__(self, constructor: Callable[[], Iterator[X]]):
        raise NotImplementedError

    def get_instance(self, container: ReadableContainer) -> X:
        raise NotImplementedError

    def __copy__(self):
        raise NotImplementedError


class YieldWithContainer(SpecialDepDefinition[X]):
    """Wraps a generator for constructing a type"""

    def __init__(self, constructor: Callable[[ReadableContainer], Iterator[X]]):
        raise NotImplementedError

    def get_instance(self, container: ReadableContainer) -> X:
        raise NotImplementedError

    def __copy__(self):
        raise NotImplementedError


def async_construction(
    resolver: Callable,
) -> Union[AsyncConstructionWithContainer, AsyncConstructionWithoutContainer]:
    """
    Takes a generator and returns a type definition
    :param reflector:
    :param resolver:
    :return:
    """
    raise NotImplementedError


def construction(
    resolver: Callable,
) -> Union[ConstructionWithContainer, ConstructionWithoutContainer]:
    """
    Takes a generator and returns a type definition
    :param reflector:
    :param resolver:
    :return:
    """
    raise NotImplementedError


def yielding_construction(
    resolver: Callable,
) -> Union[YieldWithContainer, YieldWithoutContainer]:
    """
    Takes a generator and returns a type definition
    :param reflector:
    :param resolver:
    :return:
    """
    raise NotImplementedError


class Alias(SpecialDepDefinition[X]):
    """When one class is asked for the other should be returned"""

    alias_type: Type[X]
    skip_definitions: bool

    def __init__(self, alias_type, skip_definitions=False):
        raise NotImplementedError

    def get_instance(self, container: ReadableContainer) -> X:
        raise NotImplementedError

    def __copy__(self):
        raise NotImplementedError


class SingletonWrapper(SpecialDepDefinition[X]):
    """Builds only once then saves the built instance"""

    singleton_type: SpecialDepDefinition
    _instance: Optional[X]
    _thread_lock: Lock

    def __init__(self, def_to_wrap: SpecialDepDefinition):
        raise NotImplementedError

    def get_instance(self, container: ReadableContainer) -> X:
        raise NotImplementedError

    @property
    def _has_instance(self) -> bool:
        pass

    def _load_instance(self, container):
        raise NotImplementedError


class Singleton(SingletonWrapper[X]):
    """Builds only once then saves the built instance"""

    def __init__(self, singleton_type: TypeResolver):
        raise NotImplementedError


class PlainInstance(SpecialDepDefinition[X]):
    """Wraps an actual object that should just be returned"""

    value: X

    def __init__(self, value):
        raise NotImplementedError

    def get_instance(self, _) -> X:
        raise NotImplementedError


class UnresolvableTypeDefinition(SpecialDepDefinition[NoReturn]):
    """
    Used to represent a type that should not be built by the container
    """

    _dep_type: Optional[Type]
    _msg_or_exception: Union[str, Exception]

    def __init__(
        self, msg_or_exception: Union[str, Exception], dep_type: Optional[Type] = None
    ):
        raise NotImplementedError

    def get_instance(self, container: ReadableContainer) -> NoReturn:
        raise NotImplementedError


def normalise(
    resolver: TypeResolver, skip_alias_definitions=False
) -> SpecialDepDefinition:
    """
    :param resolver:
    :param skip_alias_definitions if an alias is loaded should futher definitions be skipped
    :return:
    """
    raise NotImplementedError
