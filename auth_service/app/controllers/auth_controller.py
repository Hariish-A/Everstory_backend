from fastapi import APIRouter, Depends, Header, HTTPException, status, Security
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services import auth_service
from app.schemas.auth_schema import SignUpRequest, LoginRequest, TokenResponse, MessageResponse, ErrorResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/signup",
    response_model=MessageResponse,
    responses={
        400: {"model": ErrorResponse, "description": "User already signed up"},
    },
    summary="Sign up a new user",
    description="Store user temporarily. On login, user will be moved to permanent table."
)

def signup(payload: SignUpRequest, db: Session = Depends(get_db)):
    return auth_service.signup_user(db, payload.name, payload.email, payload.password)

@router.post(
    "/login",
    response_model=TokenResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials or user not found"},
    },
    summary="Login a user",
    description="""
        Login using credentials. If the user exists in the temp table, they are migrated to the main users table.
        A new access token is generated and the previous one (if any) is revoked.
        **Token format:** `Bearer <access_token>`
    """
)

def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login_user(db, payload.email, payload.password)

@router.post(
    "/logout",
    response_model=MessageResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid token"},
    },
    summary="Logout a user",
    description="Blacklist the current access token in Redis. If already blacklisted, returns a friendly message 😉"
)

def logout(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    return auth_service.logout_user(token)
