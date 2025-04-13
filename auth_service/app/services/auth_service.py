from datetime import timedelta
from app.schemas.follow_schema import FollowCountsResponse
from fastapi import HTTPException, status
from httpx import AsyncClient
import random
from app.assets.profile_pictures import pictures
from sqlalchemy.orm import Session
from app.models.user import User, Follower
from app.models.temp_user import TempUser
from app.utils.password_hasher import hash_password, verify_password
from app.handlers.jwt_handler import create_access_token, decode_access_token
from app.handlers.redis_handler import redis_client
from app.config.config import settings
from app.enums.role_enum import Role
from app.schemas.user_schema import UserProfileUpdateRequest, FollowersListResponse, FollowingListResponse, UserProfileResponse
from app.schemas.profile_picture_schema import CreatePostRequest, CreatePostResponse


def signup_user(db: Session, name: str, email: str, password: str):
    if db.query(TempUser).filter_by(email=email).first():
        raise HTTPException(status_code=400, detail="User already signed up. Please log in.")

    temp_user = TempUser(name=name, email=email, password=hash_password(password))
    db.add(temp_user)
    db.commit()
    return {"message": "Signup successful. Please login to activate your account."}


def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter_by(email=email).first()
    if user and verify_password(password, user.password):
        return _issue_or_reuse_token(user, force_new=True)

    temp_user = db.query(TempUser).filter_by(email=email).first()
    if temp_user and verify_password(password, temp_user.password):
        user = User(
            name=temp_user.name,
            email=temp_user.email,
            password=temp_user.password,
            role=Role.USER
        )
        db.add(user)
        db.delete(temp_user)
        db.commit()
        db.refresh(user)
        return _issue_or_reuse_token(user, force_new=True)

    raise HTTPException(status_code=401, detail="Invalid credentials")


def _issue_or_reuse_token(user: User, force_new: bool = False):
    redis_key = f"user:{user.email}"

    if not force_new:
        existing_token = redis_client.get(redis_key)
        if existing_token:
            return {"access_token": existing_token, "token_type": "Bearer"}

    # Create new
    token = create_access_token({
        "sub": user.email,
        "user_id": user.id,
        "role": user.role
    })
    redis_client.setex(redis_key, timedelta(days=settings.JWT_ACCESS_TOKEN_EXPIRY_DAYS), token)
    return {"access_token": token, "token_type": "Bearer"}



def logout_user(token: str):
    
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    email = payload["sub"]
    redis_key = f"user:{email}"
    existing_token = redis_client.get(redis_key)

    if not existing_token or existing_token != token:
        raise HTTPException(status_code=401, detail="You're already logged out. Login again to logout 😜")

    redis_client.delete(redis_key)
    return {"message": "Logged out successfully"}



def verify_token(token: str, db: Session):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter_by(id=payload.get("user_id")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Token is valid", "user_id": user.id, "email": user.email, "role": user.role.name}


def get_my_profile(token: str, db: Session) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter_by(id=payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

def get_user_profile(user_id, token: str, db: Session) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

def create_user_profile(token: str, db: Session, payload: UserProfileUpdateRequest):
    creds = decode_access_token(token)
    if not creds:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter_by(id=creds["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
   
    # Update user profile fields
    user.name = payload.name 
    user.username = payload.username 
    user.bio = payload.bio 
    user.location = payload.location
    user.website = payload.website 
    user.birth_date = payload.birth_date
    user.profile_pic = random.choice(pictures)
    user.gender = payload.gender

    db.commit()
    db.refresh(user)

    return user

def update_user_profile(token: str, db: Session, payload: UserProfileUpdateRequest):
    creds = decode_access_token(token)
    if not creds:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter_by(id=creds["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
   
    # Update user profile fields
    user.name = payload.name 
    user.username = payload.username 
    user.bio = payload.bio 
    user.location = payload.location
    user.website = payload.website 
    user.birth_date = payload.birth_date
    user.gender = payload.gender
    # user.profile_pic = random.choice(pictures)
    

    db.commit()
    db.refresh(user)

    return user

def follow_user(db: Session, token: str, followed_id: int):
    user_id = decode_access_token(token).get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    if user_id == followed_id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")

    followed_user = db.query(User).filter(User.id == followed_id).first()
    if not followed_user:
        raise HTTPException(status_code=404, detail="User to follow not found")

    existing_follow = db.query(Follower).filter(Follower.follower_id == user_id, Follower.followed_id == followed_id).first()
    if existing_follow:
        raise HTTPException(status_code=400, detail="You are already following this user")

    follow = Follower(follower_id=user_id, followed_id=followed_id)
    db.add(follow)
    db.commit()
    return {"message": f"You are now following {followed_user.username}"}

def unfollow_user(db: Session, token: str, followed_id: int):
    user_id = decode_access_token(token).get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    follow = db.query(Follower).filter(Follower.follower_id == user_id, Follower.followed_id == followed_id).first()
    if not follow:
        raise HTTPException(status_code=404, detail="You are not following this user")

    db.delete(follow)
    db.commit()
    return {"message": f"You have unfollowed user"}

def get_followers(db: Session, token: str, user_id: int):
     user = db.query(User).filter(User.id == user_id).first()
     if not user:
          raise HTTPException(status_code=404, detail="User not found")
     
     followers = user.followers
     follower_list = []

     for follower in followers:
          user = db.query(User).filter(User.id == follower.follower_id).first()
          follower_list.append(UserProfileResponse(id=user.id, name=user.name or "", username=user.username or "", email=user.email or "", bio=user.bio or "", profile_pic=user.profile_pic or "", website=user.website or "", gender=user.gender or "", location=user.location or ""))
     
     return FollowersListResponse(followers=follower_list)

def get_following(db: Session, token: str, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    following = user.following
    following_list = []

    for followed in following:
        user = db.query(User).filter(User.id == followed.followed_id).first()
        following_list.append(UserProfileResponse(id=user.id, name=user.name, username=user.username, email=user.email, bio=user.bio, profile_pic=user.profile_pic, website=user.website, gender=user.gender, location=user.location))
    
    return FollowingListResponse(following=following_list)


def get_follow_counts(db: Session, token: str, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    followers_count = db.query(Follower).filter(Follower.followed_id == user_id).count()
    following_count = db.query(Follower).filter(Follower.follower_id == user_id).count()

    return FollowCountsResponse(followers_count=followers_count, following_count=following_count)

async def create_user_profile_picture():
    ... 
    
async def update_user_profile_picture():
    ...


def check_username_exists(db: Session, username: str):
    user = db.query(User).filter_by(username=username).first()
    if user:
        return {
            "exists": True,
            "user_id": user.id,
            "message": "Username exists"
        }
    raise HTTPException(
        status_code=404,
        detail={
            "exists": False,
            "user_id": None,
            "message": "Username does not exist"
        }
    )
