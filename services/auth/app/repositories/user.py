from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import UserModel


class UserRepository:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user_by_id(self, user_id: int) -> UserModel:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self._session.scalars(stmt)
        return result.one_or_none()

    async def get_user_by_phone(self, phone_number: str) -> UserModel:
        stmt = select(UserModel).where(UserModel.phone_number == phone_number)
        result = await self._session.scalars(stmt)
        return result.one_or_none()

    async def create_user(self, user_model: UserModel) -> None:
        self._session.add(user_model)
        await self._session.flush()
