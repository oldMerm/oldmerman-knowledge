from datetime import datetime

from pydantic import BaseModel, Field

# 用于统计时间和总数的公共实体
class DateWithSumParam(BaseModel):
    date: datetime = Field(description="创建时间")
    sum: int = Field(default=0, description="总数")