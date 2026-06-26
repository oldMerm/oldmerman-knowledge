"""Description
the embedding client getter

Date: 2026-5-25
Created by oldmerman
"""
from typing import Optional
from urllib.parse import urlparse

from agents.embedding.alibaba_embedding import AlibabaEmbedding
from agents.embedding.embedding_common import EmbeddingsGetterParam, embedding_support, EMB_SUPPORT_ENUM, \
    EmbeddingsResponseParam, fuzzy_embedding_support
from agents.embedding.zhi_pu_embedding import ZhiPuEmbedding
from utils import get_logger

logger = get_logger(__name__)

def check_param(param: EmbeddingsGetterParam):
    if not param.api_key or not param.base_url or len(param.doc) == 0:
        logger.error("请求向量生成的参数为空！")
        raise ValueError("请求向量生成的参数为空！")

# 获取厂家的url获取，支持的向量模型
def get_embeddings_supported(param: EmbeddingsGetterParam) -> Optional[EmbeddingsResponseParam]:
    check_param(param)
    base_url = param.base_url
    match embedding_support.get(base_url):
        # case EMB_SUPPORT_ENUM.CHAT_GPT:
        #     return None
        case EMB_SUPPORT_ENUM.BIG_MODEL:
            return ZhiPuEmbedding.embeddings(param)

    # 模糊匹配
    pre_key = None
    for key in fuzzy_embedding_support.keys():
        if base_url in key:
            pre_key = key

    match fuzzy_embedding_support.get(pre_key):
        case EMB_SUPPORT_ENUM.ALIBABA:
            return AlibabaEmbedding.embeddings(param)

    logger.info("暂不支持该类模型")
    raise ValueError("暂不支持该类模型")


if __name__ == "__main__":
    parsed = urlparse("https://api.deepseek.com")
