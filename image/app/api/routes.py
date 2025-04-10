from fastapi import APIRouter, UploadFile, File, Form, Header, HTTPException
from app.services.token_validator import validate_token_via_redis
from sqlalchemy.orm import Session
from app.models.image import Image
from app.core.config import settings
from app.services.uploader import upload_image_to_s3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import uuid
import json

router = APIRouter()

engine = create_engine(settings.DB_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
async def upload_image(
    visibility: str = Form(...),
    file: UploadFile = File(...),
    authorization: str = Header(None),
    db: Session = next(get_db())
):
    token = authorization.split(" ")[1] if authorization else None
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    result = validate_token_via_redis(token)
    if not result.get("valid"):
        raise HTTPException(status_code=403, detail="Invalid token")

    user_id = result["user"]["user_id"]

    url = upload_image_to_s3(file, file.filename)
    image = Image(user_id=user_id, url=url, visibility=visibility)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image
