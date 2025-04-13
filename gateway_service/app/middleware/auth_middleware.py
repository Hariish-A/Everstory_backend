# app/middleware/auth_middleware.py

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import httpx

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Skip auth for public/docs/auth
        if path.startswith("/auth") or path in ["/", "/docs", "/openapi.json"]:
            return await call_next(request)

        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

        token = auth_header.split(" ")[1]

        # Verify token with Auth service
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(
                    "http://auth-service:8010/auth/me",
                    headers={"Authorization": f"Bearer {token}"}
                )
                resp.raise_for_status()
            except httpx.HTTPStatusError:
                raise HTTPException(status_code=401, detail="Invalid or expired token")

        payload = resp.json()

        # Ensure required fields exist
        if "id" not in payload:
            raise HTTPException(status_code=401, detail="User ID missing in auth payload")

        # Inject into headers for internal services
        request.scope["headers"].append((b"x-user-id", str(payload["id"]).encode()))

        # Optional: inject role only if present
        if "role" in payload:
            request.scope["headers"].append((b"x-user-role", payload["role"].encode()))

        return await call_next(request)
