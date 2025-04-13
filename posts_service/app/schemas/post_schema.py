from typing import Optional
from pydantic import BaseModel, Field

class CreatePostRequest(BaseModel):
    is_private: bool = Field(default=False, description="Set to true to make the post private.")
    type: str = Field(default="POST", description = "Set to PFP to upload Profile Picture")

class CreatePostResponse(BaseModel):
    post_id: int = Field(..., example=101)
    upload_url: str = Field(..., example="https://res.cloudinary.com/your_cloud/image/upload/v123/post_101")
    is_private: bool = Field(..., example=True)
    upload_preset: str= Field(..., example="my_upload_preset")
    public_id: str= Field(..., example="https://res.cloudinary.com/my_cloud/image/upload/pid.fmt")   

class ErrorResponse(BaseModel):
    detail: str = Field(..., example="Invalid token format")

class PostResponse(BaseModel):
    id: int
    user_id: int
    asset_url: Optional[str]
    is_private: bool
    type: Optional[str]

class PostDetailResponse(PostResponse):
    user_id: int

class UpdatePostRequest(BaseModel):
    is_private: bool = Field(..., example=True)

class MessageResponse(BaseModel):
    message: str = Field(..., example="Post deleted successfully.")
    