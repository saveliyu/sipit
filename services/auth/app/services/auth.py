from fastapi import HTTPException, status

from app.api.schemas.token import TokenResponse, TokenPayload
from app.api.schemas.user import UserRegister, UserLogin
from app.db.models import UserModel
from app.repositories.user import UserRepository
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
)


class AuthService:

    def __init__(self, repo: UserRepository):
        self._repo = repo

    async def register(self, data: UserRegister) -> UserModel:
        if data.password != data.password_confirmation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        #
        # user = self._repo.get_user_by_phone(str(data.phone_number))
        # if user is not None:
        #     raise HTTPException(
        #         status_code=status.HTTP_409_CONFLICT,
        #     )

        hashed_password = get_password_hash(data.password)

        user_model = UserModel(
            full_name=data.full_name,
            phone_number=str(data.phone_number),
            hashed_password=hashed_password,
        )
        await self._repo.create_user(user_model)

        return user_model

    async def login(self, data: UserLogin) -> TokenResponse:
        user = await self._repo.get_user_by_phone(str(data.phone_number))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
            )

        payload = TokenPayload(sub=str(user.id), role=user.role)

        return TokenResponse(
            access_token=create_access_token(payload),
            refresh_token=create_refresh_token(payload),
        )
