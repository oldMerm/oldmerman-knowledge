from functools import lru_cache

import chromadb
from chromadb import ClientAPI

from config import get_settings
from utils import get_logger

"""Description
the vector client about the project

Date: 2026-5-19
Created by oldmerman
"""

logger = get_logger(__name__)

@lru_cache
def get_vector_database() -> ClientAPI:
    settings = get_settings()
    return chromadb.PersistentClient(path=settings.VECTOR_PERSIST_URL)



