from datetime import timedelta
from fastapi import HTTPException, status
from httpx import AsyncClient
import random
from app.assets.profile_pictures import pictures
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.temp_user import TempUser
from app.utils.password_hasher import hash_password, verify_password
from app.handlers.jwt_handler import create_access_token, decode_access_token
from app.handlers.redis_handler import redis_client
from app.config.config import settings
from app.enums.role_enum import Role
from app.schemas.user_schema import UserProfileUpdateRequest
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


def get_user_profile(token: str, db: Session) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter_by(id=payload["user_id"]).first()
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


async def create_user_profile_picture():
    ... 
    
async def update_user_profile_picture():
    ...