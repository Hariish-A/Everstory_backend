from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.db.base import Base
from app.enums.post_type_enum import PostType
from sqlalchemy import Enum


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    asset_url = Column(String, nullable=True)
    type = Column()
    is_private = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    type = Column(Enum(PostType), default=PostType.POST)
    
