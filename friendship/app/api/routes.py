from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.friend import FriendRequest
from app.services.friendship import send_request, accept_request, get_friends
from app.models.friend import Base
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

@router.post("/request")
def request_friendship(payload: FriendRequest, db: Session = Depends(get_db)):
    return send_request(db, payload.user_id, payload.friend_id)

@router.post("/accept")
def accept_friendship(payload: FriendRequest, db: Session = Depends(get_db)):
    return accept_request(db, payload.user_id, payload.friend_id)

@router.get("/friends/{user_id}")
def list_friends(user_id: int, db: Session = Depends(get_db)):
    return get_friends(db, user_id)
