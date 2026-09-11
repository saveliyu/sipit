import base64
from pathlib import Path
from pydantic import BaseModel, PostgresDsn, computed_field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class JWTConfig(BaseModel):
    private_key_b64: str
    public_key_b64: str
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    @computed_field
    @property
    def private_key(self) -> str:
        return base64.b64decode(self.private_key_b64).decode("utf-8")

    @computed_field
    @property
    def public_key(self) -> str:
        return base64.b64decode(self.public_key_b64).decode("utf-8")


class RedisConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379
    path: str = "0"

    @computed_field
    @property
    def url(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis", host=self.host, port=self.port, path=self.path
        )


class DataBaseConfig(BaseModel):
    host: str
    port: int = 5432
    name: str
    user: str
    password: str

    pool_size: int = 5
    max_overflow: int = 10
    echo: bool = False
    echo_pool: bool = False

    @computed_field
    @property
    def url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.name,
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / ".env",
        env_nested_delimiter="__",
    )

    redis: RedisConfig = RedisConfig()
    db: DataBaseConfig
    jwt: JWTConfig


settings = Settings()
