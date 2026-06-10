"""Description
文档表相关mapper

Date: 2026-6-9
Created by oldmerman
"""
from psycopg2 import sql

from db import get_vector_database
from db.connection import get_db_connection
from db.models import DocumentPageParam
from utils import get_logger

logger = get_logger(__name__)


class DocumentsRepository:
    def __init__(self):
        self.table = 'documents'
        self.detail_table = 'vector_metadata'
        self.vector_client = get_vector_database()

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

    def page(self, start, size):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = sql.SQL("""SELECT d.id,
                                          d.filename,
                                          d.filesize,
                                          d.collection_name,
                                          d.created_at,
                                          COUNT(vm.id)
                                   FROM {} d
                                            LEFT JOIN {} vm
                                   ON d.id = vm.doc_id
                                   GROUP BY d.id LIMIT %s
                                   OFFSET %s;""").format(
                    sql.Identifier(self.table), sql.Identifier(self.detail_table)
                )
                cur.execute(query, (size, start))
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
                    self.vector_client.get_collection(collection_name).delete(ids=delete_detail_ids)

            except Exception as e:
                logger.error(f"delete document failed, {e}")
                raise e



if __name__ == "__main__":
    DocumentsRepository().delete_document('d191749f-e9ed-4fcf-8a77-98a4d1a36f1c')
