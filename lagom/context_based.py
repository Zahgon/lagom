import logging
from contextlib import ExitStack
from copy import copy
from typing import (
    Collection,
    Union,
    Type,
    TypeVar,
    Optional,
    cast,
    ContextManager,
    Iterator,
    Generator,
    Callable,
    List,
)

from lagom import Container
from lagom.compilaton import mypyc_attr
from lagom.definitions import ConstructionWithContainer, SingletonWrapper, Alias
from lagom.exceptions import InvalidDependencyDefinition
from lagom.interfaces import (
    ReadableContainer,
    SpecialDepDefinition,
    CallTimeContainerUpdate,
)

X = TypeVar("X")


@mypyc_attr(allow_interpreted_subclasses=True)
class ContextContainer(Container):
    """
    Wraps a regular container but is a ContextManager for use within a `with`.

    >>> from tests.examples import SomeClass, SomeClassManager
    >>> from lagom import Container
    >>> from typing import ContextManager
    >>>
    >>> # The regular container
    >>> c = Container()
    >>>
    >>> # register a context manager for SomeClass
    >>> c[ContextManager[SomeClass]] = SomeClassManager
    >>>
    >>> context_c = ContextContainer(c, context_types=[SomeClass])
    >>> with context_c as c:
    ...     c[SomeClass]
    <tests.examples.SomeClass object at ...>
    """

    exit_stack: Optional[ExitStack] = None
    _context_types: Collection[Type]
    _context_singletons: Collection[Type]

    def __init__(
        self,
        container: Container,
        context_types: Collection[Type],
        context_singletons: Collection[Type] = tuple(),
        log_undefined_deps: Union[bool, logging.Logger] = False,
    ):
        raise NotImplementedError

    def clone(self) -> "ContextContainer":
        """returns a copy of the container
        :return:
        """
        raise NotImplementedError

    def __copy__(self):
        raise NotImplementedError

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    def partial(
        self,
        func: Callable[..., X],
        shared: Optional[List[Type]] = None,
        container_updater: Optional[CallTimeContainerUpdate] = None,
    ) -> Callable[..., X]:
        def _with_context():
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
        def _with_context():
            raise NotImplementedError

        raise NotImplementedError

    def _context_type_def(self, dep_type: Type):
        pass

    def _singleton_type_def(self, dep_type: Type):
        """
        The same as context_type_def but acts as a singleton within this container
        """
        pass

    def _context_resolver(self, c: ReadableContainer, type_def: SpecialDepDefinition):
        """
        Takes an existing definition which must be a context manager. Returns
        the value of the context manager from __enter__ and then places the
        __exit__ in this container's exit stack
        """
        pass
