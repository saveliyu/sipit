from pydantic import BaseModel

from app.api.schemas.types import UserRole


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class TokenRequest(BaseModel):
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str
    role: UserRole
    jti: str
