from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.friendship_schema import FriendRequestCreate, FriendRequestUpdate, FriendResponse
from app.services import friendship_service
from app.utils.gateway_auth import verify_token

router = APIRouter()

@router.post(
    "/send",
    response_model=FriendResponse,
    summary="Send a friend request",
    description="Allows an authenticated user to send a friend request to another user by providing their user ID. "
                "A user cannot send a friend request to themselves or send duplicate requests.",
    responses={
        200: {"description": "Friend request successfully sent"},
        400: {"description": "Invalid request (e.g. self-request or already friends)"},
        401: {"description": "Unauthorized - Invalid or missing token"},
        409: {"description": "Conflict - Friend request already exists"}
    }
)
async def send_request(payload: FriendRequestCreate, db: Session = Depends(get_db), user=Depends(verify_token)):
    return friendship_service.send_friend_request(db, user["id"], payload.friend_id)


@router.get(
    "/sent",
    response_model=list[FriendResponse],
    summary="View sent friend requests",
    description="Returns all friend requests that were initiated by the currently authenticated user.",
    responses={
        200: {"description": "List of sent friend requests"},
        401: {"description": "Unauthorized - Invalid or missing token"},
    }
)
async def sent_requests(db: Session = Depends(get_db), user=Depends(verify_token)):
    return friendship_service.get_sent_requests(db, user["id"])


@router.get(
    "/received",
    response_model=list[FriendResponse],
    summary="View received friend requests",
    description="Returns all pending friend requests that have been sent to the currently authenticated user.",
    responses={
        200: {"description": "List of received friend requests"},
        401: {"description": "Unauthorized - Invalid or missing token"},
    }
)
async def received_requests(db: Session = Depends(get_db), user=Depends(verify_token)):
    return friendship_service.get_received_requests(db, user["id"])


@router.put(
    "/accept",
    response_model=FriendResponse,
    summary="Accept a friend request",
    description="Allows a user to accept a pending friend request sent to them by another user.",
    responses={
        200: {"description": "Friend request accepted successfully"},
        401: {"description": "Unauthorized - Invalid or missing token"},
        404: {"description": "Friend request not found or not allowed"}
    }
)
async def accept(payload: FriendRequestUpdate, db: Session = Depends(get_db), user=Depends(verify_token)):
    updated = friendship_service.accept_request(db, user["id"], payload.request_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Request not found or not allowed")
    return updated


@router.get(
    "/friends/incoming",
    response_model=list[FriendResponse],
    summary="Friends who accepted your requests",
    description="Returns a list of users who accepted friend requests that were sent by the current user.",
    responses={
        200: {"description": "List of users who accepted your requests"},
        401: {"description": "Unauthorized - Invalid or missing token"},
    }
)
async def friends_who_accepted_me(db: Session = Depends(get_db), user=Depends(verify_token)):
    return friendship_service.get_friends_who_accepted_me(db, user["id"])


@router.get(
    "/friends/outgoing",
    response_model=list[FriendResponse],
    summary="Friends you accepted",
    description="Returns a list of users whose friend requests were accepted by the current user.",
    responses={
        200: {"description": "List of users whose requests you accepted"},
        401: {"description": "Unauthorized - Invalid or missing token"},
    }
)
async def friends_i_accepted(db: Session = Depends(get_db), user=Depends(verify_token)):
    return friendship_service.get_friends_i_accepted(db, user["id"])
