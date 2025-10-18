import os
from typing import Optional

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-change-me")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    SQL_ECHO: bool = os.getenv("SQL_ECHO", "false").lower() in ("true", "1", "yes")
    AUTO_LOAD: bool = os.getenv("AUTO_LOAD", "false").lower() in ("true", "1", "yes")

settings = Settings()
