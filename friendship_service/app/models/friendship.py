from sqlalchemy import Column, Integer, Enum, UniqueConstraint, ForeignKey
from app.db.base import Base
from app.enums.status_enum import FriendRequestStatus

class Friendship(Base):
    __tablename__ = "friendships"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    friend_id = Column(Integer, nullable=False)
    status = Column(Enum(FriendRequestStatus), default=FriendRequestStatus.PENDING)

    __table_args__ = (
        UniqueConstraint('user_id', 'friend_id', name='unique_friendship'),
    )
