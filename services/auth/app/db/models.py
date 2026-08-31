from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.api.schemas.types import UserRole


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class UserModel(Base):
    __tablename__ = "users"

    full_name: Mapped[str]

    phone_number: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()

    role: Mapped[UserRole] = mapped_column(default=UserRole.CUSTOMER)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
