from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse

from apps.authentication.schemas import AuthRegisterUserSerializer
from apps.authentication.utils import authenticate_user, create_user

router = APIRouter(prefix="/api/auth")


@router.post("/")
async def auth_user(body: AuthRegisterUserSerializer, request: Request) -> JSONResponse:
    try:
        return await authenticate_user(body)
    except Exception:
        return JSONResponse(
            {
                "message": "Error occurred while authenticating",
                "success": False,
            },
            status_code=400,
        )


@router.post("/sign-up/")
async def sign_up(body: AuthRegisterUserSerializer, request: Request) -> dict:
    await create_user(body)
    return {
        "success": True,
    }
