# app/models/device.py

from sqlalchemy import Column, String, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid
from sqlalchemy.orm import relationship
from ..database import Base

class Device(Base):
    __tablename__ = 'devices'

    device_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_name = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    status = Column(String(20), default='active')
    created_at = Column(DateTime, server_default='now()')

    # Relationships
    readings = relationship('Reading', back_populates='device', cascade='all, delete-orphan')
    certificates = relationship('Certificate', back_populates='device', cascade='all, delete-orphan')
