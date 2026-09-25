import uuid
import jwt

from datetime import datetime, timezone, timedelta
from pwdlib import PasswordHash

from app.api.schemas.token import TokenPayload
from app.api.schemas.types import TokenType
from app.core.config import settings
from app.core.exceptions import (
    ExpiredTokenException,
    InvalidTokenException,
    InvalidTokenPayloadException,
    InvalidTokenTypeException,
)

password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def _create_token(data: TokenPayload, token_expire: timedelta, token_type: str) -> str:
    to_encode = data.model_dump()
    expire = datetime.now(timezone.utc) + token_expire

    to_encode.update({"exp": expire})
    to_encode.update({"type": token_type})

    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=settings.jwt.private_key,
        algorithm=settings.jwt.algorithm,
    )
    return encoded_jwt


def create_access_token(data: TokenPayload) -> str:
    return _create_token(
        data,
        timedelta(minutes=settings.jwt.access_token_expire_minutes),
        TokenType.ACCESS,
    )


def create_refresh_token(data: TokenPayload) -> str:
    return _create_token(
        data, timedelta(days=settings.jwt.refresh_token_expire_days), TokenType.REFRESH
    )


def decode_token(token: str, expected_type: str) -> dict:
    try:
        payload = jwt.decode(
            token, settings.jwt.public_key, algorithms=[settings.jwt.algorithm]
        )
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenException
    except jwt.InvalidTokenError:
        raise InvalidTokenException

    if "sub" not in payload:
        raise InvalidTokenPayloadException

    if payload["type"] != expected_type:
        raise InvalidTokenTypeException

    return payload
