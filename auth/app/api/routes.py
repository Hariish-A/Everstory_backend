from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, Token
from app.services.auth import create_user, authenticate_user
from app.models.user import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

router = APIRouter()

engine = create_engine(settings.DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user.username, user.password)
    token = authenticate_user(db, user.username, user.password)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    token = authenticate_user(db, user.username, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}
