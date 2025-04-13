from pydantic import BaseModel, EmailStr
from typing import Optional, List
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
    role: Optional[Role] = None
    profile_pic: Optional[str] = None

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
    role: Optional[Role] = None
    profile_pic: Optional[str] = None
    
class FollowersListResponse(BaseModel):
    followers: List[UserProfileResponse]

class FollowingListResponse(BaseModel):
    following: List[UserProfileResponse]


class UsernameCheckResponse(BaseModel):
    exists: bool
    user_id: int | None = None
    message: str
    