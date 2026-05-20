from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class VectorCollection:
    id: Optional[int] = None
    embedding_id: Optional[int] = None
    collection_name: Optional[str] = None
    collection_alias: Optional[str] = None
    collection_description: Optional[str] = None
    items_number: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "embedding_id": self.embedding_id,
            "collection_name": self.collection_name,
            "collection_alias": self.collection_alias,
            "collection_description": self.collection_description,
            "items_number": self.items_number,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

