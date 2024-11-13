from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ..database import get_db
from .. import models, schemas
from ..dependencies import get_client_certificate, verify_client_certificate
from ..dependencies import internal_only

router = APIRouter(
    prefix="/readings",
    tags=["Readings"],
    dependencies=[Depends(internal_only)]
)

@router.post("/", response_model=schemas.Reading, status_code=201)
def create_reading(
    reading: schemas.ReadingCreate,
    client_cert = Depends(get_client_certificate),
    db: Session = Depends(get_db)
):
    """
    Creates a new reading for a device.
    """
    # Verify the client certificate and get the associated device_id
    device_id = verify_client_certificate(client_cert, db)

    # Create a new reading associated with the authenticated device
    reading_data = reading.model_dump()
    reading_data['device_id'] = device_id

    db_reading = models.Reading(**reading_data)
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading

@router.get("/", response_model=List[schemas.Reading])
def read_readings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of readings with pagination.
    """
    readings = db.query(models.Reading).offset(skip).limit(limit).all()
    return readings

@router.get("/{reading_id}", response_model=schemas.Reading)
def get_reading(reading_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a reading by its ID.
    """
    reading = db.query(models.Reading).filter(models.Reading.reading_id == reading_id).first()
    if not reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    return reading
