from anyio.functools import lru_cache
from langchain.agents import create_agent

from agents.model_provider import ModelProvider
from agents.tool import save_token_usage_to_db
from agents.types import CommonContext, AgentParam


@lru_cache(maxsize=10)
def get_common_agent(model_id: int = None) -> AgentParam:
    """获取通用智能体，用于完成简单的业务"""
    if model_id:
        model = ModelProvider.get_model(model_id)
    else:
        model = ModelProvider.get_model(
            model_name=ModelProvider.DEFAULT_MODEL_NAME
        )

    return AgentParam(
        agent=create_agent(
            model=model.model,
            context_schema=CommonContext,
            middleware=[
                save_token_usage_to_db
            ]
        ),
        model_id=model.model_id,
        model_name=model.model_name,
    )
