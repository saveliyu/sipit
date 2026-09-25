from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.api.schemas.types import TokenType
from app.api.schemas.user import UserData
from app.core.exceptions import CredentialsException
from app.core.security import decode_token
from app.db.database import db_helper
from app.db.redis import get_redis_client
from app.repositories.auth import AuthRedisRepository
from app.repositories.user import UserRepository
from app.services.auth import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_user(access_token: Annotated[str, Depends(oauth2_scheme)]) -> UserData:

    payload = decode_token(access_token, TokenType.ACCESS)
    if not payload:
        raise CredentialsException

    user_id = payload.get("sub")
    user_role = payload.get("role")

    if user_role is None or user_id is None:
        raise CredentialsException

    return UserData(id=int(user_id), role=user_role)


def get_user_repo(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> UserRepository:
    repo = UserRepository(session)
    return repo


def get_auth_repo(redis: Annotated[Redis, Depends(get_redis_client)]):
    repo = AuthRedisRepository(redis)
    return repo


def get_auth_service(
    repo: Annotated[UserRepository, Depends(get_user_repo)],
    redis: Annotated[AuthRedisRepository, Depends(get_auth_repo)],
) -> AuthService:
    service = AuthService(repo, redis)
    return service


AuthServiceDepends = Annotated[AuthService, Depends(get_auth_service)]
GetUserDepends = Annotated[UserData, Depends(get_user)]
