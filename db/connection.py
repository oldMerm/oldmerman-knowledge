import os
from contextlib import contextmanager

import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

from config import get_settings

load_dotenv()

_connection_pool = None

DATABASE_URL = os.getenv("DATABASE_URL", "")

settings = get_settings()


def init_db():
    global _connection_pool

    _connection_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=settings.MAX_DATABASE_POOL_SIZE,
        dsn=DATABASE_URL
    )


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
    """从连接池获取连接，自动管理事务"""
    global _connection_pool
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e  # 重新抛出原始异常，让调用方处理
    finally:
        close_connection(conn)