import logging
from typing import List

from fastapi.params import Depends

from db.dao.model_type_repository import ModelTypeRepository
from utils.logger import get_logger

"""Description
The bus code about model_type

Date: 2026-5-16
Created by oldmerman
"""

logger = get_logger(__name__)


class ModelTypeService:

    def __init__(self,
                 model_dao: ModelTypeRepository):
        self.__mapper = model_dao


    def select_all_type(self):
        return self.__mapper.select_all()


    def insert_type(self, model_type_name):
        self.__mapper.insert(model_type_name)


    def delete_type(self, type_id):
        if not self.__mapper.delete_by_id(type_id):
            raise ValueError(f"failed to delete type: {type_id}")

def get_model_type_service(
        model_dao: ModelTypeRepository = Depends()
) -> ModelTypeService:
    return ModelTypeService(model_dao)