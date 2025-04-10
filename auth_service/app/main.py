from fastapi import FastAPI
from app.controllers import auth_controller
from app.db.base import Base
from app.db.session import engine

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

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth_controller.router, prefix="/auth", tags=["Authentication"])
