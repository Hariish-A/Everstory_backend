from fastapi import FastAPI
from app.routes import auth_proxy, posts_proxy
from app.config.config import settings
import uvicorn
import os
from app.middleware.auth_middleware import AuthMiddleware

app = FastAPI(
    title="Everstory Gateway",
    description="Routes frontend requests to internal microservices",
    version="1.0.0"
)

app.include_router(auth_proxy.router, prefix="/auth", tags=["Auth"])
app.include_router(posts_proxy.router, prefix="/posts", tags=["Posts"])

app.add_middleware(AuthMiddleware)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)



# USAGE OF AuthMiddleware

# def get_user_id(x_user_id: str = Header(None)):
#     if not x_user_id:
#         raise HTTPException(status_code=401, detail="Missing user ID")
#     return int(x_user_id)

# @router.get("/me/posts")
# def get_my_posts(user_id: int = Depends(get_user_id)):
#     ...
