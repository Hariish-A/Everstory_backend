import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    DB_URL = os.getenv("DATABASE_URL")
    S3_BUCKET = os.getenv("S3_BUCKET")
    S3_KEY = os.getenv("S3_KEY")
    S3_SECRET = os.getenv("S3_SECRET")
    REGION = os.getenv("REGION")

settings = Settings()
