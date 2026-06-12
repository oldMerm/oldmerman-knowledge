"""Description
Model Initialization

Date: 2026-4-29
Created by oldmerman
"""
from functools import lru_cache

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from db.dao.models_repository import ModelsRepository
from utils import get_logger

logger = get_logger(__name__)


class ModelCommonParam(BaseModel):
    model_id: int
    model_name: str
    model: ChatOpenAI


class ModelProvider:

    DEFAULT_MODEL_NAME = "deepseek-v4-flash"

    @classmethod
    @lru_cache(maxsize=5)
    def get_model(cls, model_id: int = None,
                  model_name: str = None,
                  max_token: int = 1024,
                  temperature: float = 1.2) -> ModelCommonParam:
        if model_name is None and model_id is None:
            model_name = cls.DEFAULT_MODEL_NAME

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


if __name__ == "__main__":
    model = ModelProvider.get_model(1006)
    res = model.invoke("牛逼 = 1，那2*牛逼=几？")
    print(res)
