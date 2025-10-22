"""
Configuration module for Klarna parser.

Loads environment variables and defines constants used across the project.
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options

# Mode
DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "false").lower() == "true"

# Load environment variable from .env file
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# General path
DOWNLOAD_DIR: Path = BASE_DIR / os.getenv("DOWNLOAD_DIR", "klarna_csv")
LOG_DIR: Path = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Google Sheet
GOOGLE_SHEET_NAME: str = os.getenv("GOOGLE_SHEET_NAME", "")
GOOGLE_SHEET_WORKSHEET_NAME: str = os.getenv(
    "GOOGLE_SHEET_WORKSHEET_NAME", "Klarna Refunded"
)

# Email credentials
EMAIL_ADDRESS: str = os.getenv("EMAIL_ADDRESS", "")
EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "")

# Klarna URL
URL: str = os.getenv("KLARNA_URL", "")

# Date format
DATE_FORMAT = "%Y-%m-%d"

# Selenium setting
CHROME_OPTIONS = Options()
CHROME_OPTIONS.add_experimental_option("prefs", {"download.default_directory": str(DOWNLOAD_DIR)})

if not DEBUG_MODE:
    # Production mode
    CHROME_OPTIONS.add_argument("--headless")    
    CHROME_OPTIONS.add_argument("--disable-gpu")    
    CHROME_OPTIONS.add_argument("--window-size=1920,1080")    
else:
    # Debug mode
    CHROME_OPTIONS.add_argument("--start-maximized")

# Logging configuration
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_FILE: Path = LOG_DIR / "klarna_parser.log"

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("klarna_parser")