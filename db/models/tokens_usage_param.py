from datetime import datetime

from pydantic import BaseModel, Field


class TokensUsageCountParam(BaseModel):
    date: datetime = Field(description="对应的日期，按天算")
    prompt_tokens_consume: int = Field(default=0, description="提示词token总消耗")
    completion_tokens_consume: int = Field(default=0, description="补全token总消耗")
    total_tokens_consume: int = Field(default=0, description="token总消耗")