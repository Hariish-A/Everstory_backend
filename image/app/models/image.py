from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    url = Column(String)
    visibility = Column(String)  # 'public' or 'private'
