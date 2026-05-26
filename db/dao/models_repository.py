from typing import List

from psycopg2 import sql

from db.connection import get_db_connection
from db.dao.common_repository import check_value_exists
from db.models import ModelRegisterParam
from db.models.models_param import ModelRenderParam
from utils import get_logger, AESEncryptUtil

"""Description
The SQL about table named 'models'

Date: 2026-4-28
Created by oldmerman
"""

logger = get_logger(__name__)


# TODO: 注册时使用默认值则有问题


class ModelsRepository:
    def __init__(self):
        self.table = 'models'

    @classmethod
    def as_dependency(cls):
        return cls()

    # 获取参数用以注册大模型
    def select_model(self, model_id: int) -> ModelRegisterParam:
        with get_db_connection() as conn:
            cur = conn.cursor()
            query = sql.SQL("SELECT id, model_name, api_key, base_url FROM {} WHERE id = %s").format(
                sql.Identifier(self.table)
            )
            cur.execute(query, (model_id,))
            row = cur.fetchone()

            if row is None:
                logger.warning(f"model with model_id {model_id} not found")
                raise ValueError(f"model with model_id {model_id} does not exist")

            return ModelRegisterParam(
                id=row[0],
                model_name=row[1],
                api_key=AESEncryptUtil.decrypt(row[2]),
                base_url=row[3],
            )

    # 模型+种类集合，用于前端渲染
    def select_name_list(self, group_uuid: str) -> List[ModelRenderParam]:
        with get_db_connection() as conn:
            cur = conn.cursor()
            query = sql.SQL("SELECT m.id as model_id,"
                            "m.model_name as model_name,"
                            "mt.id as type_id,"
                            "mt.model_type_name as type_name "
                            "FROM models m "
                            "LEFT JOIN model_type_link mtl ON m.id = mtl.model_id "
                            "LEFT JOIN model_type mt ON mtl.type_id = mt.id "
                            "WHERE m.group_uuid = %s "
                            "ORDER BY m.id;")
            cur.execute(query, (group_uuid,))
            rows = cur.fetchall()

            return [
                ModelRenderParam(
                    model_id=row[0],
                    model_name=row[1],
                    type_id=row[2],
                    type_name=row[3]
                )
                for row in rows
            ]

    def insert_model(self,
                     model_name: str,
                     group_uuid: str,
                     user_uuid: str,
                     api_key: str = None,
                     base_url: str = None,
                     type_id: int = None,
                     ) -> int:
        if check_value_exists("models_group", "group_uuid", group_uuid) is False:
            logger.error(f"Group with uuid {group_uuid} does not exist")
            raise ValueError(f"Group with uuid {group_uuid} does not exist")
        if check_value_exists(self.table, "model_name", model_name):
            logger.error(f"Model:{model_name} does exist")
            raise ValueError(f"Model:{model_name} does exist")

        with get_db_connection() as conn:
            cur = conn.cursor()

            if api_key is not None:
                crypt_api_key = AESEncryptUtil.encrypt(api_key)
            else:
                crypt_api_key = None

            query = sql.SQL("INSERT INTO {} (model_name, group_uuid, user_uuid, api_key, base_url) "
                            "VALUES (%s, %s, %s, %s, %s) "
                            "RETURNING id").format(
                sql.Identifier(self.table)
            )
            cur.execute(query, (model_name, group_uuid, user_uuid, crypt_api_key, base_url))
            row = cur.fetchone()

            model_id = row[0]

            query = sql.SQL("INSERT INTO model_type_link (model_id, type_id)"
                            "VALUES (%s, %s)")
            cur.execute(query, (model_id, type_id))

            logger.info(f"Model:{model_id} named {model_name} successfully added")
            return model_id

    # 删除模型
    def remove_model(self, model_id: int):
        if check_value_exists(self.table, "id", model_id) is False:
            logger.error(f"Model with id {model_id} does not exist")
            raise ValueError(f"Model with id {model_id} does not exist")
        with get_db_connection() as conn:
            cur = conn.cursor()
            query = sql.SQL("DELETE FROM {} WHERE id = %s").format(
                sql.Identifier(self.table)
            )
            cur.execute(query, (model_id,))
            query = sql.SQL("DELETE FROM model_type_link WHERE model_id = %s")
            cur.execute(query, (model_id,))

    # return SQL
    def remove_model_by_group(self):
        return sql.SQL("DELETE FROM {} WHERE group_uuid = %s").format(
            sql.Identifier(self.table)
        )


if __name__ == '__main__':
    mr = ModelsRepository()
