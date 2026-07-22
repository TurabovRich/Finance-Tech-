from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    APP_ENV: str = "development"
    APP_NAME: str = "Clarity API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    DATABASE_URL: str = "postgresql+asyncpg://clarity:clarity_dev@localhost:5432/clarity"
    # Separate database so the test suite never touches local dev data. Defaults to
    # the same server as DATABASE_URL with `_test` appended if not set explicitly.
    TEST_DATABASE_URL: str | None = None

    SECRET_KEY: str = "change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"


settings = Settings()
