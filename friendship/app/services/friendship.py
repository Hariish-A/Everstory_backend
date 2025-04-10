from sqlalchemy.orm import Session
from app.models.friend import Friendship

def send_request(db: Session, user_id: int, friend_id: int):
    request = Friendship(user_id=user_id, friend_id=friend_id, status="pending")
    db.add(request)
    db.commit()
    db.refresh(request)
    return request

def accept_request(db: Session, user_id: int, friend_id: int):
    request = db.query(Friendship).filter(
        Friendship.user_id == friend_id,
        Friendship.friend_id == user_id,
        Friendship.status == "pending"
    ).first()
    if request:
        request.status = "accepted"
        db.commit()
        db.refresh(request)
    return request

def get_friends(db: Session, user_id: int):
    return db.query(Friendship).filter_by(user_id=user_id, status="accepted").all()
