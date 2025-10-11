from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "dev-secret-change-me"
    ALGORITHM: str = "HS256"
    DATABASE_URL: str | None = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SQL_ECHO: bool = False
    AUTO_LOAD: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
