import functools
import io
import logging
import typing

from .compilaton import mypyc_attr

from types import FunctionType, MethodType
from typing import (
    Dict,
    Type,
    Any,
    TypeVar,
    Callable,
    Set,
    List,
    Optional,
    cast,
    Union,
)

from .definitions import (
    normalise,
    Singleton,
    Alias,
    ConstructionWithoutContainer,
    UnresolvableTypeDefinition,
)
from .exceptions import (
    UnresolvableType,
    DuplicateDefinition,
    InvalidDependencyDefinition,
    RecursiveDefinitionError,
    DependencyNotDefined,
    TypeOnlyAvailableAsAwaitable,
    CircularDefinitionError,
)
from .interfaces import (
    SpecialDepDefinition,
    WriteableContainer,
    TypeResolver,
    DefinitionsSource,
    ExtendableContainer,
    ContainerDebugInfo,
    CallTimeContainerUpdate,
)
from .markers import injectable
from .updaters import update_container_singletons
from .util.logging import NullLogger
from .util.reflection import (
    FunctionSpec,
    CachingReflector,
    remove_optional_type,
    remove_awaitable_type,
)
from .wrapping import apply_argument_updater

UNRESOLVABLE_TYPES = [
    str,
    int,
    float,
    bool,
    bytes,
    bytearray,
    io.BytesIO,
    io.BufferedIOBase,
    io.BufferedRandom,
    io.BufferedReader,
    io.BufferedRWPair,
    io.BufferedWriter,
    io.FileIO,
    io.IOBase,
    io.RawIOBase,
    io.TextIOBase,
    typing.IO,
    typing.TextIO,
    typing.BinaryIO,
]

X = TypeVar("X")

Unset: Any = object()


@mypyc_attr(allow_interpreted_subclasses=True)
class Container(
    WriteableContainer, ExtendableContainer, DefinitionsSource, ContainerDebugInfo
):
    """Dependency injection container

    Lagom is a dependency injection container designed to give you "just enough"
    help with building your dependencies. The intention is that almost
    all of your code doesn't know about or rely on lagom. Lagom will
    only be involved at the top level to pull everything together.

    >>> from tests.examples import SomeClass
    >>> c = Container()
    >>> c[SomeClass]
    <tests.examples.SomeClass object at ...>

    Objects are constructed as they are needed

    >>> from tests.examples import SomeClass
    >>> c = Container()
    >>> first = c[SomeClass]
    >>> second = c[SomeClass]
    >>> first != second
    True

    And construction logic can be defined
    >>> from tests.examples import SomeClass, SomeExtendedClass
    >>> c = Container()
    >>> c[SomeClass] = SomeExtendedClass
    >>> c[SomeClass]
    <tests.examples.SomeExtendedClass object at ...>
    """

    _registered_types: Dict[Type, SpecialDepDefinition]
    _parent_definitions: DefinitionsSource
    _reflector: CachingReflector
    _undefined_logger: logging.Logger

    def __init__(
        self,
        container: Optional["Container"] = None,
        log_undefined_deps: Union[bool, logging.Logger] = False,
    ):
        """
        :param container: Optional container if provided the existing definitions will be copied
        :param log_undefined_deps indicates if a log message should be emmited when an undefined dep is loaded
        """

        # ContainerDebugInfo is always registered
        # This means consumers can consume an overview of the container
        # without hacking anything custom together.
        raise NotImplementedError

    def define(self, dep: Type[X], resolver: TypeResolver[X]) -> SpecialDepDefinition:
        """Register how to construct an object of type X

        >>> from tests.examples import SomeClass
        >>> c = Container()
        >>> c.define(SomeClass, lambda: SomeClass())
        <lagom.definitions.ConstructionWithoutContainer ...>

        :param dep: The type to be constructed
        :param resolver: A definition of how to construct it
        :return:
        """
        raise NotImplementedError

    @property
    def defined_types(self) -> Set[Type]:
        """The types the container has explicit build instructions for

        :return:
        """
        pass

    @property
    def reflection_cache_overview(self) -> Dict[str, str]:
        pass

    def temporary_singletons(
        self, singletons: Optional[List[Type]] = None
    ) -> "_TemporaryInjectionContext":
        """
        Returns a context that loads a new container with singletons that only exist
        for the context.

        >>> from tests.examples import SomeClass
        >>> base_container = Container()
        >>> def my_func():
        ...     with base_container.temporary_singletons([SomeClass]) as c:
        ...         assert c[SomeClass] is c[SomeClass]
        >>> my_func()

        :param singletons: items which should be considered singletons within the context
        :return:
        """
        raise NotImplementedError

    def resolve(
        self, dep_type: Type[X], suppress_error=False, skip_definitions=False
    ) -> X:
        """Constructs an object of type X

         If the object can't be constructed an exception will be raised unless
         supress errors is true

        >>> from tests.examples import SomeClass
        >>> c = Container()
        >>> c.resolve(SomeClass)
        <tests.examples.SomeClass object at ...>

        >>> from tests.examples import SomeClass
        >>> c = Container()
        >>> c.resolve(int)
        Traceback (most recent call last):
        ...
        lagom.exceptions.UnresolvableType: ...

        Optional wrappers are stripped out to be what is being asked for
        >>> from tests.examples import SomeClass
        >>> c = Container()
        >>> c.resolve(Optional[SomeClass])
        <tests.examples.SomeClass object at ...>

        :param dep_type: The type of object to construct
        :param suppress_error: if true returns None on failure
        :param skip_definitions:
        :return:
        """
        raise NotImplementedError

    def _resolve(
        self,
        dep_type: Type[X],
        suppress_error=False,
        skip_definitions=False,
        default: X = Unset,
        type_stack: Optional[Set[Type]] = None,
    ) -> X:
        raise NotImplementedError

    def partial(
        self,
        func: Callable[..., X],
        shared: Optional[List[Type]] = None,
        container_updater: Optional[CallTimeContainerUpdate] = None,
    ) -> Callable[..., X]:
        """Takes a callable and returns a callable bound to the container
        When invoking the new callable if any arguments have a default set
        to the special marker object "injectable" then they will be constructed by
        the container. For automatic injection without the marker use "magic_partial"
        >>> from tests.examples import SomeClass
        >>> c = Container()
        >>> def my_func(something: SomeClass = injectable):
        ...     return f"Successfully called with {something}"
        >>> bound_func = c.magic_partial(my_func)
        >>> bound_func()
        'Successfully called with <tests.examples.SomeClass object at ...>'

        :param func: the function to bind to the container
        :param shared: items which should be considered singletons on a per call level
        :param container_updater: An optional callable to update the container before resolution
        :return:
        """
        def _update_args(supplied_args, supplied_kwargs):
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
        """Takes a callable and returns a callable bound to the container
        When invoking the new callable if any arguments can be constructed by the container
        then they can be ommited.
        >>> from tests.examples import SomeClass
        >>> c = Container()
        >>> def my_func(something: SomeClass):
        ...   return f"Successfully called with {something}"
        >>> bound_func = c.magic_partial(my_func)
        >>> bound_func()
        'Successfully called with <tests.examples.SomeClass object at ...>'

        :param func: the function to bind to the container
        :param shared: items which should be considered singletons on a per call level
        :param keys_to_skip: named arguments which the container shouldnt build
        :param skip_pos_up_to: positional arguments which the container shouldnt build
        :param container_updater: An optional callable to update the container before resolution
        :return:
        """
        def _update_args(supplied_args, supplied_kwargs):
            raise NotImplementedError

        raise NotImplementedError

    def clone(self) -> "Container":
        """returns a copy of the container
        :return:
        """
        raise NotImplementedError

    def get_definition(self, dep_type: Type[X]) -> Optional[SpecialDepDefinition[X]]:
        """
        Will return the definition in this container. If none has been defined any
        definition in the parent container will be used.

        :param dep_type:
        :return:
        """
        raise NotImplementedError

    def __getitem__(self, dep: Type[X]) -> X:
        raise NotImplementedError

    def __setitem__(self, dep: Type[X], resolver: TypeResolver[X]):
        raise NotImplementedError

    def _reflection_build_with_err_handling(
        self,
        dep_type: Type[X],
        suppress_error: bool,
        *,
        default: X = Unset,
        type_stack: Optional[Set[Type]] = None,
    ) -> X:
        raise NotImplementedError

    def _reflection_build(
        self,
        dep_type: Type[X],
        *,
        default: X = Unset,
        type_stack: Optional[Set[Type]] = None,
    ) -> X:
        raise NotImplementedError

    def _infer_dependencies(
        self,
        spec: FunctionSpec,
        suppress_error=False,
        keys_to_skip: Optional[List[str]] = None,
        skip_pos_up_to=0,
        types_to_skip: Optional[Set[Type]] = None,
        type_stack: Optional[Set[Type]] = None,
    ):
        raise NotImplementedError

    def _get_spec_without_self(self, func: Callable[..., X]) -> FunctionSpec:
        raise NotImplementedError


@mypyc_attr(allow_interpreted_subclasses=True)
class ExplicitContainer(Container):
    def resolve(
        self, dep_type: Type[X], suppress_error=False, skip_definitions=False
    ) -> X:
        raise NotImplementedError

    def define(self, dep, resolver):
        raise NotImplementedError

    def clone(self):
        """returns a copy of the container
        :return:
        """
        raise NotImplementedError


class EmptyDefinitionSet(DefinitionsSource):
    """
    Represents the starting state for a collection of dependency definitions
    i.e. None and everything has to be built with reflection
    """

    def get_definition(self, dep_type: Type[X]) -> Optional[SpecialDepDefinition[X]]:
        """
        No types are defined in the empty set
        :param dep_type:
        :return:
        """
        return None

    @property
    def defined_types(self) -> Set[Type]:
        pass


class _TemporaryInjectionContext:
    _base_container: Container

    def __init__(
        self,
        container: Container,
        update_function: Optional[Callable[[Container], Container]] = None,
    ):
        raise NotImplementedError

    def __enter__(self) -> Container:
        raise NotImplementedError

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def _update_nothing(_c: WriteableContainer, _a: typing.Collection, _k: Dict):
    pass
