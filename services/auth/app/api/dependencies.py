from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.schemas.types import TokenType
from app.api.schemas.user import UserData
from app.core.security import decode_token
from app.db.database import db_helper
from app.repositories.user import UserRepository
from app.services.auth import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_user(access_token: Annotated[str, Depends(oauth2_scheme)]) -> UserData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(access_token, TokenType.ACCESS)
    if not payload:
        raise credentials_exception

    user_id = payload.get("sub")
    user_role = payload.get("role")

    if user_role is None:
        raise credentials_exception

    if user_id is None:
        raise credentials_exception

    return UserData(id=int(user_id), role=user_role)


def get_user_repo(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> UserRepository:
    repo = UserRepository(session)
    return repo


def get_auth_service(
    repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> AuthService:
    service = AuthService(repo)
    return service


AuthServiceDepends = Annotated[AuthService, Depends(get_auth_service)]
GetUserDepends = Annotated[UserData, Depends(get_user)]
