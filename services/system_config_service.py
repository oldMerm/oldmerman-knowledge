"""Description
系统配置相关业务代码

Date: 2026-7-5
Created by oldmerman
"""
from agents.rerank import get_rerank_config, set_rerank
from common.utils import get_logger

logger = get_logger(__name__)


class SystemConfigService:

    def get_rerank_config(self):
        return get_rerank_config()

    def set_rerank(self, user_id, model_id, is_enabled):
        if not model_id:
            set_rerank(user_id, enabled=is_enabled)
            return
        set_rerank(user_id, enabled=is_enabled, model_id=model_id)

def get_system_config_service() -> SystemConfigService:
    return SystemConfigService()
