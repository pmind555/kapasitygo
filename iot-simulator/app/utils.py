# utils.py

import logging

def configure_logging():
    logging.basicConfig(
        filename='device.log',  # Log file name
        level=logging.INFO,  # Log level
        format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
        datefmt='%Y-%m-%d %H:%M:%S'  # Date format in log
    )

    # Add console logging handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(console_formatter)
    logging.getLogger().addHandler(console_handler)
