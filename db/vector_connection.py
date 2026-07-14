"""Description
the vector client about the project

Date: 2026-5-19
Created by oldmerman
"""
from functools import lru_cache
from typing import Any

import chromadb
from chromadb.api import ClientAPI

from agents.embedding import EmbeddingsGetterParam, get_embeddings_supported
from config import get_settings, SystemConfigConstants
from db.models import VectorCollectionCreateParam
from common.utils import get_logger, get_config_client

logger = get_logger(__name__)
Settings = get_settings()

_default_collection_name = None

@lru_cache
def get_vector_database() -> ClientAPI:
    settings = get_settings()
    return chromadb.PersistentClient(path=settings.VECTOR_PERSIST_URL)


# ChromaDB向量库操作封装
class VectorDatabase:
    _instance: ClientAPI | None = None

    @classmethod
    def get_client(cls) -> ClientAPI:
        path = get_settings().VECTOR_PERSIST_URL
        if cls._instance is None:
            cls._instance = chromadb.PersistentClient(path=path)
        return cls._instance

    @classmethod
    def reset(cls):
        """测试或重启时调用"""
        cls._instance = None

def set_default_knowledge(user_id: str, collection_name: str, is_enabled: bool = False):
    client = get_config_client()
    config_key = SystemConfigConstants.EMBEDDING_CONFIG_KEY

    if not is_enabled:
        client.set_config(key=config_key, new_config={"is_enabled": False}, user_id=user_id)
        logger.info(f"管理员：{user_id}, 禁用知识库")
        return

    client.set_config(config_key, {"is_enabled": True, "collection_name": collection_name}, user_id=user_id,
                      description="默认使用的知识库")
    logger.info(f"管理员：{user_id}，配置默认知识库")

class ChromaVectorHelper:

    # 显示创建集合
    @classmethod
    def create_collection(cls, name: str, metadata: dict[str, Any]):
        get_vector_database().create_collection(name=name, metadata=metadata)

    @classmethod
    def delete_collection(cls, collection_name: str):
        get_vector_database().delete_collection(collection_name)

    def __init__(self, collection_name = None):
        from db.dao import ModelsRepository, TokensUsageRepository
        global _default_collection_name

        self.client = get_vector_database()
        if not collection_name:
            if _default_collection_name is None:
                config_dict = get_config_client().get_config(key=SystemConfigConstants.EMBEDDING_CONFIG_KEY)
                if config_dict:
                    _default_collection_name = config_dict.get("collection_name")
                    collection_name = _default_collection_name
                else:
                    logger.error("未配置知识库参数，或不存在该知识库")
                    raise ValueError("未配置知识库参数，或不存在该知识库")
            else:
                collection_name = _default_collection_name

        self.collection = self.client.get_or_create_collection(collection_name)
        self.embedding_id = self.collection.metadata.get("embedding_id")
        self.token_usage_dao = TokensUsageRepository()
        model_param = ModelsRepository().select_model(self.embedding_id)
        self.embedding_param = EmbeddingsGetterParam(
            api_key=model_param.api_key,
            base_url=model_param.base_url,
            model_name=model_param.model_name,
            dimensions=self.collection.metadata.get("dimensions") or 1024,
            doc=[]
        )

    def add(self, user_id: str,
            ids: list[str] = None,
            documents: list[Any] = None,
            metadatas: list[dict[str, Any]] = None) -> VectorCollectionCreateParam:
        update_param = self.embedding_param
        update_param.doc = documents
        embeddings_with_metadata = get_embeddings_supported(update_param, False)  # 获取统一响应的数据
        # 记录嵌入向量的相关数据
        self.collection.add(
            ids=ids,
            embeddings=embeddings_with_metadata.data,
            documents=documents,
            metadatas=metadatas,
        )

        self.token_usage_dao.add(user_id, self.embedding_id, embeddings_with_metadata.tokens)
        return VectorCollectionCreateParam(
            model_id=self.embedding_id,
        )

    def delete(self, ids: list[str]):
        self.collection.delete(ids=ids)

    def query(self, user_id: str, messages: list[str], n_result: int = Settings.EMBEDDING_RESULT_N):
        query_param = self.embedding_param
        query_param.doc = messages
        res_param = get_embeddings_supported(query_param)
        self.token_usage_dao.add(user_id, self.embedding_id, res_param.tokens)
        return self.collection.query(
            query_embeddings=res_param.data,
            n_results=n_result
        )


if __name__ == "__main__":
    e_input = ["鱼人博客V1.2.5版本讲了什么？"]

    # query demo
    # p_res = ChromaVectorHelper("small_text_collection").collection.get(
    #     ids="e09b284b-d9bf-4404-887d-237479106d41"
    # )
    # print(p_res)
    print(ChromaVectorHelper("text_collection").collection.peek())
    # res = p_res.get("documents")
    #
    # m_documents = []
    # for list1 in res:
    #     for item in list1:
    #         m_documents.append(item)
    # print(m_documents)
    # print(client.get_collection("text_collection").peek())
