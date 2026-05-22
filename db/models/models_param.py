from typing import Optional, List

from pydantic import BaseModel


class ModelRenderParam(BaseModel):
    model_id: Optional[int] = None
    model_name: Optional[str] = None
    type_id: Optional[int] = None
    type_name: Optional[str] = None

class ModelRenderParam1(BaseModel):
    model_id: Optional[int] = None
    model_name: Optional[str] = None

class ModelRegisterParam(BaseModel):
    id: Optional[int] = None
    model_name: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None

class ModelCreateParam(BaseModel):
    model_name: Optional[str] = None
    group_uuid: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    type_id: Optional[int] = None

class ModelsWithTypeParam(BaseModel):
    type_id: Optional[int] = None
    type_name: Optional[str] = None
    models: List[ModelRenderParam1] = None
