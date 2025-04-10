from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.temp_user import TempUser
from app.utils.password_hasher import hash_password, verify_password
from auth_service.app.handlers.jwt_handler import create_access_token
from app.handlers.redis_handler import blacklist_token, is_token_blacklisted
from app.handlers.redis_handler import redis_client
from app.config.config import settings


def signup_user(db: Session, name: str, email: str, password: str):
    if db.query(TempUser).filter_by(email=email).first():
        raise HTTPException(status_code=400, detail="User already signed up. Please log in.")

    temp_user = TempUser(name=name, email=email, password=hash_password(password))
    db.add(temp_user)
    db.commit()
    db.refresh(temp_user)
    return {"message": "Signup successful. Please login to activate your account."}

def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter_by(email=email).first()
    if user and verify_password(password, user.password):
        return _issue_or_reuse_token(user.email)

    temp_user = db.query(TempUser).filter_by(email=email).first()
    if temp_user and verify_password(password, temp_user.password):
        user = User(name=temp_user.name, email=temp_user.email, password=temp_user.password)
        db.add(user)
        db.delete(temp_user)
        db.commit()
        db.refresh(user)
        return _issue_or_reuse_token(user.email)

    raise HTTPException(status_code=401, detail="Invalid credentials")


def _issue_or_reuse_token(email: str):
    key = f"user:{email}"
    existing_token = redis_client.get(key)

    if existing_token and not is_token_blacklisted(existing_token):
        return {"access_token": f"{existing_token}", "token_type": "Bearer"}

    # Revoke old if exists
    if existing_token:
        blacklist_token(existing_token)
        redis_client.delete(key)

    # Create new and store
    token = create_access_token({"sub": email})
    redis_client.setex(key, timedelta(days=settings.JWT_ACCESS_TOKEN_EXPIRY_DAYS), token)
    return {"access_token": f"{token}", "token_type": "Bearer"}


def logout_user(token: str):
    if is_token_blacklisted(token):
        return {"message": "You're already logged out. Login again to logout 😜"}
    
    blacklist_token(token)
    return {"message": "Logged out successfully"}
