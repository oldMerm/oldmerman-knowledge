"""Description
获取token消耗日志记录

Date: 2026-6-8
Created by oldmerman
"""
from typing import List

from fastapi import APIRouter
from fastapi.params import Depends

from common import Result
from db.dao.tokens_usage_repository import TokensUsageRepository
from db.models import TokensUsageCountParam
from common.utils import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/tokens_usage", tags=["model"])


def get_tokens_usage_repository() -> TokensUsageRepository:
    return TokensUsageRepository()


@router.get("")
def get_month_consume(dao: TokensUsageRepository = Depends(get_tokens_usage_repository)) -> Result[List[TokensUsageCountParam]]:
    return Result.success(
        data=dao.get_month_token_consume() # 获取一个月内每日的token消耗
    )

