from .embedding_provider import get_embeddings_supported
from .zhi_pu_embedding import ZhiPuEmbedding
from .common import EMB_SUPPORT_ENUM, embedding_support, EmbeddingsGetterParam, EmbeddingsResponseParam

# 如何选择切分器？
# 任务场景 | 首选切分器 | 理由
# 处理通用、长篇文章/文档  	RecursiveCharacterTextSplitter	最大限度保持段落、句子完整，语义最连贯 。
# 开发 RAG 应用	        TokenTextSplitter	            直接满足模型 Token 限制，计费和上下文控制最精准 。
# 处理 Markdown 格式文档	MarkdownTextSplitter	        保留标题、代码块等结构，切分结果更符合文档逻辑 。
# 分析 GitHub 仓库代码	PythonCodeTextSplitter 等	    确保函数、类等代码单元完整，避免切坏语法 。
# 处理格式极其规整的数据	CharacterTextSplitter	        逻辑最简单，处理速度快，无额外计算开销 。


__all__ = [
    "get_embeddings_supported",
    "ZhiPuEmbedding",
    "EmbeddingsGetterParam", "embedding_support", "EMB_SUPPORT_ENUM", "EmbeddingsResponseParam"
]
