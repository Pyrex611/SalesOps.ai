from datetime import datetime
from pydantic import BaseModel

from app.models.entities import CallStatus


class CallOut(BaseModel):
    id: int
    file_name: str
    status: CallStatus
    transcript: str
    analysis: dict
    created_at: datetime

    model_config = {'from_attributes': True}
