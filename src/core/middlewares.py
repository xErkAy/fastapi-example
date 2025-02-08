from __future__ import annotations

from typing import Union, Any

from starlette.requests import HTTPConnection
from starlette.responses import PlainTextResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send


class BaseMiddleware:
    def __init__(
        self,
        app: ASGIApp,
    ) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> Union[Response, None]:
        if scope["type"] not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return None

        conn = HTTPConnection(scope)
        try:
            await self.run(conn, scope, receive, send)
        except Exception as exc:
            response = self.on_error(conn, exc)
            if scope["type"] == "websocket":
                await send({"type": "websocket.close", "code": 1000})
            else:
                await response(scope, receive, send)
            return None

        await self.app(scope, receive, send)
        return None

    async def run(self, *args: Any) -> None:
        raise NotImplementedError()

    def on_error(self, conn: HTTPConnection, exc: Exception) -> Response:
        return PlainTextResponse(str(exc), status_code=400)
