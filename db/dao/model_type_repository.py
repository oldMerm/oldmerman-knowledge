from typing import List, Optional

from psycopg2 import sql

from db.connection import get_db_connection
from db.dao.common_repository import check_value_exists
from db.entities.model_type import ModelType
from db.models import ModelsWithTypeParam, ModelRenderParam1
from utils import get_logger

"""Description
The SQL about table named 'model_type'

Date: 2026-5-16
Created by oldmerman
"""

logger = get_logger(__name__)


class ModelTypeRepository:

    def __init__(self):
        self.table = 'model_type'
        self.link_table = 'model_type_link'

    @classmethod
    def as_dependency(cls):
        return cls()

    def insert(self, model_type_name: str) -> int:
        if check_value_exists(self.table, "model_type_name", model_type_name):
            logger.error(f"ModelType:{model_type_name} already exists")
            raise ValueError(f"ModelType:{model_type_name} already exists")

        with get_db_connection() as conn:
            with conn.cursor() as cur:
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
            with conn.cursor() as cur:
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
            with conn.cursor() as cur:
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

    def select_type_models(self, type_name: str):
        with get_db_connection() as conn:
            with conn.cursor() as cur:

                query = sql.SQL("SELECT id FROM model_type WHERE model_type_name = %s")
                cur.execute(query, (type_name,))
                row = cur.fetchone()

                if row[0] is None:
                    return None
                type_id = row[0]

                query = sql.SQL("SELECT m.id, m.model_name FROM models m "
                                "INNER JOIN {} mtl ON m.id = mtl.model_id "
                                "WHERE mtl.type_id = %s ").format(
                    sql.Identifier(self.link_table)
                )
                cur.execute(query, (type_id,))
                rows = cur.fetchall()

                return ModelsWithTypeParam(
                    type_id=type_id,
                    type_name=type_name,
                    models=[
                        ModelRenderParam1(
                            model_id=row[0],
                            model_name=row[1]
                        )
                        for row in rows
                    ]
                )


    def delete_by_id(self, type_id: int) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = sql.SQL("DELETE FROM {} WHERE id = %s").format(
                    sql.Identifier(self.table)
                )
                cur.execute(query, (type_id,))
                if cur.rowcount > 0:
                    logger.info(f"ModelType with id {type_id} deleted")
                    return True
                logger.warning(f"ModelType with id {type_id} not found for deletion")
                return False

if __name__ == "__main__":
    dao = ModelTypeRepository()
    print(dao.select_type_models('向量模型'))