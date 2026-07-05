"""Description
系统配置相关业务代码

Date: 2026-7-5
Created by oldmerman
"""
from agents.rerank import get_rerank_config
from utils import get_logger

logger = get_logger(__name__)


class SystemConfigService:

    def get_rerank_config(self):
        return get_rerank_config()


def get_system_config_service() -> SystemConfigService:
    return SystemConfigService()
