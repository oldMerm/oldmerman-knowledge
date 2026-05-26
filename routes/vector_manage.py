"""Description
Controller about vector database management

Date: 2026-5-19
Created by oldmerman
"""

from typing import List, Any, Optional

from fastapi import APIRouter, UploadFile, Request, Form
from fastapi.params import Depends, Body

from common import Result
from db.entities import VectorCollection
from db.models import VectorCollectionUpdateParam
from services.vector_manage_service import VectorManageService, get_vector_manage_service
from utils import UserContext

from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/vector-manage", tags=["vector"])


@router.post("/upload")
async def upload(req: Request,
                 collection_name: str = Form(description="所要向量化数据所处的集合"),
                 file: Optional[UploadFile] = Form(description="向量化使用的文档，最大10MB"),
                 metadatas: Optional[dict[str, Any]] = Form(default={}, description="切分的文档元数据"),
                 language: str = Form(default='en', description="文档使用的主语言"),
                 service: VectorManageService = Depends(get_vector_manage_service)) -> Result[dict[str, List[str]]]:
    user_id = UserContext.get_user_id(req)
    return Result.success(
        data=await service.upload(user_id, collection_name, metadatas, file, language)
    )


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


@router.delete("/{collection_id}")
def remove_collection(collection_id: int,
                      service: VectorManageService = Depends(get_vector_manage_service)
                      ) -> Result:
    return Result.success(
        data=service.remove_collection(collection_id)
    )
