from starlette.requests import Request

from core.permissions import BasePermission


class IsAdminPermission(BasePermission):
    def has_permission(self, request: Request) -> bool:
        return True
