from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXP_MINUTES: int
    REDIS_HOST: str
    REDIS_PORT: int
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    JWT_ACCESS_TOKEN_EXPIRY_DAYS: int

    class Config:
        env_file = ".env"

settings = Settings()
