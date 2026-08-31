from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.api.schemas.types import RuPhoneNumber, UserRole


class UserRegister(BaseModel):
    full_name: str
    phone_number: RuPhoneNumber

    password: str
    password_confirmation: str


class UserLogin(BaseModel):
    full_name: str
    password: str


class UserRead(BaseModel):
    id: int

    full_name: str
    phone_number: RuPhoneNumber
    role: UserRole

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
