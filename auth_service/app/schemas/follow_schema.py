from pydantic import BaseModel
from typing import  List
class FollowerResponse(BaseModel):
    id: int
    follower_id: int
    followed_id: int

class FollowingResponse(BaseModel):
    id: int
    follower_id: int
    followed_id: int



class FollowCountsResponse(BaseModel):
    followers_count: int
    following_count: int