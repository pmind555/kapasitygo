# app/schemas/readings.py

from pydantic import BaseModel, UUID4, conint
from datetime import datetime

class ReadingCreate(BaseModel):
    timestamp: datetime
    fullness_level: conint(ge=0, le=100)

class Reading(ReadingCreate):
    reading_id: int
    device_id: UUID4
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
