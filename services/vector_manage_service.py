"""Description
The bus code about vector manage

Date: 2026-5-19
Created by oldmerman
"""

from uuid import uuid4
from typing import List, Any

from fastapi import UploadFile
from fastapi.params import Depends

from common import BusinessException
from config import get_settings
from db.dao import VectorCollectionRepository
from db.dao.tokens_usage_repository import TokensUsageRepository
from db.models import VectorCollectionRenderParam
from db.models.vector_manage_param import VectorCollectionUpdateParam
from db.vector_connection import ChromaVectorHelper
from utils import language_separators
from utils.file_processor import extract_text
from utils.logger import get_logger
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

logger = get_logger(__name__)
settings = get_settings()


class VectorManageService:

    def __init__(self,
                 vector_dao: VectorCollectionRepository,
                 tokens_usage_dao: TokensUsageRepository):
        self.__mapper = vector_dao
        self.__tokens_usage_mapper = tokens_usage_dao

    async def upload(self, user_id: str, collection_name: str, metadatas: dict[str, Any],
                     file: UploadFile, language: str) -> list[str]:
        """
            向量化流程梳理：
            1. 判断文件是否大于最大的阈值MAX_FILE_SIZE
            2. 封装元数据，准备切分
            3. 切分文章并落库，postgresSQL，chromadb
        """
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

        # 元数据封装
        metadatas["author"] = user_id
        metadatas["filename"] = filename

        text = extract_text(original_content, filename) # 提纯文本
        original_doc = Document(
            page_content=text,
            metadata=metadatas
        )

        # 文档切分器(根据标点符号优先级)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=separators
        )
        doc_chunks = splitter.split_documents([original_doc])  # 切分

        batch_ids = [str(uuid4()) for i in range(len(doc_chunks))]  # 向量化的文档id
        batch_texts = [chunk.page_content for chunk in doc_chunks]  # 文档分块数据
        batch_metadatas = [chunk.metadata for chunk in doc_chunks]  # 分块的元数据

        # hash进行重复过滤
        res = self.__mapper.filter_exist_hash(batch_ids, batch_texts, collection_name=collection_name, metadatas=batch_metadatas)
        filter_ids = res.get("ids")
        filter_documents = res.get("documents")
        filter_metadatas = res.get("metadatas")
        filter_content_hashes = res.get("content_hashes")

        if len(filter_ids) == 0:
            logger.warning("documents are exist in DB")
            raise BusinessException("documents are exist in DB")

        helper = None
        try:
            # 入库
            self.__mapper.embeddings_record(
                ids=filter_ids,
                texts=filter_documents,
                metadatas=filter_metadatas,
                doc_id=doc_id,
                content_hashes=filter_content_hashes
            )

            # 入向量库
            helper = ChromaVectorHelper(collection_name=collection_name)
            response = await helper.add(
                ids=filter_ids,
                documents=filter_documents,
                metadatas=filter_metadatas
            )
        except ValueError as e:
            self.__mapper.remove_embeddings_record(doc_id)
            helper.delete(filter_ids)
            logger.error(f"Failed to add document in DB: {e}")
            raise BusinessException("Failed to add document in DB: {e}")

        # 记录文档增量
        self.__mapper.update_collection(collection_name=collection_name, number_update=len(filter_ids))
        # 记录token消耗量
        self.__tokens_usage_mapper.add(user_id, response.model_id, response.tokens)
        return response.ids

    def get_render_list(self) -> List[VectorCollectionRenderParam]:
        return self.__mapper.select_name_list()

    def insert_collection(self, dto: VectorCollectionUpdateParam) -> int:
        collection_name = dto.collection_name
        collection_desc = dto.collection_description
        embedding_id = dto.embedding_id
        if collection_name is None or collection_desc is None or embedding_id is None:
            logger.error("Invalid update param because is None")
            raise BusinessException("Invalid update param because is None")

        dimensions = dto.dimensions
        collection_alias = dto.collection_alias
        collection_id = self.__mapper.insert_collection(
            embedding_id=embedding_id,
            collection_name=collection_name,
            collection_alias=collection_alias,
            collection_description=collection_desc,
            items_number=0,
            dimensions=dimensions
        )

        try:
            v_metadata = {
                "embedding_id": embedding_id,
                "collection_description": collection_desc,
                "dimensions": str(dimensions)
            }
            if collection_alias is not None:
                v_metadata["collection_alias"] = collection_alias

            ChromaVectorHelper.create_collection(
                name=collection_name,
                metadata=v_metadata
            )
        except Exception:
            self.__mapper.remove_collection(collection_id)
            raise BusinessException(
                f"collection added fail, because collection_name:{collection_name} is exist in vector database")

        return collection_id

    def remove_collection(self, collection_id: int):
        collection_name = self.__mapper.remove_collection(collection_id=collection_id)
        ChromaVectorHelper.delete_collection(collection_name=collection_name)
        logger.info(f"remove collection:{collection_name} success")

    def get_collections(self):
        return self.__mapper.simple_select_name_list()

def get_vector_manage_service(
        vector_dao: VectorCollectionRepository = Depends(),
        tokens_usage_dao: TokensUsageRepository = Depends(),
) -> VectorManageService:
    return VectorManageService(vector_dao, tokens_usage_dao)


if __name__ == "__main__":
    print("a")
