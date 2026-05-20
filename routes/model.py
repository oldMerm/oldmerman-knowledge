from typing import List

from fastapi import APIRouter, Request
from fastapi.params import Depends, Param, Body

from common import Result
from db.models import ModelRenderParam
from db.models.models_param import ModelCreateParam
from services import get_model_service
from services.model_service import ModelService

from utils.logger import get_logger

"""Description
Controller about model management

Date: 2026-5-2
Created by oldmerman
"""

logger = get_logger(__name__)

router = APIRouter(prefix="/model", tags=["model"])


@router.get("/render")
async def get_render_model(group_uuid: str = Param(description="模型所属分组uuid"),
                           service: ModelService = Depends(get_model_service)) -> Result[List[ModelRenderParam]]:
    return Result.success(
        data=service.get_group_models(group_uuid)
    )


@router.post("")
async def add_model(request: Request,
                    dto: ModelCreateParam = Body(description="创建模型所需参数体"),
                    service: ModelService = Depends(get_model_service)):
    user_uuid = getattr(request.state.user, "user_id", None)
    return Result.success(
        data=service.add_model(dto, user_uuid)
    )


@router.delete("")
async def delete_model(model_id: int = Param(description="模型唯一id"),
                       service: ModelService = Depends(get_model_service)):
    return Result.success(
        data=service.delete_model(model_id)
    )
