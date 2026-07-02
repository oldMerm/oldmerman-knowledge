import os

from langgraph.checkpoint.postgres import PostgresSaver
from psycopg.rows import dict_row
from dotenv import load_dotenv
from psycopg_pool import ConnectionPool

from config import get_settings

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")
settings = get_settings()

# 全局连接池（应用启动时创建一次）
_pool = None
_checkpointer = None


def init_checkpointer():
    """初始化全局连接池和 checkpointer（应用启动时调用）"""
    global _pool, _checkpointer

    if _pool is not None:
        return _checkpointer

    import psycopg
    conn = psycopg.connect(DATABASE_URL + "?sslmode=disable")
    conn.execute("CREATE SCHEMA IF NOT EXISTS langchain")
    conn.close()

    _pool = ConnectionPool(
        conninfo=DATABASE_URL + "?sslmode=disable",
        min_size=1,
        max_size=settings.MAX_LANGGRAPH_CHECKPOINTER_POOL_SIZE,
        kwargs={
            "autocommit": True,
            "row_factory": dict_row,
            "options": "-c search_path=langchain"
        }
    )

    # 创建 checkpointer
    _checkpointer = PostgresSaver(conn=_pool)
    _checkpointer.setup()

    return _checkpointer


def get_checkpointer():
    if _checkpointer is None:
        init_checkpointer()
    return _checkpointer


def close_checkpointer():
    global _pool, _checkpointer
    if _pool:
        _pool.close()
        _pool = None
        _checkpointer = None