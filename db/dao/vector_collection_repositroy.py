from typing import List, Optional

from psycopg2 import sql

from db.connection import get_db_connection
from db.dao.common_repository import check_value_exists
from db.entities import vector_collection as vc_entity
from db.entities.vector_collection import VectorCollection
from utils import get_logger

"""Description
the sql to manage table named "vector_connection"

Date: 2026-5-19
Created by oldmerman
"""

logger = get_logger(__name__)

class VectorCollectionRepository:
    def __init__(self):
        self.table = vc_entity.__name__.split('.')[-1]

    @classmethod
    def as_dependency(cls):
        return cls()

    def select_by_id(self, collection_id: int) -> Optional[VectorCollection]:
        with get_db_connection() as conn:
            cur = conn.cursor()
            query = sql.SQL("SELECT id, embedding_id, collection_name, collection_alias, "
                            "collection_description, items_number, created_at "
                            "FROM {} WHERE id = %s").format(
                sql.Identifier(self.table)
            )
            cur.execute(query, (collection_id,))
            row = cur.fetchone()

            if row is None:
                logger.warning(f"collection with id {collection_id} not found")
                return None

            return vc_entity.VectorCollection(
                id=row[0],
                embedding_id=row[1],
                collection_name=row[2],
                collection_alias=row[3],
                collection_description=row[4],
                items_number=row[5],
                created_at=row[6]
            )

    def select_by_embedding(self, embedding_id: int) -> List[VectorCollection]:
        with get_db_connection() as conn:
            cur = conn.cursor()
            query = sql.SQL("SELECT id, embedding_id, collection_name, collection_alias, "
                            "collection_description, items_number, created_at "
                            "FROM {} WHERE embedding_id = %s ORDER BY id").format(
                sql.Identifier(self.table)
            )
            cur.execute(query, (embedding_id,))
            rows = cur.fetchall()

            return [
                vc_entity.VectorCollection(
                    id=row[0],
                    embedding_id=row[1],
                    collection_name=row[2],
                    collection_alias=row[3],
                    collection_description=row[4],
                    items_number=row[5],
                    created_at=row[6]
                )
                for row in rows
            ]

    def select_name_list(self) -> List[VectorCollection]:
        with get_db_connection() as conn:
            cur = conn.cursor()
            query = sql.SQL("SELECT id, embedding_id, collection_name, collection_alias, "
                            "collection_description, items_number, created_at "
                            "FROM {} ORDER BY id").format(
                sql.Identifier(self.table)
            )
            cur.execute(query)
            rows = cur.fetchall()

            return [
                vc_entity.VectorCollection(
                    id=row[0],
                    embedding_id=row[1],
                    collection_name=row[2],
                    collection_alias=row[3],
                    collection_description=row[4],
                    items_number=row[5],
                    created_at=row[6]
                )
                for row in rows
            ]

    def insert_collection(self,
                          embedding_id: int = None,
                          collection_name: str = None,
                          collection_alias: str = None,
                          collection_description: str = None,
                          items_number: int = 0) -> int:
        if check_value_exists(self.table, "collection_name", collection_name) is True:
            logger.warning(f"collection_name: {collection_name} is exist")
            raise ValueError(f"collection_name: {collection_name} is exist")

        with get_db_connection() as conn:
            cur = conn.cursor()
            query = sql.SQL("INSERT INTO {} (embedding_id, collection_name, collection_alias, "
                            "collection_description, items_number) "
                            "VALUES (%s, %s, %s, %s, %s) "
                            "RETURNING id").format(
                sql.Identifier(self.table)
            )
            cur.execute(query, (embedding_id, collection_name, collection_alias,
                                collection_description, items_number))
            row = cur.fetchone()

            collection_id = row[0]
            logger.info(f"Collection:{collection_id} named {collection_name} successfully added")
            return collection_id

    def update_collection(self,
                          collection_id: int,
                          collection_alias: str = None,
                          collection_description: str = None,
                          items_number: int = None) -> bool:
        if check_value_exists(self.table, "id", collection_id) is False:
            logger.error(f"Collection with id {collection_id} does not exist")
            raise ValueError(f"Collection with id {collection_id} does not exist")

        with get_db_connection() as conn:
            cur = conn.cursor()
            updates = []
            values = []

            if collection_alias is not None:
                updates.append("collection_alias = %s")
                values.append(collection_alias)

            if collection_description is not None:
                updates.append("collection_description = %s")
                values.append(collection_description)

            if items_number is not None:
                updates.append("items_number = %s")
                values.append(items_number)

            if not updates:
                logger.warning(f"No fields to update for collection {collection_id}")
                return False

            values.append(collection_id)
            query = sql.SQL("UPDATE {} SET {} WHERE id = %s").format(
                sql.Identifier(self.table),
                sql.SQL(", ").join(sql.Identifier(field) for field in updates)
            )
            cur.execute(query, values)

            logger.info(f"Collection:{collection_id} successfully updated")
            return True

    def remove_collection(self, collection_id: int):
        if check_value_exists(self.table, "id", collection_id) is False:
            logger.error(f"Collection with id {collection_id} does not exist")
            raise ValueError(f"Collection with id {collection_id} does not exist")

        with get_db_connection() as conn:
            cur = conn.cursor()
            query = sql.SQL("DELETE FROM {} WHERE id = %s").format(
                sql.Identifier(self.table)
            )
            cur.execute(query, (collection_id,))
            logger.info(f"Collection:{collection_id} successfully deleted")

    def remove_by_embedding(self, embedding_id: int):
        if check_value_exists(self.table, "embedding_id", embedding_id) is False:
            logger.warning(f"No collections found for embedding_id {embedding_id}")
            return

        with get_db_connection() as conn:
            cur = conn.cursor()
            query = sql.SQL("DELETE FROM {} WHERE embedding_id = %s").format(
                sql.Identifier(self.table)
            )
            cur.execute(query, (embedding_id,))
            logger.info(f"Collections for embedding_id:{embedding_id} successfully deleted")


if __name__ == '__main__':
    vr = VectorCollectionRepository()
    vr.insert_collection(collection_name="oldmerman", collection_alias="merman", collection_description="so cool")