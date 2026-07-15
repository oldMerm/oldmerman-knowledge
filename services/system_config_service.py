"""Description
系统配置相关业务代码

Date: 2026-7-5
Created by oldmerman
"""
from datetime import datetime
from enum import Enum
from typing import Any

from agents import set_default_model
from agents.rerank import set_rerank
from common.utils import get_logger, get_config_client
from config import SystemConfigConstants
from db.vector_connection import set_default_knowledge

logger = get_logger(__name__)

# 系统管理页面的对话测试功能，在此处进行配置
class ModelTypeEnum(Enum):
    CHAT = 1
    EMBEDDING = 2
    RERANK = 3

class SystemConfigService:

    def get_models_config(self, model_type: int = 1) -> dict:
        """
        获取Agent主要配置

        :return: dict[str, str]
        """
        if model_type == ModelTypeEnum.CHAT.value:
            return get_config_client().get_config(SystemConfigConstants.MODEL_CONFIG_KEY)
        elif model_type == ModelTypeEnum.EMBEDDING.value:
            # 嵌入模型与知识库绑定，故该配置主要存集合的名称
            return get_config_client().get_config(SystemConfigConstants.EMBEDDING_CONFIG_KEY)
        elif model_type == ModelTypeEnum.RERANK.value:
            return get_config_client().get_config(SystemConfigConstants.RERANK_CONFIG_KEY)
        else:
            logger.info(f"不存在功能类型： {model_type}")
            raise ValueError(f"不存在功能类型： {model_type}")


    def set_models_config(self, user_id, model_type: int = 1, is_enabled: bool = False, model_id: Any = None):
        if model_type == ModelTypeEnum.CHAT.value:
            set_default_model(user_id, model_id=int(model_id), is_enabled=is_enabled)
        elif model_type == ModelTypeEnum.EMBEDDING.value:
            set_default_knowledge(user_id, collection_name=model_id, is_enabled=is_enabled)
        elif model_type == ModelTypeEnum.RERANK.value:
            set_rerank(user_id, model_id=int(model_id), is_enabled=is_enabled)
        else:
            logger.info(f"不存在功能类型： {model_type}")
            raise ValueError(f"不存在功能类型： {model_type}")

def get_system_config_service() -> SystemConfigService:
    return SystemConfigService()


if __name__ == '__main__':
     service = get_system_config_service()
     service.set_models_config("cc1beec1-1588-417a-ac36-f5472100f7c7", model_type=1, is_enabled=True, model_id=1006)
     service.set_models_config("cc1beec1-1588-417a-ac36-f5472100f7c7", model_type=2, is_enabled=True, model_id="text_collection")
     service.set_models_config("cc1beec1-1588-417a-ac36-f5472100f7c7", model_type=3, is_enabled=True, model_id=1013)
