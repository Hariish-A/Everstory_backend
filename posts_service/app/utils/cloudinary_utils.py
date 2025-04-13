import cloudinary
import cloudinary.uploader
from app.config.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

CLOUD_NAME = settings.CLOUDINARY_CLOUD_NAME
UPLOAD_PRESET = settings.CLOUDINARY_UNSIGNED_PRESET

def generate_upload_url():
    return {
        "upload_url": f"https://api.cloudinary.com/v1_1/{CLOUD_NAME}/image/upload",
        "upload_preset": UPLOAD_PRESET,
    }

def delete_asset_from_cloudinary(public_id: str):
    result = cloudinary.uploader.destroy(public_id, resource_type="auto")
    if result.get("result") not in ("ok", "not_found"):
        raise Exception(f"Failed to delete Cloudinary asset: {result}")

def get_download_url(public_id: str):
    return f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/{public_id}.jpg"
