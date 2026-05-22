from typing import List

from fastapi import APIRouter, UploadFile
from fastapi.params import Depends, Param, Body, Query

from common import Result
from db.entities import VectorCollection
from db.models import VectorCollectionUpdateParam
from services.vector_manage_service import VectorManageService, get_vector_manage_service

from utils.logger import get_logger

"""Description
Controller about vector database management

Date: 2026-5-19
Created by oldmerman
"""

logger = get_logger(__name__)

router = APIRouter(prefix="/vector-manage", tags=["vector"])


@router.get("/render")
def get_render_collection(service: VectorManageService = Depends(get_vector_manage_service)
                                ) -> Result[List[VectorCollection]]:
    return Result.success(
        data=service.get_render_list()
    )


@router.post("")
def insert_collection(dto: VectorCollectionUpdateParam = Body(description="向量集合更新对应实体"),
                            service: VectorManageService = Depends(get_vector_manage_service)
                            ) -> Result[int]:
    return Result.success(
        data=service.insert_collection(dto)
    )


# @router.post("/upload")
# async def upload(files: list[UploadFile]):
#     return [file.filename for file in files]


@router.delete("/{collection_id}")
def remove_collection(collection_id: int,
                            service: VectorManageService = Depends(get_vector_manage_service)
                            ) -> Result:
    return Result.success(
        data=service.remove_collection(collection_id)
    )
