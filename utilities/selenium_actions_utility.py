"""
selenium_actions_utility.py
-----------------------------
The single place where raw Selenium element interactions happen. Page
objects call INTO this class rather than calling driver.find_element(...)
directly, which:
    * Centralizes explicit-wait synchronization before every action
    * Centralizes logging of every UI interaction
    * Makes it trivial to add retry/self-healing behavior later
    * Keeps Selenium API calls out of test scripts entirely
"""

from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from utilities.js_executor_utility import JavaScriptExecutorUtility
from utilities.logger_utility import get_logger
from utilities.wait_utility import WaitUtility

log = get_logger(__name__)


class SeleniumActionsUtility:
    """Reusable, synchronized wrappers around common Selenium interactions."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WaitUtility(driver)
        self.js = JavaScriptExecutorUtility(driver)

    def click(self, locator: Tuple[str, str]) -> None:
        """Waits for an element to be clickable, then clicks it."""
        element = self.wait.wait_for_clickable(locator)
        try:
            element.click()
        except Exception:
            log.warning("Standard click failed for %s, falling back to JS click", locator)
            self.js.click(element)
        log.info("Clicked element: %s", locator)

    def type_text(self, locator: Tuple[str, str], text: str, clear_first: bool = True) -> None:
        """Waits for visibility, optionally clears, then types text."""
        element = self.wait.wait_for_visible(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        log.info("Typed text into element %s", locator)

    def get_text(self, locator: Tuple[str, str]) -> str:
        """Waits for visibility and returns the element's visible text."""
        element = self.wait.wait_for_visible(locator)
        text = element.text.strip()
        log.debug("Fetched text from %s -> '%s'", locator, text)
        return text

    def get_attribute(self, locator: Tuple[str, str], attribute: str) -> str:
        """Waits for presence and returns the requested attribute value."""
        element = self.wait.wait_for_present(locator)
        value = element.get_attribute(attribute)
        log.debug("Fetched attribute '%s' from %s -> '%s'", attribute, locator, value)
        return value

    def is_displayed(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """Returns True if element becomes visible within timeout, else False."""
        try:
            self.wait.wait_for_visible(locator, timeout=timeout)
            return True
        except Exception:
            return False

    def is_enabled(self, locator: Tuple[str, str]) -> bool:
        """Returns True if element is present and enabled."""
        element = self.wait.wait_for_present(locator)
        return element.is_enabled()

    def find(self, locator: Tuple[str, str]) -> WebElement:
        """Waits for presence and returns the raw WebElement (escape hatch)."""
        return self.wait.wait_for_present(locator)

    def find_all(self, locator: Tuple[str, str]):
        """Waits for visibility of at least one match and returns all matches."""
        return self.wait.wait_for_all_visible(locator)

    def clear(self, locator: Tuple[str, str]) -> None:
        """Waits for visibility and clears the element's current value."""
        element = self.wait.wait_for_visible(locator)
        element.clear()
        log.debug("Cleared element: %s", locator)

    def submit(self, locator: Tuple[str, str]) -> None:
        """Waits for presence and submits a form element."""
        element = self.wait.wait_for_present(locator)
        element.submit()
        log.info("Submitted form via element: %s", locator)
