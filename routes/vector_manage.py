from typing import List

from fastapi import APIRouter, Request
from fastapi.params import Depends, Param, Body

from common import Result
from db.models import ModelRenderParam
from services.vector_manage_service import VectorManageService, get_vector_manage_service

from utils.logger import get_logger

"""Description
Controller about vector database management

Date: 2026-5-19
Created by oldmerman
"""

logger = get_logger(__name__)

router = APIRouter(prefix="/vector_manage", tags=["vector"])


@router.get("/render")
async def get_render_collection(service: VectorManageService = Depends(get_vector_manage_service)
                                ) -> Result[List[ModelRenderParam]]:
    return Result.success(
        data=service.get_render_list()
    )

