"""Description
The SQL about table named 'models_group'

Date: 2026-4-28
Created by oldmerman
"""

from typing import List, Optional

from psycopg import sql
from db.connection import get_db_connection
from db.dao.models_repository import ModelsRepository
from db.entities import ModelsGroup
from db.models import ModelsGroupRender
from utils import get_logger, AESEncryptUtil



logger = get_logger(__name__)


class ModelsGroupRepository:
    def __init__(self):
        self.table = 'models_group'

    @classmethod
    def as_dependency(cls):
        return cls()


    def get_render_group(self) -> List[ModelsGroupRender]:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = sql.SQL("SELECT group_uuid, group_name, group_attr FROM {} ORDER BY group_name ASC").format(
                    sql.Identifier(self.table)
                )
                cur.execute(query)
                rows = cur.fetchall()
                return [
                    ModelsGroupRender(
                        group_uuid=str(row[0]),
                        group_name=row[1],
                        group_attr=row[2]
                    )
                    for row in rows
                ]


    def get_group(self, group_uuid: Optional[str]) -> ModelsGroup:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                if group_uuid is None:
                    query = sql.SQL("SELECT * FROM {} ORDER BY group_name ASC").format(
                        sql.Identifier(self.table)
                    )
                    cur.execute(query)
                else:
                    query = sql.SQL("SELECT * FROM {} WHERE group_uuid = %s").format(
                        sql.Identifier(self.table)
                    )
                    cur.execute(query, (group_uuid,))
                row = cur.fetchone()
                return ModelsGroup(
                    id=row[0],
                    group_uuid=str(row[1]),
                    group_name=row[2],
                    group_attr=row[3],
                    created_at=row[4],
                    api_key=row[5],
                    base_url=row[6]
                )


    def create_group(self, group_name: str, group_attr: str = None, api_key: str = None, base_url: str = None) -> str:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = sql.SQL("INSERT INTO {} (group_name, group_attr, api_key, base_url) VALUES (%s, %s, %s, %s) RETURNING group_uuid").format(
                    sql.Identifier(self.table)
                )
                cur.execute(query, (group_name, group_attr, AESEncryptUtil.encrypt(api_key), base_url))
                row = cur.fetchone()

                if row is None:
                    logger.warning(f"{group_name} create failed")
                    raise ValueError(f"{group_name} create failed")

                group_uuid = str(row[0])
                logger.info(f"Model:{group_uuid} named {group_name} successfully added")

                return group_uuid


    def remove_group(self, group_uuid: str) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cur:

                query1 = ModelsRepository.as_dependency().remove_model_by_group()
                cur.execute(query1, (group_uuid,))

                query2 = sql.SQL("DELETE FROM {} WHERE group_uuid = %s RETURNING id, group_name").format(
                    sql.Identifier(self.table)
                )
                cur.execute(query2, (group_uuid,))

                row = cur.fetchone()

                if row is None:
                    logger.warning(f"Group with uuid {group_uuid} not found")
                    raise ValueError(f"Group with uuid {group_uuid} does not exist")

                group_id = row[0]
                group_name = row[1]
                logger.info(f"Model:{group_id} named {group_name} successfully deleted")

                return group_id


if __name__ == '__main__':
    mr = ModelsGroupRepository()
    res = mr.create_group("DeepSeek")
    print(res)
