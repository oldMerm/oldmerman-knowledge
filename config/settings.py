"""Description
the common settings about the project

Date: 2026-5-19
Created by oldmerman
"""

from typing import List

from pydantic_settings import BaseSettings
from pydantic import  Field
from functools import lru_cache


class Settings(BaseSettings):
    """settings"""

    # base
    APP_NAME: str = Field(default="oldmerman-knowledge", alias="APP_NAME")
    APP_VERSION: str = Field(default="1.0.0", alias="APP_VERSION")

    # sever config
    HOST: str = Field(default="localhost", alias="HOST")
    PORT: int = Field(default=8000, alias="PORT")

    # database
    MAX_DATABASE_POOL_SIZE: int = Field(default=10, alias="DATABASE_POOL_SIZE")

    # chromadb
    VECTOR_PERSIST_URL: str = Field(default=r"D:\chromadb", alias="VECTOR_PERSIST_URL")

    # 文档策略
    MAX_FILE_SIZE: int = 10 * 1024 * 1024 # 10MB
    MAX_CHUNK_SIZE: int = 50 * 1024 # 50KB
    # 向量和重排序
    EMBEDDING_RESULT_N: int = 10
    RERANK_TOP_N: int = 4

    # API白名单
    # VALID_API_KEYS: dict[str, str] = {
    #     ""
    # }
    IP_WHITELIST: List[str] = [
        "192.168.1.0/24"
    ]

@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()