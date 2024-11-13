-- Enable the uuid-ossp extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create the devices table with UUID device_id
CREATE TABLE IF NOT EXISTS devices (
    device_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    location_name VARCHAR(100),
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the device_certificates table with UUID device_id
CREATE TABLE IF NOT EXISTS device_certificates (
    certificate_id SERIAL PRIMARY KEY,
    device_id UUID REFERENCES devices(device_id),
    certificate_serial_number VARCHAR(100) UNIQUE,
    certificate_fingerprint VARCHAR(100) UNIQUE,
    public_key TEXT,
    issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active'
);

-- Indexes for fast lookup
CREATE INDEX IF NOT EXISTS idx_certificate_serial ON device_certificates(certificate_serial_number);
CREATE INDEX IF NOT EXISTS idx_certificate_fingerprint ON device_certificates(certificate_fingerprint);

-- Create the readings table with UUID device_id
CREATE TABLE IF NOT EXISTS readings (
    reading_id SERIAL PRIMARY KEY,
    device_id UUID REFERENCES devices(device_id),
    timestamp TIMESTAMP,
    fullness_level INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);