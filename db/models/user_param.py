from pydantic import BaseModel
from typing import Optional

class UserSettingParam(BaseModel):
    user_uuid: str
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    status: int

class UpdateUsernameRequest(BaseModel):
    username: str