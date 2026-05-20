from typing import List

from fastapi.params import Depends

from db.dao.models_group_repository import ModelsGroupRepository
from db.dao.models_repository import ModelsRepository
from db.entities import ModelsGroup
from db.models import ModelsGroupRender
from utils.logger import get_logger

"""Description
The bus code about model_manage

Date: 2026-5-1
Created by oldmerman
"""

logger = get_logger(__name__)


class ModelManageService:

    def __init__(self,
                 group_dao: ModelsGroupRepository):
        self.__mapper = group_dao

    def get_render_group(self) -> List[ModelsGroupRender]:
        return self.__mapper.get_render_group()

    def get_model_group(self, group_uuid) -> ModelsGroup:
        param = self.__mapper.get_group(group_uuid)
        return param

    def create_group(self, name, attr, key, base_url) -> str:
        name_size = len(name)
        if name_size <= 1 or name_size > 50:
            logger.error(f"Group added fail because the length invalid")
            raise ValueError(f"Group added fail because the length invalid")

        if key is None or base_url is None:
            logger.error(f"Group added fail because the key or base_url is null")
            raise ValueError(f"Group added fail because the key or base_url is null")

        return self.__mapper.create_group(group_name=name, group_attr=attr, api_key=key, base_url=base_url)

    def delete_group(self, group_uuid):
        return self.__mapper.remove_group(group_uuid)


def get_model_manage_service(
        model_dao: ModelsGroupRepository = Depends()
) -> ModelManageService:
    return ModelManageService(model_dao)
