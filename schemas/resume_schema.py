from datetime import datetime

from pydantic import BaseModel


class ResumeResponse(BaseModel):
    id: str
    filename: str
    file_reference: str
    created_at: datetime