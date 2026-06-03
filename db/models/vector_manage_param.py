from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

class VectorCollectionUpdateParam(BaseModel):
    embedding_id: Optional[int] = None
    collection_name: Optional[str] = Field(default=None, max_length=30)
    collection_alias: Optional[str] = Field(default=None, max_length=30)
    collection_description: Optional[str] = Field(default=None, max_length=255)
    items_number: Optional[int] = None
    dimensions: int = 1024

class VectorCollectionRenderParam(BaseModel):
    id: Optional[int] = None
    embedding_id: Optional[int] = None
    embedding_name: Optional[str] = None
    collection_name: Optional[str] = None
    collection_alias: Optional[str] = None
    collection_description: Optional[str] = None
    items_number: Optional[int] = None
    created_at: datetime = Field(default=datetime.now)
    dimensions: Optional[int] = 1024

class VectorCollectionCreateParam(BaseModel):
    ids: List[str] = None
    model_id: int = None
    tokens: dict[str, int] = None
