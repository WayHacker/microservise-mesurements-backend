from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    DATABASE_URL: str
    ALEMBIC_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    REDIS_URL: str
    VERIFICATION_CODE_EXPIRE: int = 300
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin"
    ADMIN_SECRET_KEY: str = "change-me"

    class Config:
        env_file = ".env"


settings = Setting()
