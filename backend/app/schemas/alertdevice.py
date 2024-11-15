# app/schemas/alertdevice.py

from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional

class AlertDevice(BaseModel):
    location_name: str
    latitude: float
    longitude: float
    device_id: UUID4
    status: str
    created_at: datetime
    timestamp: datetime
    fullness_level: int

    model_config = {
        "from_attributes": True
    }