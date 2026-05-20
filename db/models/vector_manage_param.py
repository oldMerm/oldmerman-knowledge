from typing import Optional


class VectorCollectionUpdateParam:
    embedding_id: Optional[int] = None
    collection_name: Optional[str] = None
    collection_alias: Optional[str] = None
    collection_description: Optional[str] = None
    items_number: Optional[int] = None

    def to_metadata(self) -> dict:
        return {
            "embedding_id": self.embedding_id,
            "collection_name": self.collection_name,
            "collection_alias": self.collection_alias,
            "collection_description": self.collection_description,
        }