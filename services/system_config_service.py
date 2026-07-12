"""Description
系统配置相关业务代码

Date: 2026-7-5
Created by oldmerman
"""
from agents.rerank import get_rerank_config, set_rerank
from common.utils import get_logger, get_config_client

logger = get_logger(__name__)


class SystemConfigService:

    MODEL_CONFIG_KEY = "models_config"

    def get_models_config(self) -> dict:
        """
        获取Agent主要配置

        :return: dict[str, str]
        """
        return get_config_client().get_config(self.MODEL_CONFIG_KEY)

    def get_rerank_config(self):
        return get_rerank_config()

    def set_models_config(self):
        pass

    def set_rerank(self, user_id, model_id, is_enabled):
        if not model_id:
            set_rerank(user_id, enabled=is_enabled)
            return
        set_rerank(user_id, enabled=is_enabled, model_id=model_id)

def get_system_config_service() -> SystemConfigService:
    return SystemConfigService()
