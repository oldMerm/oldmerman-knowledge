from typing import List

from chromadb import ClientAPI
from fastapi.params import Depends

from db import get_vector_database
from db.dao import VectorCollectionRepository
from db.entities import VectorCollection
from db.models.vector_manage_param import VectorCollectionUpdateParam
from utils.logger import get_logger

"""Description
The bus code about vector manage

Date: 2026-5-19
Created by oldmerman
"""

logger = get_logger(__name__)

class VectorManageService:

    def __init__(self,
                 vector_dao: VectorCollectionRepository,
                 vector_client: ClientAPI):
        self.__mapper = vector_dao
        self.__vector_client = vector_client

    def get_render_list(self) -> List[VectorCollection]:
        return self.__mapper.select_name_list()

    def insert_collection(self, dto: VectorCollectionUpdateParam) -> int:
        collection_name = dto.collection_name
        collection_desc = dto.collection_description
        if collection_name is None or collection_desc is None:
            logger.error("Invalid update param because name or desc is None")
            raise ValueError("Invalid update param because name or desc is None")

        collection_id = self.__mapper.insert_collection(
            embedding_id=dto.embedding_id,
            collection_name=collection_name,
            collection_alias=dto.collection_alias,
            collection_description=dto.collection_description,
            items_number=0
        )

        try:
            self.__vector_client.create_collection(
                name=collection_name,
                metadata=dto.to_metadata()
            )
        except ValueError:
            self.__mapper.remove_collection(collection_id)
            raise ValueError(f"collection added fail, because the collection_name is exist in vector database")

        return collection_id

def get_vector_manage_service(
        vector_dao: VectorCollectionRepository = Depends(),
        vector_client: ClientAPI = Depends(get_vector_database)
) -> VectorManageService:
    return VectorManageService(vector_dao, vector_client)