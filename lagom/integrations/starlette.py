"""
For use with Starlette (https://www.starlette.io/)
"""

from typing import List, Type, Callable, Optional, Union

from starlette.routing import Route, WebSocketRoute
from starlette.endpoints import HTTPEndpoint, WebSocketEndpoint

from ..interfaces import ExtendableContainer

OVERRIDE_HTTP_METHODS = {
    "get",
    "head",
    "post",
    "put",
    "delete",
    "connect",
    "options",
    "trace",
    "patch",
}

OVERRIDE_WEBSOCKET_METHODS = {"on_connect", "on_receive", "on_disconnect"}


class StarletteIntegration:
    """
    Wraps a container and a route method for use in the Starlette framework
    """

    _request_singletons: List[Type]
    _container: ExtendableContainer

    def __init__(
        self,
        container: ExtendableContainer,
        request_singletons: Optional[List[Type]] = None,
    ):
        """
        :param request_singletons: List of types that will be singletons for a request
        :param container:
        """
        raise NotImplementedError

    def route(
        self,
        path: str,
        endpoint: Callable,
        *,
        methods: Optional[List[str]] = None,
        name: Optional[str] = None,
        include_in_schema: bool = True,
    ) -> Route:
        """Returns an instance of a starlette Route
        The callable endpoint is bound to the container so dependencies can be
        injected. All other arguments are passed on to starlette.
        :param path:
        :param endpoint:
        :param methods:
        :param name:
        :param include_in_schema:
        :return:
        """
        pass

    def magic_route(
        self,
        path: str,
        endpoint: Callable,
        *,
        methods: Optional[List[str]] = None,
        name: Optional[str] = None,
        include_in_schema: bool = True,
    ) -> Route:
        """Returns an instance of a starlette Route
        The callable endpoint is bound to the container so dependencies can be
        auto injected. All other arguments are passed on to starlette.
        :param path:
        :param endpoint:
        :param methods:
        :param name:
        :param include_in_schema:
        :return:
        """
        pass

    def ws_route(
        self,
        path: str,
        endpoint: Callable,
        *,
        name: Optional[str] = None,
    ) -> WebSocketRoute:
        """Returns an instance of a starlette WebSocketRoute
        The callable endpoint is bound to the container so dependencies can be
        injected. All other arguments are passed on to starlette.
        :param path:
        :param endpoint:
        :param name:
        :return:
        """
        pass

    def ws_magic_route(
        self,
        path: str,
        endpoint: Callable,
        *,
        name: Optional[str] = None,
    ) -> WebSocketRoute:
        """Returns an instance of a starlette WebSocketRoute
        The callable endpoint is bound to the container so dependencies can be
        auto injected. All other arguments are passed on to starlette.
        :param path:
        :param endpoint:
        :param name:
        :return:
        """
        pass

    def wrapped_endpoint_factory(
        self, endpoint: Union[Callable, Type[HTTPEndpoint]], partial_provider: Callable
    ):
        """Builds an instance of a starlette Route with endpoint callables
        bound to the container so dependencies can be auto injected.

        :param endpoint:
        :param partial_provider:
        """
        pass

    @staticmethod
    def create_http_endpoint_proxy(
        endpoint_cls: Type[HTTPEndpoint],
        partial_provider: Callable,
        request_singletons: List[Type],
    ) -> Type[HTTPEndpoint]:
        """Create a subclass of Starlette's HTTPEndpoint which injects dependencies
        into HTTP-method-named methods on the user's `endpoint_cls` subclass of HTTPEndpoint

        :param endpoint_cls:
        :param partial_provider:
        :param request_singletons:
        """
        def __init__(self, scope, receive, send):
            raise NotImplementedError

        def __getattribute__(self, name):
            raise NotImplementedError

        pass

    @staticmethod
    def create_websocket_endpoint_proxy(
        endpoint_cls: Type[WebSocketEndpoint],
        partial_provider: Callable,
        request_singletons: List[Type],
    ) -> Type[WebSocketEndpoint]:
        """Create a subclass of Starlette's WebSocketEndpoint which injects dependencies
        into relevant methods on the user's `endpoint_cls` subclass of WebSocketEndpoint

        :param endpoint_cls:
        :param partial_provider:
        :param request_singletons:
        """
        def __init__(self, scope, receive, send):
            raise NotImplementedError

        def __getattribute__(self, name):
            raise NotImplementedError

        pass
