import uuid
from datetime import timezone, datetime

from app.api.schemas.token import TokenResponse, TokenPayload, TokenRequest
from app.api.schemas.types import TokenType
from app.api.schemas.user import UserRegister, UserLogin, UserData
from app.core.exceptions import (
    PasswordsDoesntMatchException,
    PhoneNumberAlreadyExistsException,
    UserNotFoundOrPasswordIncorrectException,
    UserNotFoundException,
)
from app.db.models import UserModel
from app.repositories.auth import AuthRedisRepository
from app.repositories.user import UserRepository
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)


class AuthService:

    def __init__(self, repo: UserRepository, redis: AuthRedisRepository):
        self._repo = repo
        self._redis = redis

    async def register(self, data: UserRegister) -> UserModel:
        if data.password != data.password_confirmation:
            raise PasswordsDoesntMatchException

        user = await self._repo.get_user_by_phone(str(data.phone_number))
        if user is not None:
            raise PhoneNumberAlreadyExistsException

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
            raise UserNotFoundException

        if not verify_password(data.password, user.hashed_password):
            raise UserNotFoundOrPasswordIncorrectException

        payload = TokenPayload(sub=str(user.id), role=user.role, jti=str(uuid.uuid4()))

        return TokenResponse(
            access_token=create_access_token(payload),
            refresh_token=create_refresh_token(payload),
        )

    async def logout(self, data: TokenRequest, user_data: UserData):
        payload = decode_token(data.refresh_token, TokenType.REFRESH)
        key = f"blacklist:{payload.get("jti")}"
        ex = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc) - datetime.now(
            timezone.utc
        )
        await self._redis.set(key, 1, ex)
