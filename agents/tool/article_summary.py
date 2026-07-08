from langchain.agents import AgentState
from langchain.agents.middleware import after_model
from langgraph.prebuilt import ToolRuntime

from agents.types import ArticleContext
from db.connection import get_db_connection
from common.utils import get_logger

logger = get_logger(__name__)

@after_model
def refresh_cache(
        state: AgentState,
        runtime: ToolRuntime[ArticleContext]
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
