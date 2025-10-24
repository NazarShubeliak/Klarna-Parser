"""
Scraper package for automating Klarna portal interaction.

Includes modules for:
- browser setup and cookie handling
- login and OTP verification
- CSV report downloading
- orchestration of the full scraping flow
"""
from .scraper import run_scraper