"""Description
获取日志记录

Date: 2026-6-8
Created by oldmerman
"""
from typing import List

from fastapi import APIRouter
from fastapi.params import Depends

from common import Result
from db.models import TokensUsageCountParam
from common.utils import get_logger
from services.log_service import LogService, get_log_service

logger = get_logger(__name__)

router = APIRouter(prefix="/log", tags=["model"])


@router.get("/tokens_usage")
def get_tokens_usage(service: LogService = Depends(get_log_service)) -> Result[List[TokensUsageCountParam]]:
    return Result.success(
        data=service.get_tokens_usage() # 获取一个月内每日的token消耗
    )


@router.get("/time_request")
def get_request_time_log(service: LogService = Depends(get_log_service)) -> Result:
    return Result.success(
        data=service.get_request_time_log()
    )