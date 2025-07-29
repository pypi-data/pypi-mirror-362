from typing import (
    Any,
    AsyncContextManager,
    Awaitable,
    Callable,
    Generic,
    Optional,
    Type,
    TypeVar,
    cast,
)

from asgiref.typing import (
    ASGIReceiveCallable,
    ASGISendCallable,
    HTTPScope,
    Scope,
    WebSocketScope,
)

from asgify.context import HTTPContext, WebSocketContext
from asgify.status import HTTP_503_SERVICE_UNAVAILABLE, HTTP_STATUS_CODES

StateT = TypeVar("StateT")
_HttpContextT = TypeVar("_HttpContextT", bound=HTTPContext)
_WebsocketContextT = TypeVar("_WebsocketContextT", bound=WebSocketContext)


class Asgify(Generic[StateT]):
    """
    ASGI application wrapper for HTTP, WebSocket, and lifespan event handling.

    This class provides a unified interface for handling ASGI protocol events, allowing users to define custom
    HTTP and WebSocket handlers, as well as manage application lifespan events. Supports customization of context
    classes and handler assignment as needed for your ASGI application.
    """

    def __init__(
        self,
        lifespan: Optional[Callable[[], AsyncContextManager[StateT]]] = None,
        http: Optional[Callable[[_HttpContextT], Awaitable[None]]] = None,
        http_context_class: Type[_HttpContextT] = HTTPContext[Any],
        websocket: Optional[
            Callable[[_WebsocketContextT], Awaitable[None]]
        ] = None,
        websocket_context_class: Type[_WebsocketContextT] = WebSocketContext[
            Any
        ],
    ) -> None:
        """
        Initialize the Asgify application.

        Args:
            lifespan: Optional async context manager for application lifespan events. If provided, it is used to manage
                startup and shutdown state, allowing for resource initialization and cleanup.
            http: Optional HTTP handler coroutine. Receives an HTTPContext instance per request.
            http_context_class: Custom class for HTTP context, enabling context extension as needed.
            websocket: Optional WebSocket handler coroutine. Receives a WebSocketContext instance per connection.
            websocket_context_class: Custom class for WebSocket context, enabling context extension as needed.
        """
        self.lifespan = lifespan
        self.http = http
        self._http_context_class = http_context_class
        self.websocket = websocket
        self._websocket_context_class = websocket_context_class

    async def __call__(
        self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable
    ) -> None:
        """
        ASGI entrypoint. Dispatches incoming events to the appropriate handler based on scope type.

        Args:
            scope: ASGI scope dictionary describing the connection (type, path, headers, etc).
            receive: Awaitable callable to receive ASGI messages.
            send: Awaitable callable to send ASGI messages.
        """
        if scope["type"] == "lifespan":
            await self._handle_lifespan(scope, receive, send)

        elif scope["type"] == "http":
            scope = cast(HTTPScope, scope)
            ctx = self._http_context_class(self, scope, receive, send)
            if self.http:
                await self.http(ctx)
            else:
                await ctx.start(HTTP_503_SERVICE_UNAVAILABLE)
                await ctx.end(
                    HTTP_STATUS_CODES[HTTP_503_SERVICE_UNAVAILABLE].encode()
                )

        elif scope["type"] == "websocket":
            scope = cast(WebSocketScope, scope)
            ws_ctx = self._websocket_context_class(self, scope, receive, send)
            if self.websocket:
                await self.websocket(ws_ctx)
            else:
                await ws_ctx.close(reason="Not Implemented")

    async def _handle_lifespan(
        self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable
    ) -> None:
        """
        Internal handler for ASGI lifespan events (startup/shutdown).

        If a custom lifespan context manager is provided, it is used to manage application state and resource
        lifecycle. Otherwise, a default no-op handler is used.

        Args:
            scope: ASGI scope dictionary for the lifespan event.
            receive: Awaitable callable to receive ASGI messages.
            send: Awaitable callable to send ASGI messages.
        """
        if self.lifespan is None:
            # Default lifespan handling
            while True:
                message = await receive()
                if message["type"] == "lifespan.startup":
                    await send({"type": "lifespan.startup.complete"})
                elif message["type"] == "lifespan.shutdown":
                    await send({"type": "lifespan.shutdown.complete"})
                    return
        else:
            message = await receive()
            if message["type"] == "lifespan.startup":
                async with self.lifespan() as state:
                    if isinstance(state, dict):
                        app_state = scope.get("state", {})
                        app_state.update(state)
                        scope["state"] = app_state

                    await send({"type": "lifespan.startup.complete"})
                    while True:
                        message = await receive()
                        if message["type"] == "lifespan.shutdown":
                            await send({"type": "lifespan.shutdown.complete"})
                            break
