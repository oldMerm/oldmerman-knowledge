"""Description
Deal with the response, add request info if not

Date: 2026-4-22
Created by oldmerman
"""

from typing import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from common.Result import Result



class ResponseWrapperMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        path = str(request.url.path)

        if isinstance(response, JSONResponse):
            body = response.body
            if body:
                data = Result.model_validate_json(body)
                if hasattr(data, 'request') and not data.request:
                    data.request = path
                    return JSONResponse(
                        content=data.model_dump(),
                        status_code=response.status_code,
                        headers=dict(response.headers),
                        media_type=response.media_type
                    )

        return response