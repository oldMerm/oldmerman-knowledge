import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class ModelsGroup:
    id: Optional[int] = None
    group_uuid: str = field(default_factory=lambda: str(uuid.uuid4()))
    group_name: Optional[str] = None
    group_attr: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    api_key: Optional[str] = None
    base_url: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "group_uuid": self.group_uuid,
            "group_name": self.group_name,
            "group_attr": self.group_attr,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "base_url": self.base_url
        }