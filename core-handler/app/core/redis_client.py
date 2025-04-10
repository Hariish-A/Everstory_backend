import redis
import json
import uuid
from app.core.config import settings
from app.core.db import get_auth_db
from app.core.auth_utils import validate_token

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)

def listen_for_token_validation():
    pubsub = r.pubsub()
    pubsub.subscribe("auth:validate_token")
    print("[core-handler] Listening for token validation...")

    for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            token = data.get("token")
            response_channel = data.get("response_channel")

            with next(get_auth_db()) as db:
                user_info = validate_token(token, db)

            response = {"valid": bool(user_info), "user": user_info}
            r.publish(response_channel, json.dumps(response))
