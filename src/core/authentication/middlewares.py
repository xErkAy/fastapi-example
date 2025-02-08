from __future__ import annotations

from typing import Any, Coroutine, Union

from tortoise.exceptions import DoesNotExist

from apps.authentication.schemas import AuthenticatedUser
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from starlette.requests import HTTPConnection
from starlette.responses import JSONResponse, Response
from starlette.types import Receive, Scope, Send

from apps.authentication.utils import decode_jwt_token
from core.authentication.exceptions import InvalidTokenException
from core.middlewares import BaseMiddleware
from models import User


class AuthenticationMiddleware(BaseMiddleware):
    def on_error(self, conn: HTTPConnection, exc: Exception) -> Response:
        return JSONResponse(
            {
                "message": str(exc),
                "success": False,
            },
            status_code=401,
        )

    async def run(self, conn: HTTPConnection, scope: Scope, receive: Receive, send: Send) -> None:
        if "/api/auth" in conn.url.path:
            return

        auth_result = await self.authenticate(conn)
        if auth_result is None:
            auth_result = AuthCredentials(), UnauthenticatedUser()
        scope["auth"], scope["user"] = auth_result

    async def authenticate(self, request: HTTPConnection) -> [bool, dict]:
        if "Authorization" not in request.headers:
            raise Exception("Token not found")

        auth = request.headers["Authorization"]
        try:
            scheme, token = auth.split()
            if scheme.lower() != "bearer":
                raise Exception("Token must be the Bearer token")
            decoded = decode_jwt_token(token)
            # user = AuthenticatedUser(**decoded)
            user = await self._get_user(decoded)
        except InvalidTokenException as exc:
            raise Exception(str(exc))
        except Exception:
            raise Exception("Something went wrong while decoding the token")

        return decoded, user

    async def _get_user(self, decoded_token: dict) -> Union[User, None]:
        if not decoded_token.get("id"):
            return None
        return await User.get_or_none(id=decoded_token["id"])
