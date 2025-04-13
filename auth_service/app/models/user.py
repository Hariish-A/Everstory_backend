from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from app.db.base import Base
from app.enums.role_enum import Role
from sqlalchemy import Enum

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
