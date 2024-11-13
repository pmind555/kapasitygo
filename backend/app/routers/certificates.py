# app/routers/certificates.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas
from ..dependencies import internal_only


router = APIRouter(
    prefix="/certificates",
    tags=["Certificates"],
    dependencies=[Depends(internal_only)]
)


@router.post("/", response_model=schemas.Certificate, status_code=status.HTTP_201_CREATED)
def create_certificate(
    certificate: schemas.CertificateCreate, db: Session = Depends(get_db)
):
    """
    Creates a new certificate, ensuring the device exists and serial/fingerprint uniqueness.
    """
    # Verify that the device exists
    device = db.query(models.Device).filter(
        models.Device.device_id == certificate.device_id
    ).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Device not found"
        )

    # Check for existing certificate with the same serial number
    existing_serial = models.Certificate.get_by_serial_number(certificate.certificate_serial_number, db)
    if existing_serial:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Certificate with this serial number already exists",
        )

    # Check for existing certificate with the same fingerprint
    existing_fingerprint = db.query(models.Certificate).filter(
        models.Certificate.certificate_fingerprint == certificate.certificate_fingerprint
    ).first()
    if existing_fingerprint:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Certificate with this fingerprint already exists",
        )

    # Create the certificate
    db_certificate = models.Certificate(**certificate.model_dump())
    db.add(db_certificate)
    db.commit()
    db.refresh(db_certificate)
    return db_certificate


@router.get("/", response_model=List[schemas.Certificate])
def read_certificates(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Retrieve a list of certificates with pagination and optional limits.
    """
    # Validate skip and limit
    if skip < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid skip or limit parameters",
        )
    if limit > 1000:
        limit = 1000  # Set a reasonable maximum limit

    certificates = db.query(models.Certificate).offset(skip).limit(limit).all()
    return certificates


@router.get("/{certificate_id}", response_model=schemas.Certificate)
def read_certificate(certificate_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a certificate by its ID.
    """
    certificate = db.query(models.Certificate).filter(
        models.Certificate.certificate_id == certificate_id
    ).first()
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found"
        )
    return certificate


@router.put("/{certificate_id}/revoke", response_model=schemas.Certificate)
def revoke_certificate(
    certificate_id: int, db: Session = Depends(get_db)
):
    """
    Revoke a certificate by setting its status to 'revoked'.
    """
    certificate = db.query(models.Certificate).filter(
        models.Certificate.certificate_id == certificate_id
    ).first()
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found"
        )

    if certificate.status == schemas.CertificateStatus.revoked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Certificate is already revoked",
        )

    certificate.status = schemas.CertificateStatus.revoked
    db.commit()
    db.refresh(certificate)
    return certificate
