"""Description
The bus code about vector manage

Date: 2026-5-19
Created by oldmerman
"""

from uuid import uuid4
from typing import List, Any

from chromadb import ClientAPI
from fastapi import UploadFile
from fastapi.params import Depends

from common import BusinessException
from config import get_settings
from db import get_vector_database
from db.dao import VectorCollectionRepository
from db.entities import VectorCollection
from db.models.vector_manage_param import VectorCollectionUpdateParam
from utils import language_separators
from utils.file_processor import extract_text, split_to_chunks
from utils.logger import get_logger
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

logger = get_logger(__name__)
settings = get_settings()


class VectorManageService:

    def __init__(self,
                 vector_dao: VectorCollectionRepository,
                 vector_client: ClientAPI):
        self.__mapper = vector_dao
        self.__vector_client = vector_client

    # 对每个chunk(小于50KB)进行向量化
    async def __embeddings(self, splitter, metadatas, file_content, collection_name, doc_id) -> List[str]:
        original_doc = Document(
            page_content=file_content,
            metadata=metadatas
        )
        doc_chunks = splitter.split_documents([original_doc])  # 切分

        batch_ids = [str(uuid4()) for i in range(len(doc_chunks))]  # 向量化的文档id
        batch_texts = [chunk.page_content for chunk in doc_chunks]  # 文档分块数据
        batch_metadatas = [chunk.metadata for chunk in doc_chunks]  # 分块的元数据

        return await self.__mapper.embeddings(
            collection_name=collection_name,
            ids=batch_ids,
            texts=batch_texts,
            metadatas=batch_metadatas,
            doc_id=doc_id
        )

    async def upload(self, user_id: str, collection_name: str, metadatas: dict[str, Any],
                     file: UploadFile, language: str) -> dict[str, List[str]]:
        if user_id is None:
            raise BusinessException("Invalid param because userId is None")

        # 文件处理逻辑
        original_content = await file.read()
        filename = file.filename
        file_size = len(original_content)
        if file_size > settings.MAX_FILE_SIZE:
            raise BusinessException("The uploaded file exceeds 10MB")
        # 记录文件并返回访问id
        doc_id = self.__mapper.insert_document(user_id, filename, file_size, collection_name)

        # 开始向量化流程
        # 获取对应语言切分策略符号的优先级
        separators = language_separators[language]
        if separators is None:
            raise BusinessException(f"Not supported language {language}")

        # 文档切分器(根据标点符号优先级)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=separators
        )
        # 元数据封装
        metadatas["author"] = user_id
        metadatas["filename"] = filename

        ids: dict[str, List[str]] = {}
        docs_count_group = 1
        if file_size < settings.MAX_CHUNK_SIZE:
            # 若占用小于最大的chunk_size, 直接向量化
            text = extract_text(original_content, filename)
            ids["doc" + str(docs_count_group)] = await self.__embeddings(splitter, metadatas, text, collection_name, doc_id)
        else:
            # 否则切块进行向量化
            chunks = split_to_chunks(original_content, filename)
            for chunk in chunks:
                metadatas["file_chunk_name"] = chunk["name"]
                ids["doc" + str(docs_count_group)] = await self.__embeddings(splitter, metadatas, chunk["text"], collection_name, doc_id)
                docs_count_group += 1
        return ids

    def get_render_list(self) -> List[VectorCollection]:
        return self.__mapper.select_name_list()

    def insert_collection(self, dto: VectorCollectionUpdateParam) -> int:
        collection_name = dto.collection_name
        collection_desc = dto.collection_description
        embedding_id = dto.embedding_id
        if collection_name is None or collection_desc is None or embedding_id is None:
            logger.error("Invalid update param because is None")
            raise BusinessException("Invalid update param because is None")

        collection_id = self.__mapper.insert_collection(
            embedding_id=embedding_id,
            collection_name=collection_name,
            collection_alias=dto.collection_alias,
            collection_description=dto.collection_description,
            items_number=0,
            dimensions=dto.dimensions
        )

        return collection_id

    def remove_collection(self, collection_id: int):
        collection_name = self.__mapper.remove_collection(collection_id=collection_id)
        self.__vector_client.delete_collection(collection_name)
        logger.info(f"remove collection:{collection_name} success")


def get_vector_manage_service(
        vector_dao: VectorCollectionRepository = Depends(),
        vector_client: ClientAPI = Depends(get_vector_database)
) -> VectorManageService:
    return VectorManageService(vector_dao, vector_client)


if __name__ == "__main__":
    print("a")
