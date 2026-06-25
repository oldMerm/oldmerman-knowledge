"""Description
the sql to manage table named "vector_connection"

Date: 2026-5-19
Created by oldmerman
"""

import hashlib
import json
from typing import List, Optional, Any

from psycopg2.extras import execute_values

from psycopg2 import sql

from common import BusinessException
from db.connection import get_db_connection
from db.dao.common_repository import check_value_exists
from db.entities.vector_collection import VectorCollection
from db.models import VectorCollectionRenderParam
from utils import get_logger

logger = get_logger(__name__)


def _compute_hash(text):
    """计算文档内容的SHA256哈希"""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


class VectorCollectionRepository:
    def __init__(self):
        self.table = 'vector_collection'
        self.metadata_table = 'vector_metadata'
        self.document_table = 'documents'
        self.usage_table = 'tokens_usage'

    @classmethod
    def as_dependency(cls):
        return cls()

    def filter_exist_hash(self, ids, texts, collection_name, metadatas) -> dict[str, Any]:
        # 1. 批量计算所有文档的 hash
        content_hashes = []
        for text in texts:
            content_hash = _compute_hash(text)  # 假设传入 text
            content_hashes.append(content_hash)

        # 2. 批量查询已存在的 hash
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = sql.SQL("""
                                SELECT content_hash
                                FROM {}
                                WHERE content_hash = ANY (%s)
                                  AND collection_name = %s
                                """).format(
                    sql.Identifier(self.metadata_table)
                )

                cur.execute(query, (content_hashes, collection_name))
                existing_hashes = {row[0] for row in cur.fetchall()}

        # 3. 过滤出需要新增的文档
        new_ids = []
        new_texts = []
        new_metadatas = []
        new_hashes = []

        for chunk_id, text, metadata, content_hash in zip(ids, texts, metadatas, content_hashes):
            if content_hash not in existing_hashes:
                new_ids.append(chunk_id)
                new_texts.append(text)
                new_metadatas.append(metadata)
                new_hashes.append(content_hash)

        # 返回成功上传的元数据
        return {
            "ids": new_ids,
            "documents": new_texts,
            "metadatas": new_metadatas,
            "content_hashes": new_hashes
        }

    def embeddings_record(self, ids, texts, metadatas, content_hashes, doc_id, colletion_name):
        # 批量入库新文档元数据
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # 准备批量插入的数据
                insert_data = []
                for chunk_id, text, metadata, content_hash in zip(ids, texts, metadatas, content_hashes):
                    insert_data.append((
                        chunk_id,
                        content_hash,
                        json.dumps(metadata) if metadata else None,
                        doc_id,
                        colletion_name
                    ))
                # 批量插入
                execute_values(cur, f"""
                    INSERT INTO {self.metadata_table} 
                    (id, content_hash, metadata, doc_id, colletion_name)
                    VALUES %s
                """, insert_data)
                conn.commit()

    def remove_embeddings_record(self, doc_id):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                delete = sql.SQL("DELETE FROM {} WHERE doc_id = %s").format(
                    sql.Identifier(self.metadata_table)
                )
                cur.execute(delete, (doc_id,))

                delete = sql.SQL("DELETE FROM {} WHERE id = %s").format(
                    sql.Identifier(self.document_table)
                )
                cur.execute(delete, (doc_id,))
                logger.info("Successfully rollback DB records")

    def select_by_id(self, collection_id: int) -> Optional[VectorCollection]:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
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

                return VectorCollection(
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
            with conn.cursor() as cur:
                query = sql.SQL("SELECT id, embedding_id, collection_name, collection_alias, "
                                "collection_description, items_number, created_at , dimensions "
                                "FROM {} WHERE embedding_id = %s ORDER BY id").format(
                    sql.Identifier(self.table)
                )
                cur.execute(query, (embedding_id,))
                rows = cur.fetchall()

                return [
                    VectorCollection(
                        id=row[0],
                        embedding_id=row[1],
                        collection_name=row[2],
                        collection_alias=row[3],
                        collection_description=row[4],
                        items_number=row[5],
                        created_at=row[6],
                        dimensions=row[7]
                    )
                    for row in rows
                ]

    def select_name_list(self) -> List[VectorCollectionRenderParam]:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = sql.SQL("""
                                SELECT vc.id,
                                       vc.embedding_id,
                                       m.model_name,
                                       vc.collection_name,
                                       vc.collection_alias,
                                       vc.collection_description,
                                       vc.items_number,
                                       vc.created_at,
                                       vc.dimensions
                                FROM {} vc
                                         LEFT JOIN models m
                                ON vc.embedding_id = m.id
                                ORDER BY vc.id;
                                """).format(
                    sql.Identifier(self.table)
                )
                cur.execute(query)
                rows = cur.fetchall()

                return [
                    VectorCollectionRenderParam(
                        id=row[0],
                        embedding_id=row[1],
                        embedding_name=row[2],
                        collection_name=row[3],
                        collection_alias=row[4],
                        collection_description=row[5],
                        items_number=row[6],
                        created_at=row[7],
                        dimensions=row[8]
                    )
                    for row in rows
                ]

    def insert_collection(self,
                          embedding_id: int = None,
                          collection_name: str = None,
                          collection_alias: str = None,
                          collection_description: str = None,
                          items_number: int = 0,
                          dimensions: int = 0) -> int:
        if check_value_exists(self.table, "collection_name", collection_name) is True:
            logger.warning(f"collection_name: {collection_name} is exist")
            raise BusinessException(f"collection_name: {collection_name} is exist")

        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = sql.SQL("INSERT INTO {} (embedding_id, collection_name, collection_alias, "
                                "collection_description, items_number, dimensions) "
                                "VALUES (%s, %s, %s, %s, %s, %s) "
                                "RETURNING id").format(
                    sql.Identifier(self.table)
                )
                cur.execute(query, (embedding_id, collection_name, collection_alias,
                                    collection_description, items_number, dimensions))
                row = cur.fetchone()

                collection_id = row[0]
                logger.info(f"Collection:{collection_id} named {collection_name} successfully added")

        return collection_id

    def insert_document(self, user_id, filename, file_size, collection_name):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = sql.SQL("""INSERT INTO {} (user_id, filename, filesize, collection_name)
                                   VALUES (%s, %s, %s, %s) RETURNING id """).format(
                    sql.Identifier(self.document_table)
                )
                cur.execute(query, (user_id, filename, file_size, collection_name))
                doc_id = cur.fetchone()[0]
                return doc_id

    def update_collection(self,
                          collection_name: str,
                          collection_alias: str = None,
                          collection_description: str = None,
                          number_update: int = 0) -> bool:
        if check_value_exists(self.table, "collection_name", collection_name) is False:
            logger.error(f"Collection with {collection_name} does not exist")
            raise BusinessException(f"Collection with {collection_name} does not exist")

        with get_db_connection() as conn:
            with conn.cursor() as cur:
                updates = []
                values = []

                if collection_alias is not None:
                    updates.append("collection_alias = %s")
                    values.append(collection_alias)

                if collection_description is not None:
                    updates.append("collection_description = %s")
                    values.append(collection_description)

                abs_update = abs(number_update)
                if number_update > 0:
                    updates.append("items_number = items_number + %s")
                else:
                    updates.append("items_number = items_number - %s")
                values.append(abs_update)

                if not updates:
                    logger.warning(f"No fields to update for collection {collection_name}")
                    return False

                values.append(collection_name)
                query = sql.SQL("UPDATE {} SET {} WHERE collection_name = %s").format(
                    sql.Identifier(self.table),
                    sql.SQL(", ").join(sql.SQL(field) for field in updates)
                )
                cur.execute(query, values)

                logger.info(f"Collection:{collection_name} successfully updated")
                return True

    def remove_collection(self, collection_id: int) -> str:
        if check_value_exists(self.table, "id", collection_id) is False:
            logger.error(f"Collection with id {collection_id} does not exist")
            raise BusinessException(f"Collection with id {collection_id} does not exist")

        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = sql.SQL("DELETE FROM {} WHERE id = %s RETURNING collection_name").format(
                    sql.Identifier(self.table)
                )
                cur.execute(query, (collection_id,))
                collection_name = cur.fetchone()[0]
                logger.info(f"Collection:{collection_name} successfully deleted")
                return collection_name

    def remove_by_embedding(self, embedding_id: int):
        if check_value_exists(self.table, "embedding_id", embedding_id) is False:
            logger.warning(f"No collections found for embedding_id {embedding_id}")
            return

        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = sql.SQL("DELETE FROM {} WHERE embedding_id = %s").format(
                    sql.Identifier(self.table)
                )
                cur.execute(query, (embedding_id,))
                logger.info(f"Collections for embedding_id:{embedding_id} successfully deleted")

    def simple_select_name_list(self):
        with (get_db_connection() as conn):
            with conn.cursor() as cur:
                query = sql.SQL("SELECT collection_name FROM {}").format(
                    sql.Identifier(self.table)
                )
                cur.execute(query)
                rows = cur.fetchall()
                return [
                    row[0]
                    for row in rows
                ]


if __name__ == '__main__':
    vr = VectorCollectionRepository()
    res = vr.simple_select_name_list()
    print(res)
