"""
Main pipeline for Klarna parser.

Coordinates scraping, data cleaning, and writing results to Google Sheets.
"""
from parser.config import logger, DOWNLOAD_DIR, GOOGLE_SHEET_NAME, GOOGLE_SHEET_WORKSHEET_NAME, GOOGLE_TOKEN_NAME
from parser.tools import clean_download_folder
from parser.csv_loader import parse_csv_file
from parser.sheet import SheetService
from .scraper import run_scraper

def run_pipeline() -> None:
    """Runs the full Klarna parsing pipeline"""
    logger.info("Starting Klarna parsing")

    # Step 1: Clean download folder
    clean_download_folder(DOWNLOAD_DIR)
    logger.info("Download folder cleaned")

    # Step 2: Download csv file from Klarna
    run_scraper()
    logger.info("Download csv file from Klarna")

    # Step 3: Parse csv file 
    rows = parse_csv_file()
    logger.info("Pase csv file")

    # Step 4: Write to Google Sheet
    sheet_service = SheetService(GOOGLE_SHEET_NAME, GOOGLE_TOKEN_NAME)
    sheet_service.append_rows(GOOGLE_SHEET_WORKSHEET_NAME, rows)

    logger.info("Klarna pipeline completed successfully")