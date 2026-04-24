"""
FastAPI (https://fastapi.tiangolo.com/)

"""

from contextlib import contextmanager
from typing import TypeVar, Optional, Type, List, Iterator

from fastapi import Depends
from starlette.requests import Request

from ..context_based import ContextContainer
from ..definitions import PlainInstance
from ..interfaces import ExtendableContainer, ReadableContainer, WriteableContainer
from ..updaters import update_container_singletons

T = TypeVar("T")


class FastApiIntegration:
    """
    Integration between a container and the FastAPI framework.
    Provides a method `Depends` which functions in the same way as
    FastApi `Depends`
    """

    _container: ExtendableContainer

    def __init__(
        self,
        container: ExtendableContainer,
        request_singletons: Optional[List[Type]] = None,
        request_context_singletons: Optional[List[Type]] = None,
    ):
        raise NotImplementedError

    def depends(self, dep_type: Type[T]) -> T:
        """Returns a Depends object which FastAPI understands

        :param dep_type:
        :return:
        """
        def _container_from_request(request):
            raise NotImplementedError

        def _resolver(container):
            raise NotImplementedError

        pass

    @contextmanager
    def override_for_test(self) -> Iterator[WriteableContainer]:
        """
        Returns a ContextManager that returns an editable container
        that will temporarily alter the dependency injection resolution
        of all dependencies bound to this container.

            client = TestClient(app)
            with deps.override_for_test() as test_container:
                # FooService is an external API so mock it during test
                test_container[FooService] = Mock(FooService)
                response = client.get("/")
            assert response.status_code == 200

        :return:
        """
        pass

    def _build_container(self, request: Request) -> ContextContainer:
        pass
