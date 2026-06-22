"""Description
文档管理相关业务代码

Date: 2026-6-9
Created by oldmerman
"""
import math

from fastapi.params import Depends

from common import Page
from db.dao import DocumentsRepository
from utils import get_logger

logger = get_logger(__name__)

class DocumentManageService:

    def __init__(self,
                 dao: DocumentsRepository):
        self.__mapper = dao

    def page(self, current, size, collection_name):
        totals = self.__mapper.get_totals()
        start = (current - 1) * size
        data = self.__mapper.page(start, size, collection_name)
        return Page(
            current=current,
            size=size,
            total=totals,
            page_num=math.ceil(totals / size),
            data=data
        )

    def delete_document(self, doc_id):
        self.__mapper.delete_document(doc_id)
        logger.info(f"Successfully delete document:{doc_id}")


def get_document_manage_service(
        document_dao: DocumentsRepository = Depends(),
) -> DocumentManageService:
    return DocumentManageService(document_dao)