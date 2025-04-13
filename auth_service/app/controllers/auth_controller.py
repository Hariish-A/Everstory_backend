from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services import auth_service
from app.schemas.auth_schema import (
    SignUpRequest, LoginRequest, TokenResponse,
    MessageResponse, ErrorResponse
)
from app.schemas.user_schema import UserProfileResponse, UserProfileUpdateRequest
from app.enums.role_enum import Role
from app.guards.role_guard import require_role
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.profile_picture_schema import CreatePostRequest, CreatePostResponse


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
    responses={400: {"model": ErrorResponse}},
    summary="Sign up a new user",
    description="Stores user in temporary table. On login, user is moved to permanent table."
)
def signup(payload: SignUpRequest, db: Session = Depends(get_db)):
    return auth_service.signup_user(db, payload.name, payload.email, payload.password)


@router.post(
    "/login",
    response_model=TokenResponse,
    responses={401: {"model": ErrorResponse}},
    summary="Login a user",
    description="Login user and return access token. If in temp table, move to permanent table. Token reused if not expired."
)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login_user(db, payload.email, payload.password)


@router.post(
    "/logout",
    response_model=MessageResponse,
    responses={401: {"model": ErrorResponse}},
    summary="Logout user",
    description="Deletes access token from Redis. Friendly message if already logged out."
)
def logout(credentials: HTTPAuthorizationCredentials = Security(security)):
    return auth_service.logout_user(credentials.credentials)


@router.get(
    "/verify-token",
    response_model=MessageResponse,
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse}
    },
    summary="Verify token validity",
    description="Validates token and checks if user still exists"
)
def verify_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    return auth_service.verify_token(credentials.credentials, db)


@router.get(
    "/me",
    response_model=UserProfileResponse,
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse}
    },
    summary="Get current user profile",
    description="Returns the user object associated with the access token"
)
def get_profile(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    return auth_service.get_user_profile(credentials.credentials, db)

@router.post(
    "/me",
    response_model=UserProfileResponse,
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse}
    },
    summary="Create user profile",
    description="Creates the user profile associated with the access token"
)
def create_profile(payload: UserProfileUpdateRequest, credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    return auth_service.create_user_profile(credentials.credentials, db, payload)

@router.put(
    "/me",
    response_model=UserProfileResponse,
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse}
    },
    summary="Update current user profile",
    description="Updates the user object associated with the access token"
)
def update_profile(payload: UserProfileUpdateRequest, credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    return auth_service.update_user_profile(credentials.credentials, db, payload)


@router.get(
    "/me/pfp",
    response_model=CreatePostResponse,
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse}
    },
    summary="Get user profile picture upload url",
    description="Creates the profile picture url for the user by invoking gateway's /profile/create"
)
def create_pfp(payload: CreatePostRequest, credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    return auth_service.create_user_profile_picture(credentials.credentials, db, payload)

@router.put(
    "/me/pfp",
    response_model=CreatePostResponse,
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse}
    },
    summary="Update current user profile",
    description="Updates the user object associated with the access token"
)
def update_pfp(payload: CreatePostRequest, credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    return auth_service.update_user_profile_picture(credentials.credentials, db, payload)





# RBAC Protected Routes

@router.get("/admin-only", dependencies=[Depends(require_role(Role.ADMIN))], summary="Admin access only")
def admin_route():
    return {"message": "You are an admin!"}

@router.get("/user-only", dependencies=[Depends(require_role(Role.USER))], summary="User access only")
def user_route():
    return {"message": "You are a user!"}

@router.get("/admin-or-user", dependencies=[Depends(require_role(Role.ADMIN, Role.USER))], summary="Admin or user access")
def admin_or_user_route():
    return {"message": "You are either an admin or a user!"}

@router.get("/moderator-data", summary="Moderator or admin access")
def mod_view(current_user=Depends(require_role(Role.MODERATOR, Role.ADMIN))):
    return {"msg": f"Hello {current_user.name}, you have moderator/admin access."}
