from fastapi import FastAPI
from app.api import routes
from app.db.base import Base
from app.db.session import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Everstory Friendship Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router, prefix="/friendship", tags=["Friendship"])

Base.metadata.create_all(bind=engine)
