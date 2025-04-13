from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.post import Post
from app.enums.post_type_enum import PostType
from app.utils.token_utils import get_user_id_from_token
from app.utils.cloudinary_utils import generate_upload_url, delete_asset_from_cloudinary, get_download_url


def create_post(db: Session, token: str, is_private: bool, type: PostType):
    try:
        user_id = get_user_id_from_token(token)
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        new_post = Post(user_id=user_id, is_private=is_private or False, type = PostType.POST)
        if type == PostType.PFP:    
            new_post = Post(user_id=user_id, is_private = False, type = PostType.PFP)
            
        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        public_id = f"{'post' if type == PostType.POST else 'pfp'}_{new_post.id}"
        upload_creds = generate_upload_url()
        new_post.asset_url = get_download_url(public_id=public_id)
        
        db.commit()

        return {
            "post_id": new_post.id,
            "upload_url": upload_creds['upload_url'],
            "upload_preset": upload_creds['upload_preset'],
            "is_private": new_post.is_private,
            "public_id": public_id,
            
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"[SERVER ERROR] Failed to create post: {e}")
        # Traceback
        import traceback
        traceback.print_exc()
        # Log the error
        raise HTTPException(status_code=500, detail="Something went wrong while creating the post.")



def get_my_posts(db: Session, token: str, skip: int = 0, limit: int = 10, is_private: bool = None):
    try:
        user_id = get_user_id_from_token(token)
        query = db.query(Post).filter(Post.user_id == user_id, Post.type == PostType.POST)

        if is_private is not None:
            query = query.filter(Post.is_private == is_private)

        posts = query.offset(skip).limit(limit).all()
        for post in posts:
            print(post.id, post.asset_url, post.type, post.is_private)
        
        
        
        return [{"id": p.id, "asset_url": p.asset_url or "", "is_private": p.is_private, "type" : "post"} for p in posts]

    except Exception as e:
        print(f"[SERVER ERROR] Failed to fetch user's posts: {e}")
        raise HTTPException(status_code=500, detail="Could not retrieve posts.")


def get_post_by_id(db: Session, token: str, post_id: int):
    try:
        user_id = get_user_id_from_token(token)
        post = db.query(Post).filter(Post.id == post_id).first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        if post.user_id == user_id or not post.is_private:
            return {
                "id": post.id,
                "asset_url": post.asset_url,
                "is_private": post.is_private,
                "user_id": post.user_id,
                "type" : post.type
            }

        raise HTTPException(status_code=403, detail="Unauthorized to view this private post")

    except HTTPException:
        raise
    except Exception as e:
        print(f"[SERVER ERROR] Failed to retrieve post {post_id}: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong while retrieving the post.")


def update_post(db: Session, token: str, post_id: int, is_private: bool):
    try:
        user_id = get_user_id_from_token(token)
        post = db.query(Post).filter(Post.id == post_id).first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        if post.user_id != user_id:
            raise HTTPException(status_code=403, detail="You don't own this post")

        post.is_private = is_private
        db.commit()
        db.refresh(post)

        return {"id": post.id, "asset_url": post.asset_url, "is_private": post.is_private}

    except HTTPException:
        raise
    except Exception as e:
        print(f"[SERVER ERROR] Failed to update post {post_id}: {e}")
        raise HTTPException(status_code=500, detail="Could not update post.")

def update_pfp(db: Session, token: str):
    try:
        user_id = get_user_id_from_token(token)
        post = db.query(Post).filter(Post.id == post_id).first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        if post.user_id != user_id:
            raise HTTPException(status_code=403, detail="You don't own this post")

        post.is_private = is_private
        db.commit()
        db.refresh(post)

        return {"id": post.id, "asset_url": post.asset_url, "is_private": post.is_private}

    except HTTPException:
        raise
    except Exception as e:
        print(f"[SERVER ERROR] Failed to update post {post_id}: {e}")
        raise HTTPException(status_code=500, detail="Could not update post.")


def delete_post(db: Session, token: str, post_id: int):
    try:
        user_id = get_user_id_from_token(token)
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

    except HTTPException:
        raise
    except Exception as e:
        print(f"[SERVER ERROR] Failed to delete post {post_id}: {e}")
        raise HTTPException(status_code=500, detail="Could not delete post.")
