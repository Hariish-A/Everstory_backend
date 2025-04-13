import httpx
from fastapi import APIRouter, Request
from app.config.config import settings

router = APIRouter()

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_frienship(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{settings.FRIENDSHIP_SERVICE_URL}/friendship/{path}"
        response = await client.request(
            method=request.method,
            url=url,
            headers=request.headers.raw,
            content=await request.body()
        )
        return response.json()
