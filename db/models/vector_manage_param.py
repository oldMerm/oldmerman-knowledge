from typing import Optional

from pydantic import BaseModel, Field


class VectorCollectionUpdateParam(BaseModel):
    embedding_id: Optional[int] = None
    collection_name: Optional[str] = Field(default=None, max_length=30)
    collection_alias: Optional[str] = Field(default=None, max_length=30)
    collection_description: Optional[str] = Field(default=None, max_length=255)
    items_number: Optional[int] = None

    def to_metadata(self) -> dict:
        metadata = {}

        if self.embedding_id is not None:
            metadata["embedding_id"] = str(self.embedding_id)

        if self.collection_name:
            metadata["collection_name"] = str(self.collection_name)

        if self.collection_alias:
            metadata["collection_alias"] = str(self.collection_alias)

        if self.collection_description:
            metadata["collection_description"] = str(self.collection_description)

        return metadata