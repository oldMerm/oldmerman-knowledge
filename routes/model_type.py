from typing import List, Optional

from fastapi import APIRouter
from fastapi.params import Depends, Param

from common import Result
from db.entities import ModelType
from db.models.models_param import ModelsWithTypeParam
from services import get_model_type_service
from services.model_type_service import ModelTypeService
from utils import get_logger

"""Description
Controller about model type management

Date: 2026-5-16
Created by oldmerman
"""

logger = get_logger(__name__)

router = APIRouter(prefix="/model_type", tags=["model_type"])


@router.get("/all")
def get_all(service: ModelTypeService = Depends(get_model_type_service)
            ) -> Result[List[ModelType]]:
    return Result.success(
        data=service.select_all_type()
    )


@router.get("/vector-models")
def select_type_models(type_name: Optional[str] = Param(description="要查询的模型名称"),
                            service: ModelTypeService = Depends(get_model_type_service)
                            ) -> Result[ModelsWithTypeParam]:
    return Result.success(
        data=service.select_type_models(type_name)
    )


@router.post("")
def insert_type(model_type_name: str,
                service: ModelTypeService = Depends(get_model_type_service)
                ) -> Result:
    service.insert_type(model_type_name)
    return Result.success()


@router.delete("")
def delete_type(type_id: int,
                service: ModelTypeService = Depends(get_model_type_service)
                ) -> Result:
    service.delete_type(type_id)
    return Result.success()
