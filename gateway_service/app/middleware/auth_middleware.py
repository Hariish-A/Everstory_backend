from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import httpx

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Skip auth for public or auth routes
        if path.startswith("/auth") or path in ["/", "/docs", "/openapi.json"]:
            return await call_next(request)

        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

        token = auth_header.split(" ")[1]

        # Verify token with auth service
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(
                    "http://auth-service:8010/auth/verify-token",
                    headers={"Authorization": f"Bearer {token}"}
                )
                resp.raise_for_status()
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=401, detail="Invalid token")

        payload = resp.json()
        request.state.user_id = payload.get("user_id")
        request.state.role = payload.get("role")

        # Inject into headers for downstream services
        request.scope["headers"].append((b"x-user-id", str(payload["user_id"]).encode()))
        request.scope["headers"].append((b"x-user-role", payload["role"].encode()))

        return await call_next(request)
