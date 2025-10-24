"""
Main pipeline for Klarna parser.

Coordinates scraping, data cleaning, and writing results to Google Sheets.
"""
from parser.config import logger, DOWNLOAD_DIR
from parser.tools import clean_download_folder
from .scraper import run_scraper

def run_pipeline() -> None:
    """Runs the full Klarna parsing pipeline"""
    logger.info("Starting Klarna parsing")

    # Step 1: Clean download folder
    clean_download_folder(DOWNLOAD_DIR)
    logger.info("Download folder cleaned")

    # Setp 2: Download csv file from Klarna
    run_scraper()
    logger.info("Download csv file from Klarna")