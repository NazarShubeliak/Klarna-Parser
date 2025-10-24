"""
Handles browser setup and cookie acceptance for Klarna scraping.
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from parser.config import logger, CHROME_OPTIONS

def create_driver() -> webdriver.Chrome:
    """Initializes and returns a Chrome WebDriver instance."""
    logger.info("Launching Chrome browser")
    driver = webdriver.Chrome(options=CHROME_OPTIONS)
    return driver

def accept_cookies(wait: WebDriverWait) -> None:
    """Accepts Klarna's cookie banner if present."""
    try:
        cookie_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
        cookie_button.click()
        logger.info("Cookies accepted")
    except Exception as e:
        logger.error("Cookies banner not found", e)
        raise e