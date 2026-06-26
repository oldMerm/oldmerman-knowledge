import json
from datetime import datetime
from enum import Enum
from typing import Optional, Any, List

from pydantic import BaseModel, Field


# 支持的模型枚举
class EMB_SUPPORT_ENUM(Enum):
    CHAT_GPT = 1
    BIG_MODEL = 2
    ALIBABA = 3


# 映射关系
# 全路径匹配
embedding_support: dict[str, EMB_SUPPORT_ENUM] = {
    "https://api.openai.com/v1": EMB_SUPPORT_ENUM.CHAT_GPT,
    "https://open.bigmodel.cn/api/paas/v4": EMB_SUPPORT_ENUM.BIG_MODEL,
}
# 模糊匹配
fuzzy_embedding_support: dict[str, EMB_SUPPORT_ENUM] = {
    "maas.aliyuncs.com": EMB_SUPPORT_ENUM.ALIBABA
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
    time: datetime = Field(default=datetime.now(), description="时间")


# 向量模型返回的统一格式
class CommonEmbedding(BaseModel):
    object: str
    index: Optional[int] = None
    embedding: List[float]


class CommonUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class CommonEmbeddingsResponded(BaseModel):
    object: str
    data: List[CommonEmbedding]
    model: str
    usage: CommonUsage


# utils
class EmbeddingUtils:

    @staticmethod
    def dict_to_request_obj(json_str: str) -> CommonEmbeddingsResponded:
        completion_dict = json.loads(json_str)
        usage = completion_dict.get("usage")
        return CommonEmbeddingsResponded(
            object=completion_dict["object"],
            data=[
                CommonEmbedding(
                    object=item["object"],
                    index=item["index"],
                    embedding=item["embedding"]
                )
                for item in completion_dict["data"]
            ],
            model=completion_dict["model"],
            usage=CommonUsage(
                prompt_tokens=usage.get("prompt_tokens"),
                completion_tokens=usage.get("completion_tokens", 0),
                total_tokens=usage.get("total_tokens")
            )
        )
