"""Description
向量模型的各项参数，需标注好参数的来源，后续会将相关事宜同步到前端
BigModel(智谱清言): https://docs.bigmodel.cn/cn/guide/start/model-overview#%E5%90%91%E9%87%8F%E6%A8%A1%E5%9E%8B
阿里巴巴: https://help.aliyun.com/zh/model-studio/embedding

Created by oldmerman
"""
from .embedding_provider import get_embeddings_supported, EmbeddingFactory
from .zhi_pu_embedding import ZhiPuEmbedding
from .embedding_common import EmbeddingsGetterParam, EmbeddingsResponseParam, EmbeddingUtils

__all__ = [
    "get_embeddings_supported", "EmbeddingFactory",
    "ZhiPuEmbedding",
    "EmbeddingsGetterParam", "EmbeddingsResponseParam", "EmbeddingUtils"
]
