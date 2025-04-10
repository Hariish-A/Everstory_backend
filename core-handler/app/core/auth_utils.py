from jose import jwt, JWTError
from app.core.config import settings
from sqlalchemy.orm import Session
from app.core.models import User  # model we'll define inline

def validate_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        user = db.query(User).filter(User.username == username).first()
        return {"username": user.username, "user_id": user.id} if user else None
    except JWTError:
        return None
