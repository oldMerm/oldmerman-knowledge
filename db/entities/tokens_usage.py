import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class TokenUsage:
    id: Optional[int] = None
    user_id: Optional[str] = field(default_factory=lambda: str(uuid.uuid4()))
    model_id: Optional[int] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "model_id": self.model_id,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }