# app/db/session.py

from sqlalchemy.orm import Session
from app.db.base import Base  # assuming you've defined your Base here
from app.config.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set up engine and sessionmaker
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency function to use in routes/services
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
