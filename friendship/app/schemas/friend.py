from pydantic import BaseModel

class FriendRequest(BaseModel):
    user_id: int
    friend_id: int

class FriendOut(BaseModel):
    friend_id: int
    status: str
    class Config:
        orm_mode = True
