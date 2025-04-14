from fastapi import FastAPI
from app.controllers import auth_controller
from app.db.base import Base
from app.db.session import engine
import os
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from tenacity import retry, wait_fixed, stop_after_attempt

app = FastAPI(
    title="Everstory Auth Service",
    description="Authentication microservice for user sign-up, login, and logout with JWT & Redis.",
    version="1.0.0",
    contact={
        "name": "Everstory Backend",
        "email": "support@everstory.io",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@retry(wait=wait_fixed(2), stop=stop_after_attempt(5))
def create_tables():
    Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup():
    create_tables()

app.include_router(auth_controller.router, prefix="/auth", tags=["Authentication"])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8010))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
