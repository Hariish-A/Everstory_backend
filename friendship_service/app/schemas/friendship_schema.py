from pydantic import BaseModel
from app.enums.status_enum import FriendRequestStatus

class FriendRequestCreate(BaseModel):
    friend_id: int

class FriendRequestUpdate(BaseModel):
    request_id: int
    new_status: FriendRequestStatus

class FriendResponse(BaseModel):
    id: int
    user_id: int
    friend_id: int
    status: FriendRequestStatus

    class Config:
        from_attributes = True
