"""
Similar to the main definitions module but these definitions do not
yet have a stable interface.
"""

from ..definitions import X, ConstructionWithContainer
from ..interfaces import SpecialDepDefinition, ReadableContainer


class PlainFunction(SpecialDepDefinition[X]):
    """Preserves a function without any dep injection performed on it"""

    callable_func: X

    def __init__(self, callable_func: X):
        """"""
        raise NotImplementedError

    def get_instance(self, _container: ReadableContainer) -> X:
        raise NotImplementedError


class AsyncConstructionWithContainer(ConstructionWithContainer):
    pass
