"""Description
The SQL about table named 'tokens_usage'

Date: 2026-6-3
Created by oldmerman
"""
from psycopg import sql

from db.connection import get_db_connection
from db.models import DateWithSumParam, TokensUsageCountParam
from utils import get_logger

logger = get_logger(__name__)


class TokensUsageRepository:
    def __init__(self):
        self.table = 'tokens_usage'

    @classmethod
    def as_dependency(cls):
        return cls()

    def add(self, user_id: str, model_id: int, tokens: dict[str, int]):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = sql.SQL("""INSERT INTO {} (user_id, model_id, prompt_tokens, completion_tokens, total_tokens)
                                   VALUES (%s, %s, %s, %s, %s)""").format(
                    sql.Identifier(self.table)
                )

                cur.execute(query, (user_id, model_id, tokens.get("prompt_tokens", 0),
                                    tokens.get("completion_tokens", 0), tokens.get("total_tokens", 0)))

    def get_month_token_consume(self):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = sql.SQL(
                    """SELECT
                           DATE (created_at), SUM (prompt_tokens) AS prompt_tokens_count, SUM (completion_tokens) AS completion_tokens_count, SUM (total_tokens) AS total_tokens_count
                       FROM tokens_usage
                       WHERE
                           created_at >= DATE_TRUNC('month'
                           , CURRENT_DATE)
                         AND created_at
                           < CURRENT_DATE + INTERVAL '1 day'
                       GROUP BY DATE (created_at)
                       ORDER BY DATE (created_at) DESC;"""
                ).format(
                    sql.Identifier(self.table)
                )
                cur.execute(query)
                rows = cur.fetchall()
                return [
                    TokensUsageCountParam(
                        date=row[0],
                        prompt_tokens_consume=row[1],
                        completion_tokens_consume=row[2],
                        total_tokens_consume=row[3]
                    )
                    for row in rows
                ]


if __name__ == "__main__":
    dao = TokensUsageRepository()
    w_list = dao.get_month_token_consume()
    for item in w_list:
        print(f"time: {item.date}")
        print(f"prompt_tokens: {item.prompt_tokens_consume}")
        print(f"completion_tokens: {item.completion_tokens_consume}")
        print(f"total_tokens: {item.total_tokens_consume}")
