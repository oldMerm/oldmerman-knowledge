from datetime import datetime
from enum import Enum
from typing import Optional, Any, List

from pydantic import BaseModel, Field

# 支持的模型枚举
class EMB_SUPPORT_ENUM(Enum):
    CHAT_GPT = 1,
    BIG_MODEL = 2
# 映射关系
embedding_support: dict[str, EMB_SUPPORT_ENUM] = {
    "https://api.openai.com/v1": EMB_SUPPORT_ENUM.CHAT_GPT,
    "https://open.bigmodel.cn/api/paas/v4": EMB_SUPPORT_ENUM.BIG_MODEL,
}

# 嵌入模型提供商参数
class EmbeddingsProviderCommonParam(BaseModel):
    model_name: str = Field(description="模型名称")
    dimensions: List[int] = Field(description="模型支持的向量")
    chunk_size: int = Field(description="模型支持的最大批处理")
    max_context: int = Field(description="单条的最大token数")
# 公共请求实体（向量）
class EmbeddingsGetterParam(BaseModel):
    api_key: str = Field(description="模型的api_key")
    base_url: str = Field(description="模型的base_url")
    model_name: Optional[str] = Field(description="模型名称")
    doc: List[Any] = Field(description="需要向量化的文档")
    dimensions: int = Field(default=1024, description="向量化的维度")
# 公共响应实体（向量）
class EmbeddingsResponseParam(BaseModel):
    model_name: str = Field(description="模型名称")
    data: List[Any] = Field(description="向量化的结果")
    tokens: dict[str, int] = Field(description="token消耗记录")
    time: datetime = Field(default=datetime.now(),description="时间")











