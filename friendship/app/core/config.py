import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    DB_URL = os.getenv("DATABASE_URL")

settings = Settings()
