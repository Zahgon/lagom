"""
Exceptions raised by the library
"""

import inspect
import typing
from abc import ABC
from typing import Type


class LagomException(Exception, ABC):
    """All exceptions in this library are instances of a LagomException"""

    pass


class InjectableNotResolved(RuntimeError, LagomException):
    """
    An instance of injectable was consumed in some user code.
    This should not occur as lagom should have replaced the injectable
    with an object. This likely means the function wasn't bound to
    an injection container.
    """

    pass


class InvalidDependencyDefinition(ValueError, LagomException):
    """The provided construction logic is not valid"""

    pass


class ClassesCannotBeDecorated(SyntaxError, LagomException):
    """Decorating classes is not supported by lagom"""

    dep_type: str

    def __init__(self):
        raise NotImplementedError


class MissingReturnType(SyntaxError, LagomException):
    """The function provided doesnt type hint a return"""

    pass


class DuplicateDefinition(ValueError, LagomException):
    """The type has already been defined somewhere else"""

    pass


class TypeOnlyAvailableAsAwaitable(SyntaxError, LagomException):
    """The type is only available as Awaitable[T]"""

    dep_type: str

    def __init__(self, dep_type: Type):
        """

        :param dep_type: The type that could not be constructed without Awaitable
        """
        raise NotImplementedError


class UnableToInvokeBoundFunction(TypeError, LagomException):
    """A function bound to the container could not be invoked"""

    unresolvable_deps: typing.List[Type]

    def __init__(self, msg, unresolvable_deps):
        raise NotImplementedError


class UnresolvableType(ValueError, LagomException):
    """The type cannot be constructed"""

    dep_type: str

    def __init__(self, dep_type: Type):
        """

        :param dep_type: The type that could not be constructed
        """
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

    def get_unresolvable_deps_sequence(self) -> typing.List[str]:
        """Returns the dependency stack with the last element being the dependency source of the exception"""
        pass


class TypeResolutionBlocked(UnresolvableType):
    """The type was explicitly blocked by configuration"""

    dep_type: str

    def __init__(self, dep_type: typing.Optional[typing.Type], msg: str):
        raise NotImplementedError


class CircularDefinitionError(RuntimeError, LagomException):
    dep_type: Type
    type_stack: typing.Set[Type]

    def __init__(self, dep_type: Type, type_stack: typing.Set[Type]):
        """
        :param dep_type: The type that could not be constructed
        """
        raise NotImplementedError


class RecursiveDefinitionError(SyntaxError, LagomException):
    """Whilst trying to resolve the type python exceeded the recursion depth"""

    dep_type: Type

    def __init__(self, dep_type: Type):
        """
        :param dep_type: The type that could not be constructed
        """
        raise NotImplementedError


class DependencyNotDefined(ValueError, LagomException):
    """The type must be explicitly defined in the container"""

    dep_type: Type

    def __init__(self, dep_type: Type):
        """
        :param dep_type: The type that was not defined
        """
        raise NotImplementedError


class MissingEnvVariable(LagomException):
    """
    Whilst trying to load settings from environment variables one or more required variables had not been set.
    More documentation for this can be found in the lagom.environment module.
    """

    def __init__(self, variable_names: typing.List[str]):
        raise NotImplementedError


class InvalidEnvironmentVariables(LagomException):
    """
    Whilst trying to load settings from environment variables one or more variables failed the validation rules.
    Internally the pydantic library is used to coerce and validate the environment variable from a string into
    a python data type.
    More documentation for this can be found in the lagom.environment module.
    """

    def __init__(self, variable_names: typing.List[str], details: str):
        raise NotImplementedError


class MissingFeature(LagomException):
    """This is raised by code in the experimental module. It represents a feature that is planned but not implemented"""

    pass


def _dep_type_as_string(dep_type: Type):
    pass
