"""Description
文档管理相关接口

Date: 2026-6-9
Created by oldmerman
"""
from fastapi import APIRouter
from fastapi.params import Depends

from common import Result, Page
from services.document_manage_service import DocumentManageService, get_document_manage_service
from common.utils import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/document", tags=["vector"])


@router.get("")
def get_documents(current: int = 1, size: int = 10,
                  service: DocumentManageService = Depends(get_document_manage_service),
                  collection_name: str = None
                  ) -> Result[Page]:
    return Result.success(
        data=service.page(current, size, collection_name)
    )


@router.delete("")
def delete_document(doc_id: str,
                    service: DocumentManageService = Depends(get_document_manage_service)):
    return Result.success(
        data=service.delete_document(doc_id)
    )
