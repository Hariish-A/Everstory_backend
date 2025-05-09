import os
import uvicorn
from fastapi import FastAPI
from app.controllers import post_controller
from app.db.base import Base
from app.db.session import engine
from fastapi.middleware.cors import CORSMiddleware
from tenacity import retry, stop_after_attempt, wait_fixed

app = FastAPI(
    title="Everstory Posts Service",
    description="Handles encrypted/compressed post creation & upload via Cloudinary.",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def create_tables():
    Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup():
    create_tables()

# Add routes
app.include_router(post_controller.router, prefix="/posts", tags=["Posts"])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8020))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
