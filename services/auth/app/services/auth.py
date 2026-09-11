from fastapi import HTTPException, status

from app.api.schemas.user import UserRegister
from app.db.models import UserModel
from app.repositories.user import UserRepository
from app.core.security import get_password_hash


class AuthService:

    def __init__(self, repo: UserRepository):
        self._repo = repo

    async def register(self, data: UserRegister) -> UserModel:
        user = self._repo.get_user_by_phone(str(data.phone_number))
        if user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
            )

        if data.password != data.password_confirmation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        hashed_password = get_password_hash(data.password)

        user_model = UserModel(
            full_name=data.full_name,
            phone_number=data.phone_number,
            hashed_password=hashed_password,
        )
        await self._repo.create_user(user_model)

        return user_model
