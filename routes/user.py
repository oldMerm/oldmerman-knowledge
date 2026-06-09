"""Description
Controller about Users

Date: 2026-4-26
Created by oldmerman
"""
from fastapi import APIRouter, Request
from fastapi.params import Depends

from common.Result import Result
from db.models.user_param import UserSettingParam, UpdateUsernameRequest
from services import get_user_service
from services.user_service import UserService
from utils import UserContext
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/setting", response_model=Result[UserSettingParam])
def get_user_setting(req: Request, service: UserService = Depends(get_user_service)):
    user_uuid = UserContext.get_user_id(req)
    if not user_uuid:
        return Result.error(message="Unauthorized", code=401)

    user = service.get_user_by_uuid(user_uuid)
    if not user:
        return Result.error(message="User not found", code=404)

    phone = service.obfuscate_phone(user.phone)
    return Result.success(
        data=UserSettingParam(
            user_uuid=user.user_uuid,
            username=user.username,
            email=user.email,
            phone=phone,
            status=user.status.value,
        )
    )


@router.post("/setting", response_model=Result)
def update_user_setting(request: UpdateUsernameRequest,
                        req: Request,
                        service: UserService = Depends(get_user_service)):
    user_uuid = UserContext.get_user_id(req)
    if not user_uuid:
        return Result.error(message="Unauthorized", code=401)

    success = service.update_username(user_uuid, request.username)
    if not success:
        return Result.error(message="User not found", code=404)

    return Result.success(message="Username updated successfully")
