from datetime import datetime

from pydantic import BaseModel


class AuthRegisterUserSerializer(BaseModel):
    username: str
    password: str


class TokenUserSerializer(BaseModel):
    id: int
    username: str
    is_admin: bool


class AuthenticatedUser(TokenUserSerializer):
    exp: int


class UserSerializer(BaseModel):
    id: int
    username: str
    is_admin: bool
    created_at: datetime
