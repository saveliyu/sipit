from typing import Annotated

from fastapi import APIRouter, Body, status

from app.api.dependencies import AuthServiceDepends, GetUserDepends
from app.api.schemas.token import TokenResponse
from app.api.schemas.user import UserRegister, UserRead, UserLogin

router = APIRouter(prefix="/auth")


@router.get("/health-check")
async def health_check():
    return {"status": "ok"}


@router.get("/me", response_model=UserRead)
async def get_me(user: GetUserDepends, service: AuthServiceDepends):
    return service._repo.get_user_by_id(user.id)


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(data: Annotated[UserRegister, Body()], service: AuthServiceDepends):
    user = await service.register(data)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(data: Annotated[UserLogin, Body()], service: AuthServiceDepends):
    tokens = await service.login(data)
    return tokens


# @router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
# async def logout(data: Annotated[TokenRequest, Body()]):
#     return
#
#
# @router.post("/refresh", response_model=TokenResponse)
# async def refresh(data: Annotated[TokenRequest, Body()]):
#     return TokenResponse(access_token="aaa", refresh_token="aaa")
