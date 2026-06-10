"""Description
About the common SQL

Date: 2026-4-28
Created by oldmerman
"""

from psycopg2 import sql

from db.connection import get_db_connection



def check_value_exists(table: str, field: str, value):
    """检查字段值是否存在"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            query = sql.SQL("SELECT EXISTS(SELECT 1 FROM {} WHERE {} = %s)").format(
                sql.Identifier(table),
                sql.Identifier(field)
            )
            cur.execute(query, (value,))
            exists = cur.fetchone()[0]
            return exists  # 返回 True 或 False
