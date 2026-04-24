import inspect
import logging
from asyncio import Lock
from contextlib import AsyncExitStack
from copy import copy
from typing import (
    Optional,
    Type,
    TypeVar,
    Awaitable,
    Generic,
    Collection,
    Union,
    ContextManager,
    AsyncContextManager,
    Iterator,
    Generator,
    AsyncGenerator,
    Callable,
    List,
)

from lagom.container import Container
from lagom.definitions import Alias, ConstructionWithContainer, SingletonWrapper
from lagom.exceptions import InvalidDependencyDefinition, MissingFeature
from lagom.experimental.definitions import AsyncConstructionWithContainer
from lagom.interfaces import (
    ReadableContainer,
    SpecialDepDefinition,
    CallTimeContainerUpdate,
)

T = TypeVar("T")
X = TypeVar("X")


class AwaitableSingleton(Generic[T]):
    instance: Optional[T]
    constructor: ConstructionWithContainer[Awaitable[T]]
    container: Container
    _lock: Lock

    def __init__(self, constructor: ConstructionWithContainer, container: Container):
        raise NotImplementedError

    async def get(self) -> T:
        raise NotImplementedError


class AsyncContextContainer(Container):
    async_exit_stack: Optional[AsyncExitStack] = None
    _context_types: Collection[Type]
    _context_singletons: Collection[Type]
    _root_context: bool = True

    def __init__(
        self,
        container: Container,
        context_types: Collection[Type],
        context_singletons: Collection[Type] = tuple(),
        log_undefined_deps: Union[bool, logging.Logger] = False,
    ):
        raise NotImplementedError

    def clone(self) -> "AsyncContextContainer":
        """returns a copy of the container
        :return:
        """
        raise NotImplementedError

    async def __aenter__(self):
        raise NotImplementedError

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    def partial(
        self,
        func: Callable[..., X],
        shared: Optional[List[Type]] = None,
        container_updater: Optional[CallTimeContainerUpdate] = None,
    ) -> Callable[..., X]:
        async def _with_context():
            raise NotImplementedError

        raise NotImplementedError

    def magic_partial(
        self,
        func: Callable[..., X],
        shared: Optional[List[Type]] = None,
        keys_to_skip: Optional[List[str]] = None,
        skip_pos_up_to: int = 0,
        container_updater: Optional[CallTimeContainerUpdate] = None,
    ) -> Callable[..., X]:
        async def _with_context():
            raise NotImplementedError

        raise NotImplementedError

    def _context_type_def(self, dep_type: Type):
        pass

    def _context_resolver(self, c: ReadableContainer, type_def: SpecialDepDefinition):
        """
        Takes an existing definition which must be a context manager. Returns
        the value of the context manager from __enter__ and then places the
        __exit__ in this container's exit stack
        """
        pass

    def _async_context_resolver(
        self, c: ReadableContainer, type_def: SpecialDepDefinition
    ):
        """
        Takes an existing definition which must be a context manager. Returns
        the value of the context manager from __aenter__ and then places the
        __aexit__ in this container's exit stack
        """
        pass

    def _singleton_type_def(self, dep_type: Type):
        """
        The same as context_type_def but acts as a singleton within this container
        """
        pass
