from typing import Optional

from db.connection import get_db_connection
from db.entities.user import User, UserStatus
from utils.logger import get_logger

logger = get_logger("services.user")


class UserService:

    @staticmethod
    def obfuscate_phone(phone: Optional[str]) -> Optional[str]:
        if not phone or len(phone) < 4:
            return None
        return "*" * (len(phone) - 4) + phone[-4:]

    def get_user_by_uuid(self, user_uuid: str) -> Optional[User]:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, user_uuid, username, email, phone, status, "
                    "created_at, updated_at FROM users WHERE user_uuid = %s",
                    (user_uuid,)
                )
                row = cur.fetchone()
                if not row:
                    return None
                return User(
                    id=row[0],
                    user_uuid=row[1],
                    username=row[2],
                    email=row[3],
                    phone=row[4],
                    status=UserStatus(row[5]),
                    created_at=row[6],
                    updated_at=row[7],
                )

    def update_username(self, user_uuid: str, new_username: str) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE users SET username = %s, updated_at = NOW() WHERE user_uuid = %s",
                    (new_username, user_uuid)
                )
                return cur.rowcount > 0


def get_user_service() -> UserService:
    return UserService()