from datetime import datetime
from typing import Any

from pydantic import BaseModel


class AnalysisResponse(BaseModel):
    id: str
    resume_id: str | None
    resume_filename: str | None
    analysis_type: str
    input_type: str
    result: dict[str, Any]
    created_at: datetime
    model_version: str