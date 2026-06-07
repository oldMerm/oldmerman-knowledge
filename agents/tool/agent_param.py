"""Description
custom agent param for langchain

Date: 2026-6-6
Created by oldmerman
"""
from langchain.agents import AgentState
from pydantic import BaseModel, Field


class SimpleCustomContext(BaseModel):
    user_id: str = Field(description="用户id", default=None)

class SimpleCustomState(AgentState):
    pass