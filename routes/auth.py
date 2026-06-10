"""Description
Controller about auth

Date: 2026-4-23
Created by oldmerman
"""

import os

from fastapi import APIRouter, Request
from fastapi.params import Depends

from dotenv import load_dotenv
from common.Result import Result
from db.models import LoginResponse, RegisterRequest, LoginRequest
from services import get_auth_service
from services.auth_service import AuthService
from utils.logger import get_logger



load_dotenv()

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/verify", response_model=Result)
def verify():
    return Result.success(message="success")


@router.post("/register", response_model=Result[LoginResponse])
def register(request: RegisterRequest,
                   req: Request,
                   service: AuthService = Depends(get_auth_service)):
    logger.info(f"Register attempt: {request.username}")
    try:
        ip_address = req.client.host if req.client else None
        if request.secretKey != os.getenv("SYSTEM_REGISTER_SECRET"):
            return Result.error(message="Secret failed")
        service.register(
            username=request.username,
            password=request.password,
            email=request.email,
            phone=request.phone,
            ip_address=ip_address,
        )
        token = service.login(request.username, request.password, ip_address)
        return Result.success(data=LoginResponse(access_token=token))
    except ValueError as e:
        logger.warning(f"Registration failed: {e}")
        return Result.error(message=str(e), code=400)


@router.post("/login", response_model=Result[LoginResponse])
def login(request: LoginRequest,
                req: Request,
                service: AuthService = Depends(get_auth_service)):
    logger.info(f"Login attempt: {request.username}")
    try:
        ip_address = req.client.host if req.client else None
        token = service.login(request.username, request.password, ip_address)
        return Result.success(data=LoginResponse(access_token=token))
    except ValueError as e:
        logger.warning(f"Login failed: {e}")
        return Result.error(message=str(e), code=401)


@router.post("/logout", response_model=Result)
def logout(service: AuthService = Depends(get_auth_service)):
    service.logout()
    return Result.success(message="Logged out successfully")