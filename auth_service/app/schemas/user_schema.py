from pydantic import BaseModel, EmailStr
from typing import Optional
from app.enums.role_enum import Role

class UserProfileResponse(BaseModel):
    id: int
    name: str
    username: Optional[str]
    email: EmailStr
    bio: Optional[str]
    profile_pic: Optional[str]
    website: Optional[str]
    gender: Optional[str]
    role: Role

    class Config:
        from_attributes = True
        use_enum_values = True
        
class UserProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[str] = None