"""Description
提供Agent的公共配置，如上下文，自定义状态参数等

Date: 2026-6-8
Created by oldmerman
"""
from typing import Any

from pydantic import BaseModel


class CommonContext(BaseModel):
    user_id: str = "11111111-1111-1111-1111-111111111111"
    model_id: int
    model_name: str

class AgentParam(BaseModel):
    agent: Any
    model_id: int
    model_name: str