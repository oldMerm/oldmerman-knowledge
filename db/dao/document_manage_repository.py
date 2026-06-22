"""Description
文档表相关mapper

Date: 2026-6-9
Created by oldmerman
"""
from psycopg2 import sql

from db.connection import get_db_connection
from db.dao import VectorCollectionRepository
from db.models import DocumentPageParam
from utils import get_logger

logger = get_logger(__name__)


class DocumentsRepository:
    def __init__(self):
        self.table = 'documents'
        self.detail_table = 'vector_metadata'

    @classmethod
    def as_dependency(cls):
        return cls()

    def get_totals(self):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = sql.SQL("SELECT COUNT(*) FROM {}").format(
                    sql.Identifier(self.table)
                )
                cur.execute(query)
                row = cur.fetchone()
                if row:
                    return row[0]
                else:
                    return 0

    def page(self, start, size, collection_name):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                base_query = sql.SQL("""SELECT d.id,
                                               d.filename,
                                               d.filesize,
                                               d.collection_name,
                                               d.created_at,
                                               COUNT(vm.id)
                                        FROM {} d
                                            LEFT JOIN {} vm
                                        ON d.id = vm.doc_id""").format(
                    sql.Identifier(self.table), sql.Identifier(self.detail_table)
                )

                # 动态添加 WHERE 条件
                where_clause = sql.SQL("")
                params = []

                if collection_name:
                    where_clause = sql.SQL("WHERE d.collection_name = %s")
                    params.append(collection_name)

                query = sql.SQL("{} {} GROUP BY d.id LIMIT %s OFFSET %s;").format(
                    base_query,
                    where_clause
                )

                params.extend([size, start])

                cur.execute(query, tuple(params))
                rows = cur.fetchall()
                return [
                    DocumentPageParam(
                        id=row[0],
                        filename=row[1],
                        filesize=row[2],
                        collection_name=row[3],
                        created_at=row[4],
                        doc_num=row[5]
                    )
                    for row in rows
                ]

    def delete_document(self, doc_id):
        from db.vector_connection import ChromaVectorHelper
        with get_db_connection() as conn:
            try:
                with conn.cursor() as cur:
                    delete = sql.SQL("DELETE FROM {} WHERE id = %s RETURNING collection_name").format(
                        sql.SQL(self.table)
                    )
                    cur.execute(delete, (doc_id,))
                    collection_name = cur.fetchone()[0]
                    delete_detail = sql.SQL("DELETE FROM {} WHERE doc_id = %s RETURNING id").format(
                        sql.SQL(self.detail_table)
                    )
                    cur.execute(delete_detail, (doc_id,))
                    rows = cur.fetchall()
                    delete_detail_ids = [row[0] for row in rows]
                    VectorCollectionRepository().update_collection(collection_name=collection_name,
                                                                   number_update=-len(delete_detail_ids))
                    ChromaVectorHelper(collection_name).delete(delete_detail_ids)

            except Exception as e:
                logger.error(f"delete document failed, {e}")
                raise e



if __name__ == "__main__":
    res = DocumentsRepository().page(0, 5, collection_name="text_collection")
    print(res)