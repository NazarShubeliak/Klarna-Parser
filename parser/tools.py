"""
Utility functions for Klarna parser.

Includes helpers for file system cleanup, validation, and formatting.
"""

import os
from typing import Tuple
from datetime import datetime, timedelta
from pathlib import Path

from parser.config import logger, DATE_FORMAT


def clean_download_folder(folder_path: Path) -> None:
    """
    Removes all files from the specified download folder.

    Args:
        folder_path (Path): Path to the folder to be cleaned.
    """
    if not folder_path.exists():
        logger.error(f"Error not found: {folder_path}")
        raise FileNotFoundError(f"Error not found: {folder_path}")
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            logger.error(f"Error while deleting: {file_path}: {e}")


def get_last_7_days() -> Tuple[str, str]:
    """Get yesterday's date and the date 7 days ago"""
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    start_date = yesterday - timedelta(days=7)

    start_date_convert = start_date.strftime(DATE_FORMAT)
    end_date_convert = yesterday.strftime(DATE_FORMAT)

    return start_date_convert, end_date_convert
