import httpx
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.friendship_schema import FriendResponse
from app.config.config import settings

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(
                f"{settings.GATEWAY_URL}/auth/me",
                headers={"Authorization": f"Bearer {credentials.credentials}"}
            )
            res.raise_for_status()
            if res.status_code != 200:
                raise HTTPException(status_code=res.status_code, detail="Unauthorized")
            return res.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Unauthorized")
