"""
Main pipeline for Klarna parser.

Coordinates scraping, data cleaning, and writing results to Google Sheets.
"""
from parser.config import logger, DOWNLOAD_DIR

def run_pipeline() -> None:
    """Runs the full Klarna parsing pipeline"""
    logger.info("Starting Klarna parsing")
