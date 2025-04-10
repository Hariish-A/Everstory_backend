import redis
import json
import uuid
import time
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=6379, decode_responses=True)

def validate_token_via_redis(token: str, timeout: int = 3):
    req_id = str(uuid.uuid4())
    response_channel = f"auth:response:{req_id}"
    pubsub = r.pubsub()
    pubsub.subscribe(response_channel)

    r.publish("auth:validate_token", json.dumps({
        "token": token,
        "response_channel": response_channel
    }))

    start_time = time.time()
    for message in pubsub.listen():
        if message["type"] == "message":
            pubsub.unsubscribe(response_channel)
            return json.loads(message["data"])
        if time.time() - start_time > timeout:
            pubsub.unsubscribe(response_channel)
            return {"valid": False}
