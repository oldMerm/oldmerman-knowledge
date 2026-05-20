import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum
from typing import Optional


class UserStatus(IntEnum):
    DISABLED = 0
    ACTIVE = 1
    DELETED = -1


@dataclass
class User:
    id: Optional[int] = None
    user_uuid: str = field(default_factory=lambda: str(uuid.uuid4()))
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password_hash: Optional[str] = None
    ip_address: Optional[str] = None
    last_login_ip: Optional[str] = None
    status: UserStatus = UserStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_login_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_uuid": self.user_uuid,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
        }