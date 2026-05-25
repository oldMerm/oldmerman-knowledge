import hashlib
import json
from typing import List, Optional

from psycopg2.extras import execute_values

from psycopg2 import sql

from agents.embedding import get_embeddings_supported
from db import get_vector_database
from db.connection import get_db_connection
from db.dao import ModelsRepository
from db.dao.common_repository import check_value_exists
from db.entities.vector_collection import VectorCollection
from utils import get_logger

"""Description
the sql to manage table named "vector_connection"

Date: 2026-5-19
Created by oldmerman
"""

logger = get_logger(__name__)


def _compute_hash(text):
    """计算文档内容的SHA256哈希"""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


class VectorCollectionRepository:
    def __init__(self):
        self.table = 'vector_collection'
        self.metadata_table = 'vector_metadata'
        self.vector_client = get_vector_database()

    @classmethod
    def as_dependency(cls):
        return cls()

    def _add_batch_new(self, collection_name, ids, texts, metadatas, content_hashes):
        """
        批量插入新文档到数据库
        """
        if not ids:
            return

        collection = self.vector_client.get_collection(collection_name)

        embedding_id = collection.metadata.get("embedding_id")
        model_param = ModelsRepository().select_model(embedding_id)
        embeddings = get_embeddings_supported(model_param.api_key, model_param.base_url, texts)

        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
        )

        with get_db_connection() as conn:
            cur = conn.cursor()
            # 准备批量插入的数据
            insert_data = []
            for doc_id, text, metadata, content_hash in zip(ids, texts, metadatas, content_hashes):
                insert_data.append((
                    doc_id,
                    collection_name,
                    text,
                    json.dumps(metadata) if metadata else None,
                    content_hash
                ))
            # 批量插入
            execute_values(cur, f"""
                INSERT INTO {self.metadata_table} 
                (id, collection_name, document_text, metadata, content_hash)
                VALUES %s
            """, insert_data)
            conn.commit()

    async def upload(self, collection_name, ids, texts, metadatas) -> List[str]:
        if not ids:
            return []

        # 1. 批量计算所有文档的 hash
        content_hashes = []
        for text in texts:
            content_hash = _compute_hash(text)  # 假设传入 text
            content_hashes.append(content_hash)

        # 2. 批量查询已存在的 hash
        with get_db_connection() as conn:
            cur = conn.cursor()
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

        for doc_id, text, metadata, content_hash in zip(ids, texts, metadatas, content_hashes):
            if content_hash not in existing_hashes:
                new_ids.append(doc_id)
                new_texts.append(text)
                new_metadatas.append(metadata)
                new_hashes.append(content_hash)

        # 4. 批量插入新文档
        if new_ids:
            self._add_batch_new(collection_name, new_ids, new_texts, new_metadatas, new_hashes)

        # 返回成功上传的ID
        return new_ids

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
            cur = conn.cursor()
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

    def select_name_list(self) -> List[VectorCollection]:
        with get_db_connection() as conn:
            cur = conn.cursor()
            query = sql.SQL("SELECT id, embedding_id, collection_name, collection_alias, "
                            "collection_description, items_number, created_at ,dimensions "
                            "FROM {} ORDER BY id").format(
                sql.Identifier(self.table)
            )
            cur.execute(query)
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

    def insert_collection(self,
                          embedding_id: int = None,
                          collection_name: str = None,
                          collection_alias: str = None,
                          collection_description: str = None,
                          items_number: int = 0,
                          dimensions: int = 0) -> int:
        if check_value_exists(self.table, "collection_name", collection_name) is True:
            logger.warning(f"collection_name: {collection_name} is exist")
            raise ValueError(f"collection_name: {collection_name} is exist")

        with get_db_connection() as conn:
            cur = conn.cursor()
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

        try:
            v_metadata = {
                "embedding_id": embedding_id,
                "collection_description": collection_description,
                "dimensions": str(dimensions)
            }
            if collection_alias is not None:
                v_metadata["collection_alias"] = collection_alias

            self.vector_client.create_collection(
                name=collection_name,
                metadata=v_metadata,
            )
        except ValueError:
            self.remove_collection(collection_id)
            raise ValueError(
                f"collection added fail, because collection_name:{collection_name} is exist in vector database")

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

    def remove_collection(self, collection_id: int) -> str:
        if check_value_exists(self.table, "id", collection_id) is False:
            logger.error(f"Collection with id {collection_id} does not exist")
            raise ValueError(f"Collection with id {collection_id} does not exist")

        with get_db_connection() as conn:
            cur = conn.cursor()
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
            cur = conn.cursor()
            query = sql.SQL("DELETE FROM {} WHERE embedding_id = %s").format(
                sql.Identifier(self.table)
            )
            cur.execute(query, (embedding_id,))
            logger.info(f"Collections for embedding_id:{embedding_id} successfully deleted")


if __name__ == '__main__':
    vr = VectorCollectionRepository()
    vr.insert_collection(collection_name="oldmerman", collection_alias="merman", collection_description="so cool")
