from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.config.config import settings
from app.handlers.redis_handler import redis_client


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXP_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    if "sub" in data:
        redis_client.set(f"user:{data['sub']}", token)

    return token


def decode_access_token(token: str):
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None
