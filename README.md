# Klarna Refund Parser

This project automates the process of downloading Klarna refund reports, parsing the latest CSV file, and updating Google Sheets with structured data. It is designed to support financial reporting workflows and integrate seamlessly with other platforms like Stripe and PayPal.

## Features

- ✅ Automated Klarna CSV download
- ✅ CSV parsing with validation
- ✅ Google Sheets integration via service account
- ✅ Modular architecture with clean separation of concerns
- ✅ Logging and error handling
- ✅ Append or replace data in target sheets

## Project Structure
klarna_parser/ 
├── parser/ 
│ ├── scraper.py
│ ├── csv_loader.py
│ ├── sheets.py 
│ ├── pipeline.py
│ │── config.py
│ │── tools.py  
├── run.py 

## Setup

Before running the pipeline, make sure to configure your credentials and paths in `config.py`.

## Required Configuration

Set the following values in your `.env` file or `config.py`:

### General
- `DEBUG_MODE`: `true` or `false`
- `DOWNLOAD_DIR`: Klarna CSV download folder

### Google Sheets
- `GOOGLE_SHEET_NAME`: e.g. "Order Overview"
- `GOOGLE_SHEET_WORKSHEET_NAME`: e.g. "Klarna Refunded"
- `GOOGLE_TOKEN`: path to service account JSON

### Email (IMAP)
- `IMAP_SERVER`: e.g. "imaps.udag.de"
- `IMAP_PORT`: e.g. `993`
- `EMAIL_ADDRESS`: your email
- `EMAIL_PASSWORD`: your email password

### Klarna
- `KLARNA_LOGIN`: Klarna email
- `KLARNA_PASSWORD`: Klarna password
- `KLARNA_URL`: Klarna report URL

### Logging
- `LOG_LEVEL`: e.g. `DEBUG`


1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
3. python run.py