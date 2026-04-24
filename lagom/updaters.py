from typing import List, Type, Union

from lagom.definitions import SingletonWrapper, ConstructionWithoutContainer
from lagom.interfaces import ExtendableContainer, WriteableContainer, ReadableContainer


def update_container_singletons(
    container: Union[ExtendableContainer, WriteableContainer], singletons: List[Type]
):
    raise NotImplementedError


def _define_singleton_in_new_container(
    new_container: WriteableContainer, container: ReadableContainer, dep: Type
):
    raise NotImplementedError
