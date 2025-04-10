from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.POSTGRES_AUTH_URL)
SessionLocal = sessionmaker(bind=engine)

def get_auth_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
