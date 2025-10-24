"""
Coordinates Klarna scraping workflow.
"""

from selenium.webdriver.support.ui import WebDriverWait
from parser.tools import get_last_7_days, clean_download_folder
from parser.config import URL, logger, DOWNLOAD_DIR
from scraper.browser import create_driver, accept_cookies
from scraper.login import login_with_otp
from scraper.downloader import download_csv

def run_scraper() -> None:
    """Executes the full Klarna scraping process."""
    start_date, end_date = get_last_7_days()
    url = f"{URL}?start_date={start_date}&end_date={end_date}"

    logger.info("Starting Klarna scraping")
    clean_download_folder(DOWNLOAD_DIR)

    driver = create_driver()
    driver.get(url)

    login_with_otp(driver)
    accept_cookies(WebDriverWait(driver, 15))
    download_csv(driver)

    driver.quit()
    logger.info("Klarna scraping completed") 