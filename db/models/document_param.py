from datetime import datetime

from pydantic import BaseModel

class DocumentPageParam(BaseModel):
    id: str
    filename: str
    filesize: int
    collection_name: str
    updated_at: datetime
    doc_num: int = 0