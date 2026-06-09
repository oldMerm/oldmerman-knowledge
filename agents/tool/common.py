"""Description
公共的agent工具

Date: 2026-6-8
Created by oldmerman
"""
from langchain.agents import AgentState
from langchain.agents.middleware import after_model
from langgraph.prebuilt import ToolRuntime

from agents.types import CommonContext
from db.dao.tokens_usage_repository import TokensUsageRepository

@after_model
def save_token_usage_to_db(
        state: AgentState,
        runtime: ToolRuntime[CommonContext]
) -> None:
    """保存token使用统计到数据库"""
    last_message = state['messages'][-1]
    model_id = runtime.context.model_id
    user_id = runtime.context.user_id
    if hasattr(last_message, 'usage_metadata'):
        usage = last_message.usage_metadata
        tokens = {
            'prompt_tokens': usage.get('input_tokens', 0),
            'completion_tokens': usage.get('output_tokens', 0),
            'total_tokens': usage.get('total_tokens', 0)
        }
        dto = TokensUsageRepository.as_dependency()
        dto.add(user_id=user_id, model_id=model_id, tokens=tokens)