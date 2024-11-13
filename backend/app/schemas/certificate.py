from pydantic import BaseModel, UUID4, Field, field_validator
from datetime import datetime, timezone
from enum import Enum

class CertificateStatus(str, Enum):
    active = 'active'
    revoked = 'revoked'

class CertificateBase(BaseModel):
    certificate_serial_number: str = Field(max_length=100)
    certificate_fingerprint: str = Field(max_length=100)
    public_key: str
    expires_at: datetime
    status: CertificateStatus = CertificateStatus.active

class CertificateCreate(CertificateBase):
    device_id: UUID4

    @field_validator('expires_at')
    def expires_at_must_be_future(cls, v):
        # Ensure both datetime objects are timezone-aware
        if v <= datetime.now(timezone.utc):
            raise ValueError('expires_at must be a future datetime')
        return v

class Certificate(CertificateBase):
    certificate_id: int
    device_id: UUID4
    issued_at: datetime

    model_config = {
        "from_attributes": True
    }
