from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base
from app.enums.role_enum import Role
from sqlalchemy import Enum
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    #profile
    bio = Column(String, nullable=True)
    profile_pic = Column(String, nullable=True)
    website = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    
    
    location = Column(String, nullable=True)
    birth_date = Column(String, nullable=True)

    role = Column(Enum(Role), default=Role.USER)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
        # Relationships
    following = relationship("Follower", foreign_keys="[Follower.follower_id]", back_populates="follower")
    followers = relationship("Follower", foreign_keys="[Follower.followed_id]", back_populates="followed")

    
class Follower(Base):
    __tablename__ = "followers"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"))
    followed_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followed = relationship("User", foreign_keys=[followed_id], back_populates="followers")
