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
from db.models import RequestTimeRenderParam

logger = get_logger(__name__)


class RequestTimeLogRepository:
    def __init__(self):
        self.table = 'request_time_log'

    @classmethod
    def as_dependency(cls):
        return cls()


    def count(self):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = sql.SQL("""SELECT COUNT(*) FROM {}""").format(
                    sql.Identifier(self.table)
                )
                cur.execute(query)
                row = cur.fetchone()[0]
                return row


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

    def log_count(self) -> RequestTimeRenderParam:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = sql.SQL("""SELECT AVG(total_duration) as request_avg,
                                          MAX(created_at)     as last_time
                                   FROM {};""").format(
                    sql.Identifier(self.table)
                )
                cur.execute(query)
                row = cur.fetchone()
                return RequestTimeRenderParam(
                    request_time_avg=row[0],
                    created_at=row[1]
                )


    def log_user_count(self) -> list[str]:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = sql.SQL("""SELECT thread_id
                                   FROM {}
                                   GROUP BY thread_id;""").format(
                    sql.Identifier(self.table)
                )
                cur.execute(query)
                rows = cur.fetchall()
                if rows:
                    return [row[0] for row in rows]
                else:
                    return []

    def log_page(self, size, offset):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = sql.SQL("""SELECT *
                                   FROM {}
                                   ORDER BY created_at DESC
                                   LIMIT %s OFFSET %s;""").format(
                    sql.Identifier(self.table)
                )
                cur.execute(query, (size, offset))
                rows = cur.fetchall()
                return [
                    RequestTimeLog(
                        id=row[0],
                        thread_id=row[1],
                        total_duration=row[2],
                        prompt=row[3],
                        created_at=row[4],
                        model_id=row[5]
                    )
                    for row in rows
                ]

if __name__ == '__main__':
    rtlr = RequestTimeLogRepository()
    print(rtlr.log_count())
