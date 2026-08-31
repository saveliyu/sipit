from sqlalchemy import select

from app.db.models import UserModel


class UserRepository:

    def __init__(self, session):
        self._session = session

    async def get_user_by_id(self, user_id: int) -> UserModel:
        stmt = select(UserModel).where(UserModel.id == user_id)
        return await self._session.scalars(stmt).one_or_none()

    async def create_user(self, user_model: UserModel) -> None:
        self._session.add(user_model)
        await self._session.flush()
