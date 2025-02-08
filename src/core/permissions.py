from functools import wraps
from typing import Any, Callable, Type

from starlette.requests import Request
from starlette.responses import JSONResponse


class BasePermission:
    def has_permission(self, request: Request) -> None:
        raise NotImplementedError()


def permissions(permissions_: list[Type[BasePermission]]) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: dict[str, Any]) -> JSONResponse:
            request = kwargs["request"]
            if getattr(request, "user", None) is not None:
                for permission in permissions_:
                    if not permission().has_permission(request.user):
                        return JSONResponse({"message": "Permission denied", "success": False}, status_code=403)
            return await func(*args, **kwargs)

        return wrapper

    return decorator
