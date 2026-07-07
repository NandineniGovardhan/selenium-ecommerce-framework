"""
screenshot_utility.py
-----------------------
Handles screenshot capture on demand and, more importantly, automatic
capture on test failure (wired through conftest.py's pytest hook).
"""

import os

from selenium.webdriver.remote.webdriver import WebDriver

from constants.constants import SCREENSHOT_EXTENSION, SCREENSHOTS_DIR, TIMESTAMP_FORMAT
from utilities.date_utility import DateUtility
from utilities.logger_utility import get_logger

log = get_logger(__name__)


class ScreenshotUtility:
    """Reusable screenshot capture helper."""

    @staticmethod
    def capture(driver: WebDriver, test_name: str) -> str:
        """
        Captures a screenshot and saves it under /screenshots.

        Args:
            driver: Active WebDriver instance.
            test_name: Name of the test (used to build a unique filename).

        Returns:
            Absolute path to the saved screenshot file.
        """
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

        safe_name = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in test_name)
        file_name = f"{safe_name}_{DateUtility.current_timestamp()}{SCREENSHOT_EXTENSION}"
        file_path = os.path.join(SCREENSHOTS_DIR, file_name)

        try:
            driver.save_screenshot(file_path)
            log.info("Screenshot captured: %s", file_path)
        except Exception as exc:
            log.error("Failed to capture screenshot for '%s': %s", test_name, exc)
            return ""

        return file_path
