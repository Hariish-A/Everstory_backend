from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.config.config import settings
from app.handlers.redis_handler import redis_client


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.JWT_ACCESS_TOKEN_EXPIRY_DAYS)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    if "sub" in to_encode:
        redis_client.setex(f"user:{to_encode['sub']}", timedelta(days=settings.JWT_ACCESS_TOKEN_EXPIRY_DAYS), token)

    return token


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
    except Exception as e:
        print(f"Error decoding token: {e}")
        return None
    