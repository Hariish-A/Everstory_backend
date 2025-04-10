import redis
from app.config.config import settings

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)

def blacklist_token(token: str):
    redis_client.set(token, "blacklisted")

def is_token_blacklisted(token: str) -> bool:
    return redis_client.exists(token)
