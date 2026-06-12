"""Description
文章Agent提供者，支持：
1. 生成文章摘要

Date: 2026-6-8
Created by oldmerman
"""
from functools import lru_cache

from langchain.agents import create_agent

from agents.model_provider import ModelProvider
from agents.prompt import DIGEST_PROMPT
from agents.tool import refresh_cache
from agents.tool.common import save_token_usage_to_db
from agents.types import ArticleContext

@lru_cache(maxsize=2)
def get_digest_agent(model_id: int = None):
    """获取文章摘要 Agent（自动缓存）"""
    if model_id:
        model = ModelProvider.get_model(model_id)
    else:
        # 默认模型可以配置化
        model = ModelProvider.get_model(
            model_name=ModelProvider.DEFAULT_MODEL_NAME,
        )

    return create_agent(
        model=model.model,
        system_prompt=DIGEST_PROMPT,
        context_schema=ArticleContext,
        middleware=[
            refresh_cache,
            save_token_usage_to_db
        ]
    )