from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    GATEWAY_URL: str
    AUTH_VERIFY_URL: str# Gateway URL like http://gateway:8000/auth/verify-token


    class Config:
        env_file = ".env"

settings = Settings()
