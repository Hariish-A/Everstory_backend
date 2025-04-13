from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.post_schema import *
from app.services import post_service
from app.utils.token_utils import verify_token
from app.db.session import get_db

router = APIRouter()
security = HTTPBearer()

@router.post("/create", response_model=CreatePostResponse, summary="Generate Cloudinary upload URL")
async def create_post_route(
    payload: CreatePostRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
    user=Depends(verify_token)
):
    return post_service.create_post(db, user_id=user["id"], is_private=payload.is_private, type=payload.type)

@router.get("/me", response_model=list[PostResponse], summary="Get your posts")
async def get_my_posts_route(
    skip: int = 0,
    limit: int = 10,
    is_private: bool = None,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
    user=Depends(verify_token)
):
    return post_service.get_my_posts(db, user_id=user["id"], skip=skip, limit=limit, is_private=is_private)

@router.get("/posts/{post_id}", response_model=PostDetailResponse, summary="Get post by ID")
async def get_post_by_id_route(
    post_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
    user=Depends(verify_token)
):
    return post_service.get_post_by_id(db, user_id=user["id"], post_id=post_id)

@router.put("/posts/{post_id}", response_model=PostResponse, summary="Update post privacy")
async def update_post_route(
    post_id: int,
    payload: UpdatePostRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
    user=Depends(verify_token)
):
    return post_service.update_post(db, user_id=user["id"], post_id=post_id, is_private=payload.is_private)

@router.delete("/posts/{post_id}", response_model=MessageResponse, summary="Delete post")
async def delete_post_route(
    post_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
    user=Depends(verify_token)
):
    return post_service.delete_post(db, user_id=user["id"], post_id=post_id)


@router.get("/feed", response_model=list[PostDetailResponse], summary="Recommended Feed")
async def get_feed(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user=Depends(verify_token)  # Use gateway-auth verified token
):
    return await post_service.get_recommended_posts(
        db=db,
        token=user["token"],  # We'll make this available via patch below
        user_id=user["id"],
        skip=skip,
        limit=limit
    )
