from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base

class TempUser(Base):
    __tablename__ = "temp_users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
