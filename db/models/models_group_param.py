from typing import Optional

from pydantic import BaseModel


class ModelsGroupRender(BaseModel):
    group_uuid: str
    group_name: Optional[str] = None
    group_attr: Optional[str] = None

class ModelsGroupCreateParam(BaseModel):
    group_name: str
    group_attr: Optional[str] = None
    group_key: str
    base_url: str