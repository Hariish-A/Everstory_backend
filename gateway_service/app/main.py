from fastapi import FastAPI
from app.routes import auth_proxy, posts_proxy, friendship_proxy
from app.config.config import settings
import uvicorn
import os
from app.middleware.auth_middleware import AuthMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Everstory Gateway",
    description="Routes frontend requests to internal microservices",
    version="1.0.0"
)

# Add CORS support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","*"],    # TODO: Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_proxy.router, prefix="/auth", tags=["Auth"])
app.include_router(posts_proxy.router, prefix="/posts", tags=["Posts"])
app.include_router(friendship_proxy.router, prefix="/friendship", tags=["Friendship"])

# Auth middleware
app.add_middleware(AuthMiddleware)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
