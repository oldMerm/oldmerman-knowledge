import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class RequestTimeLog:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    thread_id: Optional[str] = None
    total_duration: Optional[float] = None
    prompt: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    model_id: Optional[int] = None