"""Description
Model Initialization

Date: 2026-4-29
Created by oldmerman
"""

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from db.dao.models_repository import ModelsRepository
from utils import get_logger

logger = get_logger(__name__)


class ModelProvider:

    @staticmethod
    def get_model(model_id: int,
                  max_token: int = 1024,
                  temperature: float = 1.2) -> BaseChatModel:
        if temperature > 2 or temperature < 0:
            logger.warning(f"Invalid model temperature: {temperature}")
            raise ValueError(f"Invalid model temperature: {temperature}")

        dao = ModelsRepository.as_dependency()
        param = dao.select_model(model_id=model_id)

        return ChatOpenAI(
            model=param.model_name,
            base_url=param.base_url,
            api_key=param.api_key,
            temperature=temperature,
            max_tokens=max_token
        )


if __name__ == "__main__":
    model = ModelProvider.get_model(1006)
    res = model.invoke("牛逼 = 1，那2*牛逼=几？")
    print(res)
