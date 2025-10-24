"""
Handles retrieving Klarna OTP code from email via IMAP.
"""

import imaplib
import os
import email
import re
from parser.config import logger

def get_klarna_code() -> str:
    """Connects to email via IMAP and extracts Klarna OTP code from the latest message."""
    IMAP_SERVER = os.getenv("IMAP_SERVER")
    IMAP_PORT = os.getenv("IMAP_PORT")
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    logger.debug(f"Connect to EMAIL:{EMAIL_ADDRESS} using PASSWORD:{EMAIL_PASSWORD} by {IMAP_SERVER}:{IMAP_PORT}")
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        logger.info("Connected and logged to email in successfully")
    except Exception as e:
        logger.error(f"Connection failed: {e}")
        raise

    mail.select("Inbox")
    status, message = mail.search(None, 'FROM "noreply-uk@klarna.co.uk"')
    if status != "OK" or not message[0]:
        logger.error("Klarna email not found")
        raise ValueError("Klarna email not found")
    
    email_ids = message[0].split()

    for eid in reversed(email_ids):
        status, data = mail.fetch(eid, "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        logger.debug("Extract code from body")
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()
        match = re.search(r"\b(\d{6})\b.*?(?:is your 6-digit code|your 6-digit code is)", body, re.IGNORECASE)
        if match:
            code = match.group(1)
            logger.debug(f"Found code: {code}")
            return code

        logger.error(f"Not found code")
        raise ValueError("Not found code")