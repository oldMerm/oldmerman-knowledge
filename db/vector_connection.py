"""Description
the vector client about the project

Date: 2026-5-19
Created by oldmerman
"""
import os
from functools import lru_cache

import chromadb
from chromadb import ClientAPI

from agents.embedding import EmbeddingsGetterParam, get_embeddings_supported
from config import get_settings
from utils import get_logger

logger = get_logger(__name__)


@lru_cache
def get_vector_database() -> ClientAPI:
    settings = get_settings()
    return chromadb.PersistentClient(path=settings.VECTOR_PERSIST_URL)


if __name__ == "__main__":
    client = get_vector_database()

    e_input = ["广东省东莞市西南部"]

    param = EmbeddingsGetterParam(
        api_key=os.getenv("ZHI_PU_API_KEY"),
        base_url="https://open.bigmodel.cn/api/paas/v4",
        model_name="embedding-3",
        doc=e_input,
        dimensions=1024
    )

    # query demo
    print(client.get_collection("text_collection").query(
        query_embeddings=get_embeddings_supported(param).data,
        n_results=2
    ))
