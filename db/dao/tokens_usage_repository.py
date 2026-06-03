from psycopg2 import sql

from db.connection import get_db_connection
from utils import get_logger

"""Description
The SQL about table named 'tokens_usage'

Date: 2026-6-3
Created by oldmerman
"""

logger = get_logger(__name__)


class TokensUsageRepository:
    def __init__(self):
        self.table = 'tokens_usage'

    @classmethod
    def as_dependency(cls):
        return cls()

    def add(self, user_id: str, model_id: int, tokens: dict[str, int]):
        with get_db_connection() as conn:
            cur = conn.cursor()
            query = sql.SQL("INSERT INTO {} (user_id, model_id, prompt_tokens, completion_tokens, total_tokens)"
                            "VALUES (%s, %s, %s, %s, %s)").format(
                sql.Identifier(self.table)
            )

            cur.execute(query, (user_id, model_id, tokens.get("prompt_tokens"),
                                tokens.get("completion_tokens"), tokens.get("total_tokens")))