from typing import List
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.post_service import (
    create_post, get_my_posts, get_post_by_id, update_post, delete_post
)
from app.schemas.post_schema import (
    CreatePostRequest, CreatePostResponse, ErrorResponse,
    PostResponse, PostDetailResponse, UpdatePostRequest, MessageResponse
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/create",
    response_model=CreatePostResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized - Invalid token"},
        500: {"model": ErrorResponse, "description": "Unexpected server error"},
    },
    summary="Create a post and generate Cloudinary upload URL",
    description="Authenticates user via Bearer token and generates a Cloudinary URL for direct image upload."
)
def upload_post(
    payload: CreatePostRequest,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    try:
        return create_post(db, token, payload.is_private, payload.type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/me/",
    response_model=List[PostResponse],
    summary="Get all your posts (paginated)",
    description="Returns paginated list of the user's own posts. Supports optional `is_private` filter."
)
def get_my_posts_view(
    skip: int = 0,
    limit: int = 10,
    is_private: bool = None,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    return get_my_posts(db, credentials.credentials, skip, limit, is_private)

@router.get("/posts/{post_id}", response_model=PostDetailResponse, summary="Get post by ID")
def get_post(
    post_id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    return get_post_by_id(db, credentials.credentials, post_id)

@router.put("/posts/{post_id}", response_model=PostResponse, summary="Update post privacy")
def update_post_view(
    post_id: int,
    payload: UpdatePostRequest,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    return update_post(db, credentials.credentials, post_id, payload.is_private)

@router.delete("/posts/{post_id}", response_model=MessageResponse, summary="Delete post")
def delete_post_view(
    post_id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    return delete_post(db, credentials.credentials, post_id)


"""
Call /get-upload-url (send optional public_id)

Upload the image via POST to upload_url with file, upload_preset, and public_id as multipart/form-data

Use download_url to access the image!


"""