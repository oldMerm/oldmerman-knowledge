import os
from contextlib import contextmanager

from psycopg_pool import ConnectionPool
from dotenv import load_dotenv

from config import get_settings

load_dotenv()

_connection_pool = None

DATABASE_URL = os.getenv("DATABASE_URL", "")

settings = get_settings()


def init_db():
    global _connection_pool

    _connection_pool = ConnectionPool(
        conninfo=DATABASE_URL,
        min_size=1,
        max_size=settings.MAX_DATABASE_POOL_SIZE,
        open=True,
    )


def close_db():
    if _connection_pool:
        _connection_pool.close()


def get_connection():
    global _connection_pool
    if _connection_pool is None:
        init_db()
    return _connection_pool.getconn()


def close_connection(conn):
    global _connection_pool
    if _connection_pool and conn:
        _connection_pool.putconn(conn)


@contextmanager
def get_db_connection():
    """从连接池获取连接，自动管理事务（成功自动commit，异常自动rollback）"""
    global _connection_pool
    if _connection_pool is None:
        init_db()
    with _connection_pool.connection() as conn:
        yield conn