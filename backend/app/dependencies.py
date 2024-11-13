# app/dependencies.py

from dotenv import load_dotenv
import os

from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
import base64
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from .database import get_db
from . import models, schemas
from app.schemas.certificate import CertificateStatus

# Load environment variables from .env.prod file
load_dotenv()

API_KEY = os.getenv("CERT_API_KEY")

def internal_only(request: Request):
    api_key = request.headers.get("X-API-KEY")
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden"
        )

def get_client_certificate(request: Request):
    client_cert_header = request.headers.get("X-Client-Cert")
    if not client_cert_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Client certificate is required"
        )

    # Decode and parse the certificate
    try:
        # Remove headers if present and decode the certificate from Base64
        cert_base64 = client_cert_header.replace("-----BEGIN CERTIFICATE-----", "").replace("-----END CERTIFICATE-----", "").replace("\n", "")
        cert_pem = base64.b64decode(cert_base64)

        # Load the certificate using PEM format
        client_cert = x509.load_pem_x509_certificate(cert_pem, default_backend())
        #cert_der = base64.b64decode(client_cert_header)
        #client_cert = x509.load_der_x509_certificate(cert_der)
        return client_cert
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid client certificate"
        )

def verify_client_certificate(
    cert: x509.Certificate,
    db: Session = Depends(get_db)
):
    # Extract device identifier from the certificate
    # For example, from the Common Name (CN) field
    subject = cert.subject
    cn_attributes = subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)
    if not cn_attributes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Certificate does not contain a Common Name (CN)"
        )
    device_id  = cn_attributes[0].value

    # Convert the integer serial number to a hexadecimal string
    cert_serial_hex = hex(cert.serial_number)[2:].upper()  # Strip '0x' prefix and convert to uppercase

    # Query the database for a matching certificate
    db_certificate = db.query(models.Certificate).filter(
        models.Certificate.certificate_serial_number == str(cert_serial_hex),
        models.Certificate.status == CertificateStatus.active,
    models.Certificate.device_id == device_id
    ).first()

    if not db_certificate:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or revoked client certificate"
        )

    return db_certificate.device_id  # Return associated device ID