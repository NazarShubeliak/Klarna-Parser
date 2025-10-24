"""
Handles downloading Klarna CSV report.
"""

from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from parser.config import logger

def download_csv(driver: WebDriver):
    """Clicks the download button to retrieve Klarna CSV report."""
    wait = WebDriverWait(driver, 15)
    try:
        download_button = wait.until(EC.element_to_be_clickable((By.ID, "BatchReportButtonGroup__download-csv__button__text")))
        download_button.click()
        sleep(4)
        logger.info("CSV download initiated")
    except Exception as e:
        logger.error(f"Failed to click download button {e}")
        raise
