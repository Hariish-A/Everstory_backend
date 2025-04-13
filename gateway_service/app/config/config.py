from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AUTH_SERVICE_URL: str
    POSTS_SERVICE_URL: str
    GATEWAY_PORT: int = 8010
    FRIENDSHIP_SERVICE_URL: str
    class Config:
        env_file = ".env"

settings = Settings()
