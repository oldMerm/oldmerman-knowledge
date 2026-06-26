"""Description
Intercept the corresponding path and verify the signature

Date: 2026-4-22
Created by oldmerman
"""
from typing import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from common.Result import Result
from utils.jwt import verify_token

EXCLUDED_PATHS = [
    "/",
    "/docs",
    "/redoc",
    "/hello",
    "/openapi.json",
    "/auth/login", "/auth/register", # /routes/auth
    "/model_type/vector-models",
    "/v1",
    "/chat"
]


EXCLUDED_PATH_PREFIXES = [
    # "/model_type",
]

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        path = request.url.path

        if request.method == "OPTIONS":
            return await call_next(request)

        if path in EXCLUDED_PATHS:
            return await call_next(request)

        for prefix in EXCLUDED_PATH_PREFIXES:
            if path.startswith(prefix):
                return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content=Result.error(
                    message="Missing or invalid Authorization header",
                    code=401,
                    request=path
                ).model_dump()
            )

        token = auth_header.replace("Bearer ", "")
        try:
            token_data = verify_token(token)
            request.state.user = token_data
        except Exception as e:
            return JSONResponse(
                status_code=401,
                content=Result.error(
                    message=str(e),
                    code=401,
                    request=path
                ).model_dump()
            )

        return await call_next(request)