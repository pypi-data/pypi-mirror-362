import asyncio
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterator,
    Generic,
    Literal,
    NoReturn,
    Optional,
    TypeVar,
    Union,
    cast,
)

from asgiref.typing import (
    ASGIReceiveCallable,
    ASGIReceiveEvent,
    ASGISendCallable,
    ASGISendEvent,
    HTTPScope,
    Scope,
    WebSocketAcceptEvent,
    WebSocketScope,
)
from fast_query_parsers import parse_url_encoded_dict
from multidict import CIMultiDict

from asgify.errors import ClientDisconnected
from asgify.status import WS_1000_NORMAL_CLOSURE, WS_1006_ABNORMAL_CLOSURE

if TYPE_CHECKING:
    from .app import Asgify


StateT = TypeVar("StateT")


class BaseContext(Generic[StateT]):
    def __init__(
        self,
        app: "Asgify[StateT]",
        scope: Scope,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ) -> None:
        """
        Initialize the BaseContext with the given ASGI application, scope, receive, and send callables.

        Args:
            app (Asgify): The ASGI application instance.
            scope (Scope): The ASGI connection scope.
            receive (ASGIReceiveCallable): The callable to receive ASGI messages.
            send (ASGISendCallable): The callable to send ASGI messages.
        """
        self.app = app
        self._scope = scope
        self._receive = receive
        self._send = send
        self._headers: Optional[CIMultiDict[str]] = None
        self._params: dict[str, Union[str, list[str]]] = {}
        self.local: dict[str, Any] = {}

    @property
    def path(self) -> str:
        """
        Return the request path from the ASGI scope.

        Returns:
            str: The request path.
        """
        return cast(str, self._scope.get("path"))

    @property
    def method(
        self,
    ) -> Literal[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "PATCH",
        "HEAD",
        "OPTIONS",
        "TRACE",
        "CONNECT",
    ]:
        """
        Return the HTTP method from the ASGI scope.

        Returns:
            str: The HTTP method (e.g., 'GET', 'POST', 'PUT', 'DELETE', etc).
        """
        return cast(
            Literal[
                "GET",
                "POST",
                "PUT",
                "DELETE",
                "PATCH",
                "HEAD",
                "OPTIONS",
                "TRACE",
                "CONNECT",
            ],
            self._scope.get("method"),
        )

    @property
    def scheme(self) -> Optional[str]:
        """
        Return the URL scheme from the ASGI scope.

        Returns:
            str: The URL scheme (e.g., 'http', 'https').
        """
        return cast(Optional[str], self._scope.get("scheme"))

    @property
    def state(self) -> StateT:
        """
        Return the application state from the ASGI scope.

        Returns:
            dict: The application state dictionary.
        """
        return cast(StateT, self._scope.get("state", {}))

    @property
    def headers(self) -> CIMultiDict[str]:
        """
        Return the request headers as a CIMultiDict (case-insensitive MultiDict).

        Returns:
            CIMultiDict[str]: The request headers.
        """
        if self._headers is not None:
            return self._headers

        hdrs = CIMultiDict[str]()
        for name, value in cast(
            list[tuple[bytes, bytes]], self._scope.get("headers", [])
        ):
            hdrs.add(name.decode("latin-1"), value.decode("latin-1"))
        self._headers = hdrs
        return self._headers

    @property
    def params(self) -> dict[str, Union[str, list[str]]]:
        """
        Return the query parameters as a dictionary.

        Returns:
            dict[str, Union[str, list[str]]]: The query parameters.
        """
        if self._params:
            return self._params

        query_string = cast(bytes, self._scope.get("query_string", b""))
        self._params = parse_url_encoded_dict(query_string)
        return self._params

    async def receive(self) -> Union[ASGIReceiveEvent, NoReturn]:
        """
        Wrapper for the receive callable with connection close handling.
        Raises ClientDisconnected if the client disconnects.

        Returns:
            dict: The received ASGI message.
        Raises:
            ClientDisconnected: If the client disconnects.
        """
        message = await self._receive()
        if message["type"] in ("http.disconnect", "websocket.disconnect"):
            params: dict[Any, Any] = {}
            if message["type"] == "websocket.disconnect":
                params["code"] = message.get("code")
                params["reason"] = message.get("reason", "")
            raise ClientDisconnected(**params)
        return message

    async def send(self, message: ASGISendEvent) -> None:
        """
        Wrapper for the send callable with connection close handling.
        Raises ClientDisconnected if the connection is closed unexpectedly.

        Args:
            message (dict): The ASGI message to send.
        Raises:
            ClientDisconnected: If the connection is closed unexpectedly.
        """
        try:
            await self._send(message)
        except OSError as e:
            raise ClientDisconnected() from e


class HTTPContext(BaseContext[StateT]):
    def __init__(
        self,
        app: "Asgify[StateT]",
        scope: HTTPScope,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ) -> None:
        """
        Initialize the HTTPContext with the given ASGI application, HTTP scope, receive, and send callables.

        Args:
            app (Asgify): The ASGI application instance.
            scope (HTTPScope): The ASGI HTTP connection scope.
            receive (ASGIReceiveCallable): The callable to receive ASGI messages.
            send (ASGISendCallable): The callable to send ASGI messages.
        """
        super().__init__(app, scope, receive, send)

    async def read_body(self) -> AsyncIterator[bytes]:
        """
        Asynchronously read the HTTP request body in chunks.
        Yields each chunk as bytes until the body is fully read.

        Yields:
            bytes: A chunk of the request body.
        """
        yield b""
        while True:
            message = await self.receive()
            if message["type"] == "http.request":
                body = message.get("body", b"")
                yield body
                if not message.get("more_body", False):
                    break

    async def start(
        self,
        status: int,
        headers: Optional[dict[str, str]] = None,
        trailers: bool = False,
    ) -> None:
        """
        Start the HTTP response by sending the response start message with status, headers, and optional trailers.

        Args:
            status (int): The HTTP status code.
            headers (Optional[dict[str, str]]): The response headers.
            trailers (bool): Whether to expect HTTP trailers.
        """
        # Convert headers to iterable[tuple[bytes, bytes]]
        header_list = []
        for name, value in (headers or {}).items():
            header_list.append(
                (name.encode("latin-1"), value.encode("latin-1"))
            )

        await self.send(
            {
                "type": "http.response.start",
                "status": status,
                "headers": header_list,
                "trailers": trailers,
            }
        )

    async def write(self, body: bytes) -> None:
        """
        Send a chunk of the HTTP response body.

        Args:
            body (bytes): The response body chunk to send.
        """
        await self.send(
            {"type": "http.response.body", "body": body, "more_body": True}
        )

    async def end(self, body: bytes = b"") -> None:
        """
        End the HTTP response by sending the final body chunk with more_body set to False.

        Args:
            body (bytes): The final response body chunk to send. Defaults to empty bytes.
        """
        await self.send(
            {"type": "http.response.body", "body": body, "more_body": False}
        )


class WebSocketContext(BaseContext[StateT]):
    def __init__(
        self,
        app: "Asgify[StateT]",
        scope: WebSocketScope,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ) -> None:
        """
        Initialize a WebSocketContext instance.

        Parameters:
            app (Asgify): The ASGI application instance.
            scope (WebSocketScope): The ASGI WebSocket connection scope.
            receive (ASGIReceiveCallable): Callable to receive ASGI messages.
            send (ASGISendCallable): Callable to send ASGI messages.
        """
        super().__init__(app, scope, receive, send)
        self._connected = False
        self._lock = asyncio.Lock()

    async def accept(
        self,
        subprotocol: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> None:
        """
        Accept the WebSocket connection, optionally specifying a subprotocol and headers.

        Args:
            subprotocol (Optional[str]): The WebSocket subprotocol to use.
            headers (Optional[dict[str, str]]): Additional headers to include in the accept message.
        Raises:
            AssertionError: If the WebSocket is already connected.
            ValueError: If the received message is not a WebSocket connect event.
        """  # noqa: E501
        assert not await self.is_connected(), "WebSocket is already connected"
        async with self._lock:
            message = await self.receive()
            if message["type"] != "websocket.connect":
                raise ValueError(
                    f"Expected websocket.connect, got {message['type']}"
                )

            event = cast(WebSocketAcceptEvent, {"type": "websocket.accept"})
            if subprotocol:
                event["subprotocol"] = subprotocol

            # Convert headers to list[tuple[bytes, bytes]]
            header_list: list[tuple[bytes, bytes]] = []
            for name, value in (headers or {}).items():
                header_list.append(
                    (name.encode("latin-1"), value.encode("latin-1"))
                )

            event["headers"] = header_list
            await self.send(event)
            self._connected = True

    async def is_connected(self) -> bool:
        """
        Return whether the WebSocket connection is established.

        Returns:
            bool: True if connected, False otherwise.
        """
        async with self._lock:
            return self._connected

    async def receive_data(self) -> Union[str, bytes]:
        """
        Receive data from the WebSocket client after the connection is established.

        Returns the data as a string (text) or bytes (binary), depending on the type of message received.

        Raises:
            AssertionError: If the WebSocket is not connected.
            ValueError: If the received message type is not 'websocket.receive' or no data is found.
        Returns:
            Union[str, bytes]: The data received from the WebSocket client.
        """
        assert await self.is_connected(), "WebSocket is not connected"
        message = await self.receive()
        if message["type"] != "websocket.receive":
            raise ValueError(
                f"Expected websocket.receive, got {message['type']}"
            )

        data = message.get("bytes")
        if not data:
            data = message.get("text")

        assert data, f"Expected text or binary data, got {data}"
        return data

    async def receive_text(self) -> str:
        """
        Receive a text message from the WebSocket client.

        Returns:
            str: The received text data.

        Raises:
            ValueError: If the received data is not of type str.
        """
        data = await self.receive_data()
        if not isinstance(data, str):
            raise ValueError(f"Expected text data, got {data}")
        return data

    async def receive_bytes(self) -> bytes:
        """
        Receive a binary (bytes) message from the WebSocket client after the connection is established.

        Returns:
            bytes: The received binary data.

        Raises:
            ValueError: If the received data is not of type bytes.
        """
        data = await self.receive_data()
        if not isinstance(data, bytes):
            raise ValueError(f"Expected binary data, got {data}")
        return data

    async def send_text(self, text: str) -> None:
        """
        Send a text message to the WebSocket client.

        Args:
            text (str): The text message to send.
        Raises:
            AssertionError: If the WebSocket is not connected.
        """
        assert await self.is_connected(), "WebSocket is not connected"
        await self.send({"type": "websocket.send", "text": text, "bytes": None})

    async def send_bytes(self, data: bytes) -> None:
        """
        Send a binary message to the WebSocket client.

        Args:
            data (bytes): The binary data to send.
        Raises:
            AssertionError: If the WebSocket is not connected.
        """
        assert await self.is_connected(), "WebSocket is not connected"
        await self.send({"type": "websocket.send", "bytes": data, "text": None})

    async def close(
        self, code: int = WS_1000_NORMAL_CLOSURE, reason: Optional[str] = None
    ) -> NoReturn:
        """
        Close the WebSocket connection with the given code and optional reason.
        If not connected, accept the connection first.

        Args:
            code (int): The WebSocket close code.
            reason (Optional[str]): The reason for closing the connection.
        """
        if not await self.is_connected():
            code = WS_1006_ABNORMAL_CLOSURE
        async with self._lock:
            await self.send(
                {"type": "websocket.close", "code": code, "reason": reason}
            )
            self._connected = False
        raise ClientDisconnected(code=code, reason=reason)
