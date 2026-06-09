import math

from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class Page(BaseModel, Generic[T]):
    current: int = Field(default=1,description="当前页码")
    size: int = Field(default=10,description="每页条数")
    total: int = Field(default=0, description="总条数")
    page_num: int = Field(default=0, description="总页数")
    data: Optional[T]