import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Model:
    id: Optional[int] = None
    model_name: Optional[str] = None
    group_uuid: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_uuid: str = field(default_factory=lambda: str(uuid.uuid4()))
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "model_name": self.model_name,
            "group_uuid": self.group_uuid,
            "user_uuid": self.user_uuid,
            "api_key": self.api_key,
            "base_url": self.base_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }