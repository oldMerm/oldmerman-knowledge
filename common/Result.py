from typing import Any, Generic, TypeVar, Optional
from datetime import datetime
from pydantic import BaseModel

T = TypeVar('T')

class Result(BaseModel, Generic[T]):
    code: int
    message: str
    data: Optional[T]
    time: str
    request: str

    @staticmethod
    def success(data: Any = None, message: str = "success", code: int = 200, request: str = ""):
        return Result(
            code=code,
            message=message,
            data=data,
            time=datetime.now().isoformat(),
            request=request
        )

    @staticmethod
    def error(message: str = "error", code: int = 500, data: Any = None, request: str = ""):
        return Result(
            code=code,
            message=message,
            data=data,
            time=datetime.now().isoformat(),
            request=request
        )
