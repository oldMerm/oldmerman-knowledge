from anyio.functools import lru_cache
from langchain.agents import create_agent

from agents.model_provider import ModelProvider
from agents.prompt import COMMON_PROMPT
from agents.tool import trim_chat_messages, save_token_usage_to_db
from agents.types import CommonContext, AgentParam
from db.langgraph_checkpointer import get_checkpointer


@lru_cache(maxsize=10)
def get_common_agent(model_id: int = None) -> AgentParam:
    """获取通用智能体，用于完成简单的业务"""
    if model_id:
        model = ModelProvider.get_model(model_id)
    else:
        model = ModelProvider.get_model(
            model_name=ModelProvider.DEFAULT_MODEL_NAME
        )

    # 初始化检查点
    checkpointer = get_checkpointer()
    return AgentParam(
        agent=create_agent(
            model=model.model,
            context_schema=CommonContext,
            system_prompt=COMMON_PROMPT,
            middleware=[
                trim_chat_messages,
                save_token_usage_to_db
            ],
            checkpointer=checkpointer
        ),
        model_id=model.model_id,
        model_name=model.model_name,
    )
