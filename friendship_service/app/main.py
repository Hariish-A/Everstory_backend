from fastapi import FastAPI
from app.api import routes
from app.db.base import Base
from app.db.session import engine

app = FastAPI(title="Everstory Friendship Service")
app.include_router(routes.router, prefix="/friendship", tags=["Friendship"])

Base.metadata.create_all(bind=engine)
