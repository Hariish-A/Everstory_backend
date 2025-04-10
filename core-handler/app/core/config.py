import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    POSTGRES_AUTH_URL = os.getenv("POSTGRES_AUTH_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")

settings = Settings()
