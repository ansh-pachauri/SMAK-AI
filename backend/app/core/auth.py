from typing import Awaitable, Callable
from secret import JWT_SECRET
import jwt
from fastapi import Request, Response
from fastapi.responses import JSONResponse


async def middlware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    # Bypass auth for selected routes and preflight
    path = request.url.path
    if request.method == "OPTIONS" or path in {"/signin", "/signup", "/health", "/docs", "/redoc", "/openapi.json"}:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"message": "Unauthorized from auth header"})

    token = auth_header.split(" ", 1)[1]

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.PyJWTError:
        return JSONResponse(status_code=401, content={"message": "Unauthorized from token decode payload"})

    request.state.user_id = payload.get("user_id")
    response = await call_next(request)
    return response