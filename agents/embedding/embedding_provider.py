from enum import Enum
from typing import List, Any, Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Field

from utils import get_logger

"""Description
the embedding client getter

Date: 2026-5-25
Created by oldmerman
"""

logger = get_logger(__name__)

# 支持的模型枚举
class EMB_SUPPORT_ENUM(Enum):
    CHAT_GPT = 1,
    BIG_MODEL = 2
# 映射关系
embedding_support: dict[str, EMB_SUPPORT_ENUM] = {
    "https://api.openai.com/v1": EMB_SUPPORT_ENUM.CHAT_GPT,
    "https://https://open.bigmodel.cn/api/paas/v4": EMB_SUPPORT_ENUM.BIG_MODEL,
}
# 公共请求实体（向量）
class EmbeddingsGetterParam(BaseModel):
    api_key: str = Field(description="模型的api_key")
    base_url: str = Field(description="模型的base_url")
    model_name: Optional[str] = Field(description="模型名称")
    doc: List[Any] = Field(description="需要向量化的文档")
    dimensions: int = Field(default=1024, description="向量化的维度")

# 获取厂家的url获取，支持的向量模型
def get_embeddings_supported(api_key: str, base_url: str, param: EmbeddingsGetterParam):
    match embedding_support.get(base_url):
        case EMB_SUPPORT_ENUM.CHAT_GPT:
            return None
        case EMB_SUPPORT_ENUM.BIG_MODEL:
            # return get_zhi_pu_embedding(api_key)
            return None
        case _:
            logger.info("暂不支持该类模型")
            raise ValueError("暂不支持该类模型")


if __name__ == "__main__":
    parsed = urlparse("https://api.deepseek.com")
