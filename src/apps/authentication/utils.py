from __future__ import annotations

import datetime
from typing import Union

import jwt
from passlib.context import CryptContext
from starlette.responses import JSONResponse
from tortoise.exceptions import DoesNotExist

from models import User

from apps.authentication.schemas import AuthRegisterUserSerializer, TokenUserSerializer, UserSerializer
from core import settings
from core.authentication.exceptions import InvalidTokenException

password_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(credentials: AuthRegisterUserSerializer) -> Union[JSONResponse, dict]:
    try:
        user = await User.get(username=credentials.username)
    except DoesNotExist:
        return JSONResponse(
            {
                "message": "User not found",
                "success": False,
            },
            status_code=404,
        )

    if not password_hasher.verify(credentials.password, user.password):
        return JSONResponse(
            {
                "message": "Incorrect password",
                "success": False,
            },
            status_code=400,
        )

    serialized_user = UserSerializer(**user.__dict__).__dict__
    serialized_user["token"] = create_jwt_token(payload=TokenUserSerializer(**user.__dict__).__dict__)
    return serialized_user


async def create_user(credentials: AuthRegisterUserSerializer) -> User | JSONResponse:
    if await User.filter(username=credentials.username).exists():
        return JSONResponse(
            {
                "message": "The user with this username already exists",
                "success": False,
            },
            status_code=400,
        )

    return await User.create(username=credentials.username, password=password_hasher.hash(secret=credentials.password))


def create_jwt_token(payload: dict) -> str:
    secret_key = settings.SECRET_KEY
    algorithm = settings.JWT["algorithm"]
    expiration_time = settings.JWT["expiration_time"]

    payload["exp"] = datetime.datetime.utcnow() + expiration_time

    encoded_jwt = jwt.encode(payload, secret_key, algorithm=algorithm)
    return encoded_jwt


def decode_jwt_token(token: str) -> dict:
    secret_key = settings.SECRET_KEY
    algorithm = settings.JWT["algorithm"]

    try:
        decoded_payload = jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm],
            verify_signature=True,
            options={"verify_exp": True},
        )
        return decoded_payload
    except jwt.ExpiredSignatureError:
        raise InvalidTokenException("Token has expired")
    except jwt.InvalidTokenError:
        raise InvalidTokenException("Invalid token")
