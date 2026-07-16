"""Description
The bus code about log

Date: 2026-7-15
Created by oldmerman
"""

from typing import List

import math
from fastapi.params import Depends

from common import Page
from db.dao import TokensUsageRepository
from db.dao.models_group_repository import ModelsGroupRepository
from db.dao.request_time_log_repository import RequestTimeLogRepository
from db.entities import ModelsGroup
from db.models import ModelsGroupRender, RequestTimeLogParam
from common.utils import get_logger



logger = get_logger(__name__)


class LogService:

    def get_tokens_usage(self):
        return TokensUsageRepository.as_dependency().get_month_token_consume()

    def get_log_count(self):
        dao = RequestTimeLogRepository.as_dependency()
        user_list = [
            i.split("-")[0]
            for i in dao.log_user_count()
        ]
        param = dao.log_count()
        param.user_count = len(set(user_list))
        return param

    def get_log_page(self, current, size):
        offset = (current - 1) * size
        dao = RequestTimeLogRepository.as_dependency()

        total_records = dao.count()
        page_num = math.ceil(total_records / size)

        origin_page = dao.log_page(size, offset)
        page_data = [
            RequestTimeLogParam(
                username=i.thread_id.split("-")[0],
                total_duration=i.total_duration,
                prompt=i.prompt,
                created_at=i.created_at,
                model_id=i.model_id
            )
            for i in origin_page
        ]
        return Page(
            current=current,
            size=size,
            total=total_records,
            page_num=page_num,
            data=page_data
        )



def get_log_service() -> LogService:
    return LogService()


if __name__ == "__main__":
    service = get_log_service()
    print(service.get_log_page(1, 3))