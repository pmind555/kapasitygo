# app/main.py

from fastapi import FastAPI
from .routers import devices, readings, certificates
from .config import settings
import logging

# Set up logging based on LOG_LEVEL from settings
logging_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
logging.basicConfig(level=logging_level)
logger = logging.getLogger(__name__)

app = FastAPI()

# Include routers
app.include_router(devices.router)
app.include_router(readings.router)
app.include_router(certificates.router)

@app.get("/")
def read_root():
    logger.debug("Root endpoint was accessed.")
    return {"message": "Welcome to KapasityGO Backend API"}
