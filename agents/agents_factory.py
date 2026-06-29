"""Description
简单工厂，提供已配置的Agent

Date: 2026-6-22
Created by oldmerman
"""
from agents.article_agent import get_digest_agent
from agents.common_agent import get_common_agent
from agents.types import AgentParam
from typing import Optional, Dict, Callable


# 使用枚举或常量定义 Agent 类型
class AgentType:
    COMMON = "common"
    ARTICLE = "article"
    DIGEST = "article"  # 别名


# 注册表
PROCESSOR_FACTORY: Dict[str, Callable[[Optional[int]], AgentParam]] = {
    AgentType.COMMON: get_common_agent,
    AgentType.ARTICLE: get_digest_agent,
}


def get_available_types() -> list:
    """获取所有可用的 Agent 类型"""
    return list(PROCESSOR_FACTORY.keys())


class AgentsFactory:
    """Agent 工厂类"""

    def __init__(self, model_id: Optional[int] = None):
        self.model_id = model_id
        self._default_type = AgentType.COMMON

    def build_agent(self, processor_type: Optional[str] = None) -> AgentParam:
        """
        组装 Agent 对象

        Args:
            processor_type: Agent 类型，若为空或不存在则返回默认值

        Returns:
            AgentParam: Agent 参数对象
        """
        # 如果 processor_type 为空或不存在，使用默认类型
        if not processor_type or processor_type not in PROCESSOR_FACTORY:
            processor_type = self._default_type

        # 获取对应的创建函数并执行
        creator = PROCESSOR_FACTORY[processor_type]
        return creator(self.model_id)

    def register_agent(self, agent_type: str, creator: Callable):
        """动态注册新的 Agent 类型（扩展性）"""
        PROCESSOR_FACTORY[agent_type] = creator
        return self