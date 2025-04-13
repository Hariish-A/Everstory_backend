from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.post import Post
from app.enums.post_type_enum import PostType
from app.utils.cloudinary_utils import generate_upload_url, delete_asset_from_cloudinary, get_download_url
import httpx
from app.config.config import settings
import logging

logger = logging.getLogger(__name__)


def create_post(db: Session, user_id: int, is_private: bool, type: PostType):
    new_post = Post(user_id=user_id, is_private=is_private, type=type)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    public_id = f"{'post' if type == PostType.POST else 'pfp'}_{new_post.id}"
    upload_creds = generate_upload_url()
    new_post.asset_url = get_download_url(public_id)
    db.commit()

    return {
        "post_id": new_post.id,
        "upload_url": upload_creds["upload_url"],
        "upload_preset": upload_creds["upload_preset"],
        "is_private": new_post.is_private,
        "public_id": public_id,
    }


def get_my_posts(db: Session, user_id: int, skip: int, limit: int, is_private: bool = None):
    query = db.query(Post).filter(Post.user_id == user_id, Post.type == PostType.POST)
    if is_private is not None:
        query = query.filter(Post.is_private == is_private)
    posts = query.offset(skip).limit(limit).all()
    return [{"id": p.id, "asset_url": p.asset_url, "user_id": p.user_id, "is_private": p.is_private, "type": p.type} for p in posts]


def get_post_by_id(db: Session, user_id: int, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != user_id and post.is_private:
        raise HTTPException(status_code=403, detail="Unauthorized to view this private post")
    return {
        "id": post.id,
        "asset_url": post.asset_url,
        "is_private": post.is_private,
        "user_id": post.user_id,
        "type": post.type
    }


def update_post(db: Session, user_id: int, post_id: int, is_private: bool):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != user_id:
        raise HTTPException(status_code=403, detail="You don't own this post")
    post.is_private = is_private
    db.commit()
    db.refresh(post)
    return {"id": post.id, "asset_url": post.asset_url, "is_private": post.is_private, "type": post.type}


def delete_post(db: Session, user_id: int, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != user_id:
        raise HTTPException(status_code=403, detail="You don't own this post")
    if post.asset_url:
        public_id = post.asset_url.split("/")[-1].split(".")[0]
        delete_asset_from_cloudinary(f"everstory/{public_id}")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully."}


async def get_recommended_posts(
    db: Session,
    token: str,
    user_id: int,
    skip: int = 0,
    limit: int = 10
) -> list[dict]:
    try:
        async with httpx.AsyncClient() as client:
            # Step 1: Auth
            user_res = await client.get(
                f"{settings.AUTH_VERIFY_URL}",
                headers={"Authorization": f"Bearer {token}"}
            )
            user_res.raise_for_status()
            user = user_res.json()
            user_id = user.get("id")
            if not user_id:
                raise HTTPException(status_code=401, detail="User ID missing in auth response")

            # Step 2: Get Friends
            friends_incoming = []
            friends_outgoing = []

            try:
                res = await client.get(
                    f"{settings.FRIENDSHIP_SERVICE_URL}/friendship/friends/incoming",
                    headers={"Authorization": f"Bearer {token}"}
                )
                if res.status_code == 200:
                    friends_incoming = res.json()
            except Exception:
                raise HTTPException(status_code=500, detail="Error fetching incoming friends")
            
            try:
                res = await client.get(
                    f"{settings.FRIENDSHIP_SERVICE_URL}/friendship/friends/outgoing",
                    headers={"Authorization": f"Bearer {token}"}
                )
                if res.status_code == 200:
                    friends_outgoing = res.json()
            except Exception:
                raise HTTPException(status_code=500, detail="Error fetching outgoing friends")

            if not isinstance(friends_incoming, list) or not isinstance(friends_outgoing, list):
                raise HTTPException(status_code=500, detail="Friendship response is not a list")
            

            friends = set()
            for f in friends_incoming + friends_outgoing:
                if f["user_id"] == user_id:
                    friends.add(f["friend_id"])
                else:
                    friends.add(f["user_id"])

            # Step 3: Get Following (excluding friends)
            following_ids = set()
            try:
                res = await client.get(
                    f"{settings.AUTH_SERVICE_URL}/auth/following/{user_id}",
                    headers={"Authorization": f"Bearer {token}"}
                )
                if res.status_code == 200:
                    data = res.json().get("following", [])
                    if isinstance(data, list):
                        following_ids = {f["id"] for f in data if "id" in f}
            except Exception:
                pass

            only_following = following_ids - friends

        # Step 4: Get Posts (ordered by newest first)
        private_from_friends = db.query(Post).filter(
            Post.user_id.in_(friends),
            Post.is_private.is_(True),
            Post.type == PostType.POST
        )

        public_from_friends = db.query(Post).filter(
            Post.user_id.in_(friends),
            Post.is_private.is_(False),
            Post.type == PostType.POST
        )

        public_from_following = db.query(Post).filter(
            Post.user_id.in_(only_following),
            Post.is_private.is_(False),
            Post.type == PostType.POST
        )

        combined = private_from_friends.union_all(public_from_friends).union_all(public_from_following)
        posts = combined.order_by(Post.created_at.desc()).offset(skip).limit(limit).all()

        return [
            {
                "id": p.id,
                "asset_url": p.asset_url,
                "is_private": p.is_private,
                "user_id": p.user_id,
                "type": p.type.value if p.type else None
            }
            for p in posts
        ]

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="External service failure")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feed generation failed: {str(e)}")
