# app/models/readings.py

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..database import Base

class Reading(Base):
    __tablename__ = 'readings'

    reading_id = Column(Integer, primary_key=True, index=True)
    device_id = Column(UUID(as_uuid=True), ForeignKey('devices.device_id'), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    fullness_level = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default='now()')

    # Relationship to Device
    device = relationship('Device', back_populates='readings')
