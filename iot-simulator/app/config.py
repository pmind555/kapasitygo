# config.py

import os
from dotenv import load_dotenv

# Load the selected .env file
load_dotenv()

# API Configuration
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

# Simulation Parameters
POST_INTERVAL_SECONDS = int(os.getenv("POST_INTERVAL_SECONDS", "60"))
GROWTH_DURATION = int(os.getenv("GROWTH_DURATION", "600"))  # in seconds
TIME_AT_FULL = int(os.getenv("TIME_AT_FULL", "300"))  # in seconds

# Certificate path (can be passed to Device class)
CERTIFICATE_PATH = os.getenv("CERTIFICATE_PATH")
FIRMWARE_VERSION = os.getenv("FIRMWARE_VERSION", "1.0.0")  # Default to "1.0.0" if not set
