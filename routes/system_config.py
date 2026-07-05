"""Description
系统管理相关接口

Date: 2026-7-5
Created by oldmerman
"""
from fastapi import APIRouter
from fastapi.params import Depends

from common import Result
from services.system_config_service import SystemConfigService, get_system_config_service

router = APIRouter(prefix="system_config", tags=["系统配置"])


@router.get("/rerank", response_model=Result)
def get_rerank_config(
        service: SystemConfigService = Depends(get_system_config_service)
) -> Result[dict]:
    return Result.success(
        data=service.get_rerank_config()
    )