"""Description
the vector client about the project

Date: 2026-5-19
Created by oldmerman
"""

from functools import lru_cache

import chromadb
from chromadb import ClientAPI

from agents.embedding.zhi_pu_embedding import get_zhi_pu_embedding
from config import get_settings
from utils import get_logger

logger = get_logger(__name__)


@lru_cache
def get_vector_database() -> ClientAPI:
    settings = get_settings()
    return chromadb.PersistentClient(path=settings.VECTOR_PERSIST_URL)


if __name__ == "__main__":
    client = get_vector_database()
    # query demo
    print(client.get_collection("text_collection").query(
        query_embeddings=[item.embedding for item in
                          get_zhi_pu_embedding("your-api-key").create(
                              input="老鱼人博客oss使用的消费量",
                              model="embedding-3",
                              dimensions=1024
                          ).data],
        n_results=1
    ))
