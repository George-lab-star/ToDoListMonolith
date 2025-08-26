from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USER: SecretStr
    DB_PASS: SecretStr
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    REDIS_USER: SecretStr
    REDIS_PASS: SecretStr
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_NAME: str

    TEST_REDIS_HOST: str

    JWT_ALGORITHM: str
    JWT_SECRET: str
    ACCESS_TOKEN_EXPIRE_SECONDS: int
    REFRESH_TOKEN_EXPIRE_SECONDS: int

    TEST_DB_USER: SecretStr
    TEST_DB_PASS: SecretStr
    TEST_DB_HOST: str
    TEST_DB_PORT: str
    TEST_DB_NAME: str

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.DB_USER.get_secret_value()}:{self.DB_PASS.get_secret_value()}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def test_database_url(self):
        return f"postgresql+asyncpg://{self.TEST_DB_USER.get_secret_value()}:{self.TEST_DB_PASS.get_secret_value()}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    @property
    def redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_NAME}"

    @property
    def test_redis_url(self):
        return f"redis://{self.TEST_REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_NAME}"


settings = Settings() # type: ignore