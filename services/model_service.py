"""Description
The bus code about model_manage

Date: 2026-5-2
Created by oldmerman
"""

from typing import List

from fastapi.params import Depends

from db.dao.models_repository import ModelsRepository
from db.models import ModelRenderParam
from db.models.models_param import ModelCreateParam
from common.utils import get_logger



logger = get_logger(__name__)


class ModelService:

    def __init__(self,
                 model_dao: ModelsRepository):
        self.__mapper = model_dao

    @staticmethod
    def __invalid_create_param(model_name, group_uuid, user_uuid):
        return model_name is None or group_uuid is None or user_uuid is None


    def get_group_models(self, group_uuid) -> List[ModelRenderParam]:
        models = self.__mapper.select_name_list(group_uuid)
        return models


    def add_model(self, dto: ModelCreateParam, user_uuid: str) -> int:
        model_name = dto.model_name
        group_uuid = dto.group_uuid

        if self.__invalid_create_param(model_name, group_uuid, user_uuid):
            logger.error("Create param is None")
            raise ValueError("Create param is None")

        model_id = self.__mapper.insert_model(model_name, group_uuid, user_uuid,
                                              dto.api_key, dto.base_url, dto.type_id, dto.is_default)

        if model_id is None:
            logger.error("Model added failed")
            raise ValueError("Model added failed")

        return model_id

    def delete_model(self, model_id):
        logger.info(f"Delete model id: {model_id}")
        self.__mapper.remove_model(model_id)


def get_model_service(
        model_dao: ModelsRepository = Depends()
) -> ModelService:
    return ModelService(model_dao)
