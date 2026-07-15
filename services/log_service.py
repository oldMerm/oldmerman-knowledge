"""Description
The bus code about log

Date: 2026-7-15
Created by oldmerman
"""

from typing import List

from fastapi.params import Depends

from db.dao import TokensUsageRepository
from db.dao.models_group_repository import ModelsGroupRepository
from db.entities import ModelsGroup
from db.models import ModelsGroupRender
from common.utils import get_logger



logger = get_logger(__name__)


class LogService:

    def get_tokens_usage(self):
        return TokensUsageRepository.as_dependency().get_month_token_consume()

    def get_request_time_log(self):
        pass


def get_log_service() -> LogService:
    return LogService()
