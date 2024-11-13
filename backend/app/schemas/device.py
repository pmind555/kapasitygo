# app/schemas/device.py

from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional

class DeviceBase(BaseModel):
    location_name: str
    latitude: float
    longitude: float

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    location_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: Optional[str] = "active"

class Device(DeviceBase):
    device_id: UUID4
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
