from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    CLOUDINARY_UNSIGNED_PRESET : str

    JWT_SECRET: str
    JWT_ALGORITHM: str

    AUTH_VERIFY_URL: str
    FRIENDSHIP_SERVICE_URL: str
    AUTH_SERVICE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
