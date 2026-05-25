from typing import Optional

from pydantic import BaseModel, Field


class VectorCollectionUpdateParam(BaseModel):
    embedding_id: Optional[int] = None
    collection_name: Optional[str] = Field(default=None, max_length=30)
    collection_alias: Optional[str] = Field(default=None, max_length=30)
    collection_description: Optional[str] = Field(default=None, max_length=255)
    items_number: Optional[int] = None
    dimensions: int = 1024
