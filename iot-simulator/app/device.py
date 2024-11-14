# device.py

import time
from datetime import datetime, timezone
import requests
import base64
import logging
from config import *
from utils import configure_logging  # Importing the logging configuration function


# Configure logging
configure_logging()


class Device:
    def __init__(self):
        try:
            # Load configuration from config.py
            self.api_url = API_URL
            self.api_key = API_KEY
            self.certificate_path = CERTIFICATE_PATH
            self.firmware_version = FIRMWARE_VERSION
            self.post_interval_seconds = POST_INTERVAL_SECONDS
            self.growth_duration = GROWTH_DURATION
            self.time_at_full = TIME_AT_FULL

            # Validate mandatory configuration
            if not all([self.api_url, self.api_key, self.certificate_path]):
                raise ValueError(
                    "Missing required configuration parameters. Ensure API_URL, API_KEY, and CERTIFICATE_PATH are set."
                )

            # Load and encode certificate
            self.certificate = self.load_certificate()

            # Initialize simulation variables
            self.fullness_level = 0
            self.state = 'increasing'  # 'increasing', 'full', 'resetting'
            self.state_start_time = time.time()

        except ValueError as ve:
            logging.error(f"Configuration Error: {ve}")
            raise

        except Exception as e:
            logging.error(f"Unexpected Error during initialization: {e}")
            raise

    def load_certificate(self):
        """
        Load the device's certificate and encode only the certificate content in base64.
        """
        try:
            if not os.path.isfile(self.certificate_path):
                raise FileNotFoundError(f"Certificate file not found: {self.certificate_path}")

            with open(self.certificate_path, 'r') as cert_file:
                cert_content = cert_file.read()

                # Encode the core content in base64
                return base64.b64encode(cert_content.encode()).decode('utf-8')

        except FileNotFoundError as fnf_error:
            logging.error(f"File Error: {fnf_error}")
            raise

        except Exception as e:
            logging.error(f"Unexpected Error while loading certificate: {e}")
            raise

    def update_fullness_level(self):
        try:
            current_time = time.time()
            if self.state == 'increasing':
                elapsed_time = current_time - self.state_start_time
                progress = min(elapsed_time / self.growth_duration, 1.0)
                # Linear growth
                self.fullness_level = int(progress * 100)
                if progress >= 1.0:
                    self.state = 'full'
                    self.state_start_time = current_time
            elif self.state == 'full':
                elapsed_time = current_time - self.state_start_time
                if elapsed_time >= self.time_at_full:
                    self.state = 'resetting'
                    self.state_start_time = current_time
            elif self.state == 'resetting':
                self.fullness_level = 0
                self.state = 'increasing'
                self.state_start_time = current_time

        except Exception as e:
            logging.error(f"Unexpected Error during fullness level update: {e}")

    def get_reading(self):
        try:
            self.update_fullness_level()
            timestamp = datetime.now(timezone.utc).isoformat()
            return timestamp, self.fullness_level
        except Exception as e:
            logging.error(f"Unexpected Error while getting reading: {e}")
            raise

    def send_reading(self, timestamp, fullness_level):
        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key,
            "X-Client-Cert": self.certificate
        }
        data = {
            "timestamp": timestamp,
            "fullness_level": fullness_level
        }

        try:
            response = requests.post(
                self.api_url,
                json=data,
                headers=headers,
                timeout=10  # seconds
            )

            if response.status_code in (200, 201):
                logging.info(f"Successfully posted reading to {self.api_url} with data: {data}")
            else:
                logging.error(f"Failed to post reading to {self.api_url}: {response.status_code} {response.text}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Network Error while posting reading to {self.api_url}: {e}")
            raise

    def run(self):
        while True:
            try:
                timestamp, fullness_level = self.get_reading()
                self.send_reading(timestamp, fullness_level)
                time.sleep(self.post_interval_seconds)
            except Exception as e:
                logging.error(f"Unexpected Error during run loop: {e}")
                time.sleep(self.post_interval_seconds)  # Retry after sleep in case of an error


