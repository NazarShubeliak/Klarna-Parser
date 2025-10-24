"""
Handles locating and parsing Klarna CSV files.
"""
import os
import csv
from parser.config import DOWNLOAD_DIR, logger

def get_csv_file() -> str:
    """Returns the most recently modified CSV file in the folder."""
    files = [os.path.join(DOWNLOAD_DIR, f) for f in os.listdir(DOWNLOAD_DIR)]
    files = [f for f in files if os.path.isfile(f)]
    latest_file = max(files, key=os.path.getctime)

    if not latest_file:
        logger.error("File not found in:", DOWNLOAD_DIR)
        raise FileNotFoundError("File not found in:", DOWNLOAD_DIR)
    
    logger.info("Found latest CSV:", latest_file)
    return latest_file

def parse_csv_file() -> list[str]:
    """Parses the given CSV file into python list."""
    csv_file = get_csv_file()
    with open(csv_file, newline="") as f:
        reader = csv.reader(f, delimiter=";")
        return_rows = [row for row in reader if row[0] == "RETURN"]

    if not return_rows:
        logger.error("Failed to parse CSV:", csv_file)
        raise

    logger.info(f"Parsed CSV with {len(return_rows)} rows")
    return return_rows