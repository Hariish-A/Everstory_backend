# app/guards/role_guard.py
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.handlers.jwt_handler import decode_access_token
from app.enums.role_enum import Role
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User

security = HTTPBearer()

def require_role(*allowed_roles: Role):
    def _require_role(
        credentials: HTTPAuthorizationCredentials = Security(security),
        db: Session = Depends(lambda: SessionLocal())
    ) -> User:
        token = credentials.credentials
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter_by(id=payload.get("user_id")).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access denied")

        return user
    return _require_role
