"""Description
the embedding client getter

Date: 2026-5-25
Created by oldmerman
"""
from typing import Optional, Type

from dotenv import load_dotenv

from agents.embedding.alibaba_embedding import AlibabaEmbedding
from agents.embedding.embedding_base import BaseEmbeddingAdapter
from agents.embedding.embedding_common import EmbeddingsGetterParam, EmbeddingsResponseParam
from agents.embedding.zhi_pu_embedding import ZhiPuEmbedding
from utils import get_logger

load_dotenv()
logger = get_logger(__name__)

# 映射关系
# 全路径匹配
embedding_support: dict[str, Type[BaseEmbeddingAdapter]] = {
    "https://open.bigmodel.cn/api/paas/v4": ZhiPuEmbedding,
}
# 模糊匹配
fuzzy_embedding_support: dict[str, Type[BaseEmbeddingAdapter]] = {
    "maas.aliyuncs.com": AlibabaEmbedding
}

class EmbeddingFactory:
    """工厂类，根据配置返回对应的向量适配器"""
    @classmethod
    def get_adapter(cls, base_url: str) -> BaseEmbeddingAdapter:
        # 直接匹配
        adapter_cls = embedding_support.get(base_url)
        if adapter_cls:
            return adapter_cls()

        # 模糊匹配
        pre_key = None
        for key in fuzzy_embedding_support.keys():
            if key in base_url:
                pre_key = key
        adapter_cls = fuzzy_embedding_support.get(pre_key)
        if not adapter_cls:
            raise ValueError(f"暂不支持厂商，URL：{base_url}")
        return adapter_cls()


# 获取厂家的url获取，支持的向量模型
def get_embeddings_supported(param: EmbeddingsGetterParam, isSimple: bool = True) -> Optional[EmbeddingsResponseParam]:
    if not param.api_key or not param.base_url or len(param.doc) == 0:
        logger.error("请求参数为空！")
        raise ValueError("请求参数为空！")
    base_url = param.base_url
    adapter = EmbeddingFactory.get_adapter(base_url)
    if isSimple:
        return adapter.get_simple_embeddings(param)
    return adapter.get_embeddings(param)
