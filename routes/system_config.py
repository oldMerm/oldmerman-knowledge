"""Description
系统管理相关接口

Date: 2026-7-5
Created by oldmerman
"""
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.params import Depends
from pydantic import BaseModel

from common import Result
from common.utils import UserContext
from services.system_config_service import SystemConfigService, get_system_config_service

router = APIRouter(prefix="/system_config", tags=["系统配置"])


class ModelConfigSetter(BaseModel):
    model_id: Optional[int | str]
    model_type: int
    is_enabled: bool = False


@router.get("/model", response_model=Result)
def get_models_config(model_type: Optional[int],
                      service: SystemConfigService = Depends(get_system_config_service)):
    return Result.success(
        data=service.get_models_config(model_type)
    )

@router.post("/model", response_model=Result)
def set_model_config(
        setter: ModelConfigSetter,
        req: Request,
        service: SystemConfigService = Depends(get_system_config_service)
):
       user_id = UserContext.get_user_id(req)
       service.set_models_config(user_id, setter.model_id, setter.is_enabled)
       return Result.success()