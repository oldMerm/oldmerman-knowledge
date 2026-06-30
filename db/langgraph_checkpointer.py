"""Description
LangGraph统一checkpoint

Date: 2026-6-30
Created by oldmerman
"""
import os

from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver
import psycopg

from config import get_settings

_langgraph_pool = None
_checkpointer = None
_initialized = False

DATABASE_URL = os.getenv("DATABASE_URL", "")

settings = get_settings()

def init_langgraph_db(lazy: bool = True):
    """初始化 LangGraph 连接池"""
    global _langgraph_pool, _initialized
    if _initialized:
        return

    _langgraph_pool = ConnectionPool(
        DATABASE_URL,
        min_size=1,
        max_size=settings.MAX_LANGGRAPH_CHECKPOINTER_POOL_SIZE,
        open=not lazy,
        kwargs={
            "autocommit": True,
            "row_factory": psycopg.rows.dict_row
        }
    )
    _initialized = True


def ensure_initialized():
    """确保已初始化，未初始化则自动初始化"""
    global _initialized, _langgraph_pool
    if not _initialized:
        init_langgraph_db(lazy=True)

    # 确保连接池已打开
    if _langgraph_pool is not None and not _langgraph_pool.is_open:
        _langgraph_pool.open()


def get_checkpointer():
    """获取 checkpointer"""
    global _checkpointer
    ensure_initialized()

    if _checkpointer is None:
        conn = _langgraph_pool.getconn()
        _checkpointer = PostgresSaver(
            conn,
            None,
            {"schema": "langchain"}
        )
        _checkpointer.setup()
    return _checkpointer