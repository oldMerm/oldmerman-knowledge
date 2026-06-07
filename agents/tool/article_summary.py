from langchain.agents import AgentState
from langchain.agents.middleware import after_model
from langgraph.prebuilt import ToolRuntime
from pydantic import BaseModel

from db.connection import get_db_connection
from db.dao.tokens_usage_repository import TokensUsageRepository
from utils import get_logger

logger = get_logger(__name__)

PROMPT = """生成**文章摘要**：
        - 客观陈述研究/内容
        - 第三人称，200字以内
        """


class ArticleSummaryContext(BaseModel):
    user_id: str = "02813b57-71c8-4d4a-af16-44132e741fdf"
    article_id: str
    article_name: str
    model_id: int

@after_model
def refresh_cache(
        state: AgentState,
        runtime: ToolRuntime[ArticleSummaryContext]
) -> None:
    """将文章摘要缓存到数据库"""
    article_id = runtime.context.article_id
    article_name = runtime.context.article_name

    # 获取最后一条消息作为摘要
    last_message = state["messages"][-1]
    article_summary = last_message.content if hasattr(last_message, 'content') else str(last_message)

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = """
                        INSERT INTO cache.summary_cache
                            (article_id, article_name, article_summary)
                        VALUES (%s, %s, %s)
                        """
                cur.execute(
                    query,
                    (article_id, article_name, article_summary)
                )
                logger.info(f"cache article {article_id}: {article_name}")

    except Exception as e:
        logger.error(f"cache {article_id} fail: {str(e)}")


@after_model
def save_token_usage_to_db(
        state: AgentState,
        runtime: ToolRuntime[ArticleSummaryContext]
) -> None:
    """保存token使用统计到数据库"""
    last_message = state['messages'][-1]
    model_id = runtime.context.model_id
    user_id = runtime.context.user_id
    if hasattr(last_message, 'usage_metadata'):
        usage = last_message.usage_metadata
        tokens = {
            'prompt_tokens': usage.get('input_tokens', 0),
            'completion_tokens': usage.get('output_tokens', 0),
            'total_tokens': usage.get('total_tokens', 0)
        }
        dto = TokensUsageRepository.as_dependency()
        dto.add(user_id=user_id, model_id=model_id, tokens=tokens)