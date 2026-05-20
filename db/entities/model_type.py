from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class ModelType:
    id: Optional[int] = None
    model_type_name: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "model_type_name": self.model_type_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }