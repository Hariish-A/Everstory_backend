from pydantic import BaseModel

class ImageUpload(BaseModel):
    user_id: int
    visibility: str

class ImageOut(BaseModel):
    id: int
    url: str
    visibility: str
    class Config:
        orm_mode = True
