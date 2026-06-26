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
    from openai import OpenAI

    param = ModelsRepository.as_dependency().select_model(1012)
    client = OpenAI(
        api_key=param.api_key,
        base_url=param.base_url
    )

    response = client.chat.completions.create(
        model="deepseek-v4-pro",  # 必须是 pro 版本
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "请描述这张图片的内容",
             "image_url": "https://pic2.zhimg.com/v2-ada4f54f24990920bf4dc508d6d4bac9_1440w.jpg"},
        ],
        stream=False,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )

    print(response.choices[0].message.content)
