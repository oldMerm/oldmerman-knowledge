from typing import List, Optional

from psycopg2 import sql

from db.connection import get_db_connection
from db.dao.common_repository import check_value_exists
from db.entities import model_type
from db.entities.model_type import ModelType
from utils import get_logger

"""Description
The SQL about table named 'model_type'

Date: 2026-5-16
Created by oldmerman
"""

logger = get_logger(__name__)


class ModelTypeRepository:
    def __init__(self):
        self.table = model_type.__name__.split('.')[-1]

    @classmethod
    def as_dependency(cls):
        return cls()

    def insert(self, model_type_name: str) -> int:
        if check_value_exists(self.table, "model_type_name", model_type_name):
            logger.error(f"ModelType:{model_type_name} already exists")
            raise ValueError(f"ModelType:{model_type_name} already exists")

        with get_db_connection() as conn:
            cur = conn.cursor()
            query = sql.SQL("INSERT INTO {} (model_type_name) "
                            "VALUES (%s) "
                            "RETURNING id").format(
                sql.Identifier(self.table)
            )
            cur.execute(query, (model_type_name,))
            row = cur.fetchone()
            logger.info(f"ModelType:{model_type_name} added with id {row[0]}")
            return row[0]

    def select_by_id(self, type_id: int) -> Optional[ModelType]:
        with get_db_connection() as conn:
            cur = conn.cursor()
            query = sql.SQL("SELECT id, model_type_name, created_at FROM {} WHERE id = %s").format(
                sql.Identifier(self.table)
            )
            cur.execute(query, (type_id,))
            row = cur.fetchone()

            if row is None:
                logger.warning(f"ModelType with id {type_id} not found")
                return None

            return ModelType(
                id=row[0],
                model_type_name=row[1],
                created_at=row[2]
            )

    def select_all(self) -> List[ModelType]:
        with get_db_connection() as conn:
            cur = conn.cursor()
            query = sql.SQL("SELECT id, model_type_name, created_at FROM {} ORDER BY id").format(
                sql.Identifier(self.table)
            )
            cur.execute(query)
            rows = cur.fetchall()

            return [
                ModelType(
                    id=row[0],
                    model_type_name=row[1],
                    created_at=row[2]
                )
                for row in rows
            ]

    def delete_by_id(self, type_id: int) -> bool:
        with get_db_connection() as conn:
            cur = conn.cursor()
            query = sql.SQL("DELETE FROM {} WHERE id = %s").format(
                sql.Identifier(self.table)
            )
            cur.execute(query, (type_id,))
            if cur.rowcount > 0:
                logger.info(f"ModelType with id {type_id} deleted")
                return True
            logger.warning(f"ModelType with id {type_id} not found for deletion")
            return False
