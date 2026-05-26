from fastapi import Request
from typing import Optional

class UserContext:

    @staticmethod
    def get_user_id(req: Request) -> Optional[str]:
        return getattr(req.state.user, "user_id", None)

    @staticmethod
    def get_username(req: Request) -> Optional[str]:
        return getattr(req.state.user, "username", None)