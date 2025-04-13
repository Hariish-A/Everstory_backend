from pydantic import BaseModel, Field


class CreatePostRequest(BaseModel):
    is_private: bool = Field(default=False, description="Set to true to make the post private.")

class CreatePostResponse(BaseModel):
    post_id: int = Field(..., example=101)
    upload_url: str = Field(..., example="https://res.cloudinary.com/your_cloud/image/upload/v123/post_101")
    is_private: bool = Field(..., example=True)