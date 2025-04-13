import httpx
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config.config import settings

security = HTTPBearer()


async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.AUTH_VERIFY_URL}",
                headers={"Authorization": f"Bearer {credentials.credentials}"}
            )
            response.raise_for_status()
            payload = response.json()
            return {
                "id": payload["id"],
                "role": payload.get("role"),
                "token": credentials.credentials
            }
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Invalid or expired token")
    