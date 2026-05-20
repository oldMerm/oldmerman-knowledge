from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from common.Result import Result

"""Description
The exception handler about the project 

Date: 2026-4-22
Created by oldmerman
"""


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=Result.error(
            message=exc.detail,
            code=exc.status_code,
            request=str(request.url.path)
        ).model_dump(),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=Result.error(
            message=str(exc),
            code=422,
            request=str(request.url.path)
        ).model_dump(),
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=Result.error(
            message=str(exc),
            code=500,
            request=str(request.url.path)
        ).model_dump(),
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)