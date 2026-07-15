from datetime import datetime

from pydantic import BaseModel, Field

class RequestTimeLogParam(BaseModel):
    username: str = Field(default="oldmerman", description="调用者所在ip地址")
    total_duration: float = Field(default=0, description="请求耗时")
    prompt: str = Field(description="用户提示词")
    created_at: datetime = Field(description="请求发起时间")
    model_id: int = Field(description="请求的模型")

class RequestTimeRenderParam(BaseModel):
    user_count: int = Field(default=0, description="用户总访问量")
    request_time_avg: float = Field(default=0, description="请求访问平均耗时")
