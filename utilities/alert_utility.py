"""
alert_utility.py
------------------
Helpers for handling native JavaScript alerts/confirms/prompts
(e.g. "Remove item from cart?" confirmation dialogs).
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config_reader import config_reader
from utilities.logger_utility import get_logger

log = get_logger(__name__)


class AlertUtility:
    """Reusable native-alert handling helpers."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.timeout = config_reader.get_explicit_wait()

    def accept_alert(self) -> str:
        """Waits for an alert, accepts it, and returns its text."""
        alert = WebDriverWait(self.driver, self.timeout).until(EC.alert_is_present())
        text = alert.text
        alert.accept()
        log.info("Accepted alert with text: '%s'", text)
        return text

    def dismiss_alert(self) -> str:
        """Waits for an alert, dismisses it, and returns its text."""
        alert = WebDriverWait(self.driver, self.timeout).until(EC.alert_is_present())
        text = alert.text
        alert.dismiss()
        log.info("Dismissed alert with text: '%s'", text)
        return text

    def get_alert_text(self) -> str:
        """Waits for an alert and returns its text without dismissing it."""
        alert = WebDriverWait(self.driver, self.timeout).until(EC.alert_is_present())
        return alert.text

    def send_text_to_prompt(self, text: str) -> None:
        """Waits for a prompt-type alert and types text into it, then accepts."""
        alert = WebDriverWait(self.driver, self.timeout).until(EC.alert_is_present())
        alert.send_keys(text)
        alert.accept()
        log.info("Sent text '%s' to prompt and accepted", text)

    def is_alert_present(self) -> bool:
        """Returns True if a native alert is currently present."""
        try:
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            return True
        except Exception:
            return False
