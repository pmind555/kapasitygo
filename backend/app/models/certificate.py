# app/models/certificate.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Session
from ..database import Base
from ..schemas.certificate import CertificateStatus

class Certificate(Base):
    __tablename__ = 'device_certificates'

    certificate_id = Column(Integer, primary_key=True, index=True)
    device_id = Column(UUID(as_uuid=True), ForeignKey('devices.device_id'), nullable=False)
    certificate_serial_number = Column(String(100), unique=True, nullable=False)
    certificate_fingerprint = Column(String(100), unique=True, nullable=False)
    public_key = Column(Text, nullable=False)
    issued_at = Column(DateTime, server_default='now()')
    expires_at = Column(DateTime, nullable=False)
    status = Column(SqlEnum(CertificateStatus), default=CertificateStatus.active)

    # Relationship to Device
    device = relationship('Device', back_populates='certificates')

    @classmethod
    def get_by_serial_number(cls, serial_number: str, db: Session):
        """Query the database for a certificate by serial number."""
        return db.query(cls).filter(cls.certificate_serial_number == serial_number).first()
