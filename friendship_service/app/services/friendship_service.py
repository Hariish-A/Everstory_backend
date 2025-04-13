from sqlalchemy.orm import Session
from app.models.friendship import Friendship
from app.enums.status_enum import FriendRequestStatus

def send_friend_request(db: Session, user_id: int, friend_id: int):
    if user_id == friend_id:
        raise ValueError("You cannot send a friend request to yourself")

    friendship = Friendship(user_id=user_id, friend_id=friend_id)
    db.add(friendship)
    db.commit()
    db.refresh(friendship)
    return friendship

def get_sent_requests(db: Session, user_id: int):
    return db.query(Friendship).filter_by(user_id=user_id).all()

def get_received_requests(db: Session, user_id: int):
    return db.query(Friendship).filter_by(friend_id=user_id).all()

def accept_request(db: Session, user_id: int, request_id: int):
    req = db.query(Friendship).filter_by(id=request_id, friend_id=user_id).first()
    if not req:
        return None
    req.status = FriendRequestStatus.ACCEPTED
    db.commit()
    db.refresh(req)
    return req


# Friends who accepted me (I received request and accepted it)
def get_friends_who_accepted_me(db: Session, user_id: int):
    return db.query(Friendship).filter(
        (Friendship.friend_id == user_id) &
        (Friendship.status == FriendRequestStatus.ACCEPTED)
    ).all()

# Friends I accepted (I sent request and they accepted)
def get_friends_i_accepted(db: Session, user_id: int):
    return db.query(Friendship).filter(
        (Friendship.user_id == user_id) &
        (Friendship.status == FriendRequestStatus.ACCEPTED)
    ).all()
