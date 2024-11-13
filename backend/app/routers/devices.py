# app/routers/devices.py
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..schemas.device import Device, DeviceUpdate
from ..dependencies import internal_only

router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
    dependencies=[Depends(internal_only)]
)


@router.post("/", response_model=schemas.Device, status_code=201)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    """Create a new device."""
    db_device = models.device.Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

@router.get("/", response_model=List[schemas.Device])
def read_devices(skip: int = 0, limit: int = Query(100, le=100), db: Session = Depends(get_db)):
    """Retrieve a list of devices with pagination."""
    devices = db.query(models.device.Device).offset(skip).limit(limit).all()
    return devices

@router.get("/{device_id}", response_model=schemas.Device)
def read_device(device_id: UUID, db: Session = Depends(get_db)):
    """Retrieve a specific device by its UUID."""
    device = db.query(models.device.Device).filter(models.device.Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@router.put("/{device_id}", response_model=Device)
def update_device(device_id: UUID, device_update: DeviceUpdate, db: Session = Depends(get_db)):
    # Fetch the existing device by device_id
    db_device = db.query(models.device.Device).filter(models.device.Device.device_id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")

    # Update only the fields provided in the request
    update_data = device_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_device, key, value)

    # Commit changes to the database
    db.commit()
    db.refresh(db_device)
    return db_device
