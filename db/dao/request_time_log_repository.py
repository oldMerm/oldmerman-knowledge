"""Description
The SQL about table named 'request_time_log'

Date: 2026-7-11
Created by oldmerman
"""
from typing import Optional

from psycopg import sql

from db.connection import get_db_connection
from db.entities import RequestTimeLog
from common.utils import get_logger

logger = get_logger(__name__)


class RequestTimeLogRepository:
    def __init__(self):
        self.table = 'request_time_log'

    @classmethod
    def as_dependency(cls):
        return cls()

    def log(self, param: RequestTimeLog) -> Optional[str]:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = sql.SQL("""INSERT INTO {} (thread_id, total_duration, prompt, model_id)
                                    VALUES (%s, %s, %s, %s)
                                    RETURNING id
                                """).format(
                    sql.Identifier(self.table)
                )
                cur.execute(query, (param.thread_id, param.total_duration, param.prompt, param.model_id))
                row = cur.fetchone()
                return row[0] if row else None

if __name__ == '__main__':
    rtlr = RequestTimeLogRepository()
    param = RequestTimeLog(thread_id="::1-aqhuj8-2026070221", total_duration=3.432, prompt="鱼人博客经历了多少个版本的迭代？", model_id=1003)
    rtlr.log(param)
