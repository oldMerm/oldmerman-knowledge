"""Description
the service of /routes/auth.py

Date: 2026-4-23
Created by oldmerman
"""

import uuid

import bcrypt
from datetime import datetime, timezone
from typing import Optional

from db.connection import get_db_connection
from db.entities.user import User, UserStatus
from utils.jwt import create_token
from utils.logger import get_logger



logger = get_logger("services.auth")

class AuthService:
    @staticmethod
    def _hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def _verify_password(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

    def _get_user_by_username(self, username: str) -> Optional[User]:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, user_uuid, username, email, phone, password_hash, status, "
                    "created_at, updated_at, last_login_at FROM users WHERE username = %s",
                    (username,)
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
                    password_hash=row[5],
                    status=UserStatus(row[6]),
                    created_at=row[7],
                    updated_at=row[8],
                    last_login_at=row[9],
                )

    def _update_last_login(self, user_id: int, ip_address: Optional[str]) -> None:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE users SET last_login_at = %s, last_login_ip = %s WHERE id = %s",
                    (datetime.now(timezone.utc), ip_address, user_id)
                )

    def register(
        self,
        username: str,
        password: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> User:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id FROM users WHERE username = %s OR (email = %s AND %s IS NOT NULL) "
                    "OR (phone = %s AND %s IS NOT NULL)",
                    (username, email, email, phone, phone)
                )
                if cur.fetchone():
                    raise ValueError("Username, email or phone already exists")

                password_hash = self._hash_password(password)
                user_uuid = str(uuid.uuid4())

                cur.execute(
                    "INSERT INTO users (user_uuid, username, email, phone, password_hash, ip_address, status) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s) "
                    "RETURNING id, created_at, updated_at",
                    (user_uuid, username, email, phone, password_hash, ip_address, UserStatus.ACTIVE)
                )
                row = cur.fetchone()

                user = User(
                    id=row[0],
                    user_uuid=user_uuid,
                    username=username,
                    email=email,
                    phone=phone,
                    password_hash=password_hash,
                    ip_address=ip_address,
                    status=UserStatus.ACTIVE,
                    created_at=row[1],
                    updated_at=row[2],
                )
                logger.info(f"User registered: {username}")
                return user

    def login(self, username: str, password: str, ip_address: Optional[str] = None) -> str:
        user = self._get_user_by_username(username)
        if not user:
            raise ValueError("Invalid username or password")

        if user.status != UserStatus.ACTIVE:
            raise ValueError("Account is disabled")

        if not self._verify_password(password, user.password_hash):
            raise ValueError("Invalid username or password")

        self._update_last_login(user.id, ip_address)
        token = create_token(str(user.user_uuid), username)
        logger.info(f"User logged in: {username}")
        return token

    def logout(self) -> bool:
        return True

def get_auth_service() -> AuthService:
    return AuthService()