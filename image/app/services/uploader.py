import boto3
from uuid import uuid4
from app.core.config import settings

s3 = boto3.client(
    's3',
    aws_access_key_id=settings.S3_KEY,
    aws_secret_access_key=settings.S3_SECRET,
    region_name=settings.REGION
)

def upload_image_to_s3(file, filename):
    unique_name = f"{uuid4()}_{filename}"
    s3.upload_fileobj(file.file, settings.S3_BUCKET, unique_name, ExtraArgs={"ACL": "public-read"})
    return f"https://{settings.S3_BUCKET}.s3.{settings.REGION}.amazonaws.com/{unique_name}"
