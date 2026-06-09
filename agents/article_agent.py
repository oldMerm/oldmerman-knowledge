"""Description
文章Agent提供者，支持：
1. 生成文章摘要

Date: 2026-6-8
Created by oldmerman
"""
from langchain.agents import create_agent

from agents.model_provider import ModelProvider
from agents.prompt import DIGEST_PROMPT
from agents.tool import refresh_cache
from agents.tool.common import save_token_usage_to_db
from agents.types import ArticleSummaryContext

default_param = ModelProvider.get_model(model_name='deepseek-v4-flash', max_token=256)
default_agent = create_agent(
    model=default_param.model,
    system_prompt=DIGEST_PROMPT,
    context_schema=ArticleSummaryContext,
    middleware=[
        refresh_cache,
        save_token_usage_to_db
    ]
)

class ArticleAgentProvider:
    __default_agent = default_agent

    @classmethod
    def get_digest_agent(cls, model_id: int = None):
        if model_id:
            return create_agent(
                model=ModelProvider.get_model(model_id).model,
                system_prompt=DIGEST_PROMPT,
                context_schema=ArticleSummaryContext,
                middleware=[
                    refresh_cache,
                    save_token_usage_to_db
                ]
            )
        return cls.__default_agent
