from typing import List

from fastapi import APIRouter
from fastapi.params import Depends

from common import Result
from db.entities import ModelType
from services import get_model_type_service
from services.model_type_service import ModelTypeService
from utils import get_logger

"""Description
Controller about model type management

Date: 2026-5-16
Created by oldmerman
"""

logger = get_logger(__name__)

router = APIRouter(prefix="/model_type", tags=["model"])

@router.get("/all")
async def get_all(service: ModelTypeService = Depends(get_model_type_service)
                  ) -> Result[List[ModelType]]:
    return Result.success(
        data=service.select_all_type()
    )

@router.post("")
async def insert_type(model_type_name : str,
                      service: ModelTypeService = Depends(get_model_type_service)
                      ) -> Result:
    service.insert_type(model_type_name)
    return Result.success()

@router.delete("")
async def delete_type(type_id: int,
                      service: ModelTypeService = Depends(get_model_type_service)
                      ) -> Result:
    service.delete_type(type_id)
    return Result.success()