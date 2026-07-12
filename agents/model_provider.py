"""Description
Model Initialization

Date: 2026-4-29
Created by oldmerman
"""
from datetime import datetime
from functools import lru_cache

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from db.dao.models_repository import ModelsRepository
from common.utils import get_logger, get_config_client

logger = get_logger(__name__)


class ModelCommonParam(BaseModel):
    model_id: int
    model_name: str
    model: ChatOpenAI


class ModelProvider:

    DEFAULT_MODEL_KEY = "default_model"

    @classmethod
    def set_default_model(cls, user_id: str, model_id: int):
        dao = ModelsRepository.as_dependency()
        param = dao.select_model(model_id=model_id)
        config_dict = {
            "is_enabled": True,
            "base_url": param.base_url,
            "api_key": param.api_key,
            "model_name": param.model_name,
            "model_id": param.model_id,
            "updated_at": datetime.now()
        }
        get_config_client().set_config(key=cls.DEFAULT_MODEL_KEY, new_config=config_dict,
                                       user_id=user_id, description="默认使用的大语言模型")

    @classmethod
    @lru_cache(maxsize=5)
    def get_model(cls, model_id: int = None,
                  model_name: str = None,
                  max_token: int = 1024,
                  temperature: float = 1.2) -> ModelCommonParam:
        # 不传参，默认读取公共配置的模型
        if model_name is None and model_id is None:
            config_dict = get_config_client().get_config(cls.DEFAULT_MODEL_KEY)

            assert config_dict is not None
            if config_dict.get("is_enabled"):
                model_id = config_dict.get("model_id")
                model_name = config_dict.get("model_name")
                base_url = config_dict.get("base_url")
                api_key = config_dict.get("api_key")

                if not model_id or not model_name or not base_url or not api_key:
                    raise ValueError("模型参数缺失")

                return ModelCommonParam(
                    model_id=model_id,
                    model_name=model_name,
                    model=ChatOpenAI(
                        model=model_name,
                        base_url=base_url,
                        api_key=api_key,
                        temperature=temperature,
                        max_tokens=max_token
                    )
                )

        if temperature > 2 or temperature < 0:
            logger.warning(f"Invalid model temperature: {temperature}")
            raise ValueError(f"Invalid model temperature: {temperature}")

        dao = ModelsRepository.as_dependency()
        if model_id:
            param = dao.select_model(model_id=model_id)
        elif model_name:
            param = dao.select_model_by_name(model_name=model_name)
        else:
            raise ValueError("error param for agent")

        return ModelCommonParam(
            model_id=param.id,
            model_name=param.model_name,
            model=ChatOpenAI(
                model=param.model_name,
                base_url=param.base_url,
                api_key=param.api_key,
                temperature=temperature,
                max_tokens=max_token
            )
        )
