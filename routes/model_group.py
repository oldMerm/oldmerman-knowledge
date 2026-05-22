from typing import Optional, List

from fastapi import APIRouter
from fastapi.params import Depends

from common import Result

from db.entities import ModelsGroup
from db.models import ModelsGroupRender, ModelsGroupCreateParam
from services import get_model_manage_service
from services.model_group_service import ModelManageService
from utils.logger import get_logger

"""Description
Controller about model and model group management

Date: 2026-5-1
Created by oldmerman
"""

logger = get_logger(__name__)

router = APIRouter(prefix="/model_group", tags=["model_group"])


@router.get("/render")
def get_all_group(service: ModelManageService = Depends(get_model_manage_service)
                        ) -> Result[List[ModelsGroupRender]]:
    return Result.success(
        data=service.get_render_group()
    )


@router.get("")
def get_model_group(group_uuid: Optional[str] = None,
                          service: ModelManageService = Depends(get_model_manage_service)
                          ) -> Result[ModelsGroup]:
    return Result.success(
        data=service.get_model_group(group_uuid)
    )


@router.post("")
def create_group(dto: ModelsGroupCreateParam,
                       service: ModelManageService = Depends(get_model_manage_service)
                       ) -> Result[str]:
    return Result.success(
        data=service.create_group(dto.group_name, dto.group_attr, dto.group_key, dto.base_url)
    )


@router.delete("")
def delete_group(group_uuid: str,
                       service: ModelManageService = Depends(get_model_manage_service)
                       ) -> Result[int]:
    return Result.success(
        data=service.delete_group(group_uuid)
    )
