import cloudinary
import cloudinary.uploader
from app.config.config import settings
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

CLOUD_NAME = settings.CLOUDINARY_CLOUD_NAME
UPLOAD_PRESET = settings.CLOUDINARY_UNSIGNED_PRESET


"""
curl -X POST upload_url \
-F file=@filepath \
-F upload_preset=preset \
-F public_id=id    
"""


def generate_upload_url() :
    
    upload_url = f"https://api.cloudinary.com/v1_1/{CLOUD_NAME}/image/upload"

    upload_fields = {
        "upload_url": upload_url,
        "upload_preset": UPLOAD_PRESET,
    }
    return upload_fields

def delete_asset_from_cloudinary(public_id: str):
    try:
        result = cloudinary.uploader.destroy(public_id, resource_type="auto")
        if result.get("result") not in ("ok", "not_found"):
            raise Exception(f"[POSTS SERVICE - CLOUDINARY]   |   Unexpected Cloudinary delete result: {result}")
    except Exception as e:
        logger.error(f"[POSTS SERVICE - CLOUDINARY]   |   Failed to delete Cloudinary asset {public_id}: {e}")
        raise HTTPException(status_code=500, detail="Cloudinary deletion failed.")


def get_download_url(public_id :str):
    return f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/{public_id}.jpg"
     