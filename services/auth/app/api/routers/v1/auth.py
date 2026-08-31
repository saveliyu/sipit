from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Body, status

from app.api.schemas.token import TokenResponse, TokenRequest
from app.api.schemas.types import UserRole
from app.api.schemas.user import UserRegister, UserRead, UserLogin

router = APIRouter(prefix="/auth")


@router.get("/health-check")
async def health_check():
    return {"status": "ok"}


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(data: Annotated[UserRegister, Body()]):
    return UserRead(
        id=1,
        full_name=data.full_name,
        phone_number=data.phone_number,
        role=UserRole.CUSTOMER,
        created_at=datetime.now(),
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: Annotated[UserLogin, Body()]):
    return TokenResponse(access_token="aaa", refresh_token="aaa")


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(data: Annotated[TokenRequest, Body()]):
    return


@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: Annotated[TokenRequest, Body()]):
    return TokenResponse(access_token="aaa", refresh_token="aaa")
