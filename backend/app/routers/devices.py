# app/routers/devices.py
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..schemas.device import Device, DeviceUpdate
from ..schemas.alertdevice import AlertDevice
from ..dependencies import internal_only

router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
    dependencies=[Depends(internal_only)]
)


@router.get("/alerts", response_model=List[schemas.AlertDevice])
def read_alerts(
    min_fullness: int = Query(0, ge=0, le=100),
    max_fullness: int = Query(100, ge=0, le=100),
    skip: int = 0,
    limit: int = Query(100, le=100),
    db: Session = Depends(get_db),
):
    """Retrieve a list of devices with the latest fullness level and timestamp, filtered by fullness level."""
    subquery = (
        db.query(models.Reading.device_id, models.Reading.fullness_level, models.Reading.timestamp)
        .distinct(models.Reading.device_id)
        .order_by(models.Reading.device_id, desc(models.Reading.timestamp))
        .subquery()
    )

    alerts = (
        db.query(
            models.Device.location_name,
            models.Device.latitude,
            models.Device.longitude,
            models.Device.device_id,
            models.Device.status,
            models.Device.created_at,
            subquery.c.timestamp,
            subquery.c.fullness_level,
        )
        .join(subquery, models.Device.device_id == subquery.c.device_id)
        .filter(subquery.c.fullness_level >= min_fullness, subquery.c.fullness_level <= max_fullness)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [
        schemas.AlertDevice(
            location_name=device.location_name,
            latitude=device.latitude,
            longitude=device.longitude,
            device_id=device.device_id,
            status=device.status,
            created_at=device.created_at,
            timestamp=device.timestamp,
            fullness_level=device.fullness_level,
        )
        for device in alerts
    ]


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


