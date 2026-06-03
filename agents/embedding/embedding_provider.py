"""Description
the embedding client getter

Date: 2026-5-25
Created by oldmerman
"""
from typing import Optional
from urllib.parse import urlparse

from agents.embedding.common import EmbeddingsGetterParam, embedding_support, EMB_SUPPORT_ENUM, EmbeddingsResponseParam
from agents.embedding.zhi_pu_embedding import ZhiPuEmbedding
from utils import get_logger

logger = get_logger(__name__)

# 获取厂家的url获取，支持的向量模型
def get_embeddings_supported(param: EmbeddingsGetterParam) -> Optional[EmbeddingsResponseParam]:
    match embedding_support.get(param.base_url):
        case EMB_SUPPORT_ENUM.CHAT_GPT:
            return None
        case EMB_SUPPORT_ENUM.BIG_MODEL:
            return ZhiPuEmbedding.embeddings(param)
        case _:
            logger.info("暂不支持该类模型")
            raise ValueError("暂不支持该类模型")


if __name__ == "__main__":
    parsed = urlparse("https://api.deepseek.com")
