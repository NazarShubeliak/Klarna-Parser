"""
Handles writing parsed Klarna data to Google Sheets.
"""

from functools import  wraps
from typing import Any, Callable
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from parser.config import GOOGLE_TOKEN_NAME, logger

def require_rows(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self, worksheet_name: str, rows: list[list[Any]], *args, **kwargs):
        if not rows:
            logger.error(f"No data passed to {func.__name__} for worksheet: {worksheet_name}")
            raise TypeError("Missing rows")
        return func(self, worksheet_name, rows, *args, **kwargs)
    return wrapper

class SheetService:
    """
    Encapsulates Google Sheets operations: authorization, reading, clearing, appending, and replacing data.
    """

    def __init__(self, sheet_name: str, creds_path: str) -> None:
        """
        Initializes the SheetService with a target spreadsheet.

        Args:
            sheet_name (str): The name of the Google Spreadsheet to open.
            creds_path (str): Path to the service account credentials JSON file.
        """
        self.sheet_name = sheet_name
        self.creds_path = creds_path
        self.client = self.__authorize()
        self.sheet = self.client.open(sheet_name)

    def __authorize(self) -> gspread.Client:
        """
        Authorizes and returns a gspread client using service account credentials.

        Returns:
            gspread.Client: Authorized client for interacting with Google Sheets.
        """
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_TOKEN_NAME, scope)
        client = gspread.authorize(creds)
        logger.debug("Authorize complete")

        return client

    def get_worksheet(self, worksheet_name: str) -> gspread.Worksheet:
        """
        Returns a specific worksheet by name.

        Args:
            name (str): The name of the worksheet tab.

        Returns:
            gspread.Worksheet: The worksheet object.
        """
        return self.sheet.worksheet(worksheet_name)

    def clear_range(self, worksheet_name: str, start_row: int = 2, end_col: str = "Z") -> None:
        """
        Clears a rectangular range in the worksheet, typically used to remove old data.

        Args:
            worksheet (str): Worksheet tab name.
            start_row (int): Row to start clearing from (default is 2 to preserve headers).
            end_col (str): Last column to clear (default is 'Z').
        """
        ws = self.get_worksheet(worksheet_name)
        row_count = len(ws.get_values()) 
        if row_count > 1:
            clear_range = f"A{start_row}:{end_col}{row_count}"
            ws.batch_clear([clear_range])
            logger.info(f"Cleared range: {clear_range} in {worksheet_name}")
        else:
            logger.info(f"Nothing to clear in {worksheet_name}")

    @require_rows
    def append_rows(self, worksheet_name: str, rows: list[list[Any]]) -> None:
        """
        Appends rows to the end of the worksheet.

        Args:
            worksheet (str): Worksheet tab name.
            rows (list[list[Any]]): List of rows to append, each row is a list of cell values.
        """
        ws = self.get_worksheet(worksheet_name)
        last_row = len(ws.get_all_values())
        ws.update(f"A{last_row + 1}", rows)
        logger.info(f"Appended {len(rows)} rows to {worksheet_name}")

    @require_rows
    def replace_rows(self, worksheet_name: str, rows: list[list[Any]], start_row: int, start_col: str = "A", end_col: str = "Z") -> None:
        """
        Replaces a range of rows in the worksheet, starting from a given row.

        Args:
            worksheet (str): Worksheet tab name.
            rows (list[list[Any]]): List of rows to write.
            start_row (int): Row number to start replacing from (default is 2).
            star_col (str): First column to replace (default is 'A').
            end_col (str): Last column to replace (default is 'Z').
        """
        ws = self.get_worksheet(worksheet_name)
        end_row = start_row + len(rows) -1
        table_range = f"{start_col}{start_row}:{end_col}{end_row}"
        ws.batch_clear(table_range)
        ws.update(f"{start_col}{start_row}", rows)
        logger.info(f"Replaced {len(rows)} rows in {worksheet_name}, range: {table_range}")



