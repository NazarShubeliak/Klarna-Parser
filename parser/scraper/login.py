"""
Handles Klarna login and OTP verification.
"""

import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from parser.config import logger
from scraper.email_reader import get_klarna_code

def login_with_otp(driver: WebDriver) -> None:
    """Logs into Klarna portal and enters OTP code from email."""
    wait = WebDriverWait(driver, 15)

    # ------ Filling in login credentials
    logger.info("Filling in login credentials")
    try:
        username = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username.send_keys(os.getenv("KLARNA_LOGIN"))

        password = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password.send_keys(os.getenv("KLARNA_PASSWORD"))

        wait.until(EC.element_to_be_clickable((By.ID, "loginBtn__text"))).click()
        logger.info("Success login to Klarna")
        sleep(5)
    except Exception as e:
        logger.error(f"Error while login: {e}")
        raise 

    # ------ Switching to OTP iframe
    logger.info("Switching to OTP iframe")
    try:
        frame = driver.find_elements(By.TAG_NAME, "iframe")[2]
        driver.switch_to.frame(frame)
        driver.find_element(By.ID, "otp-intro-send-button__text").click()
        logger.info("OTP request send")
    except Exception as e:
        logger.error(f"OTP button not found: {e}")
        raise

    # ------ Get Klarna code
    logger.info("Get Klarna code")
    code = get_klarna_code()
    try:
        input_field = driver.find_element(By.TAG_NAME, "input")
        sleep(10)
        input_field.send_keys(code)
        logger.info("OTP code intered")
    except Exception as e:
        logger.error(f"Failed to enter OTP code: {e}")
        raise

    driver.switch_to.default_content()
    sleep(3)