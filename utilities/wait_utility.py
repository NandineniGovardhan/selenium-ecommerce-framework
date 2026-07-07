"""
wait_utility.py
----------------
Centralized EXPLICIT wait helpers. The framework standard mandates explicit
waits only — time.sleep() and reliance on implicit wait for synchronization
is prohibited. Every page/action method should synchronize through here.
"""

from typing import Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config_reader import config_reader
from utilities.logger_utility import get_logger

log = get_logger(__name__)


class WaitUtility:
    """Reusable explicit-wait wrappers around Selenium's WebDriverWait."""

    def __init__(self, driver: WebDriver, timeout: int = None):
        self.driver = driver
        self.timeout = timeout or config_reader.get_explicit_wait()

    def _wait(self, timeout: int = None) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout or self.timeout)

    def wait_for_visible(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """Waits until element is present AND visible in the DOM."""
        log.debug("Waiting for element to be visible: %s", locator)
        return self._wait(timeout).until(EC.visibility_of_element_located(locator))

    def wait_for_present(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """Waits until element exists in the DOM (not necessarily visible)."""
        log.debug("Waiting for element to be present: %s", locator)
        return self._wait(timeout).until(EC.presence_of_element_located(locator))

    def wait_for_clickable(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """Waits until element is visible and enabled for interaction."""
        log.debug("Waiting for element to be clickable: %s", locator)
        return self._wait(timeout).until(EC.element_to_be_clickable(locator))

    def wait_for_invisible(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """Waits until element becomes invisible or is removed from DOM."""
        log.debug("Waiting for element to be invisible: %s", locator)
        return self._wait(timeout).until(EC.invisibility_of_element_located(locator))

    def wait_for_text_present(self, locator: Tuple[str, str], text: str,
                               timeout: int = None) -> bool:
        """Waits until the given text appears inside the element."""
        log.debug("Waiting for text '%s' in element: %s", text, locator)
        return self._wait(timeout).until(EC.text_to_be_present_in_element(locator, text))

    def wait_for_url_contains(self, fragment: str, timeout: int = None) -> bool:
        """Waits until current URL contains the given fragment."""
        log.debug("Waiting for URL to contain: %s", fragment)
        return self._wait(timeout).until(EC.url_contains(fragment))

    def wait_for_title_contains(self, title_fragment: str, timeout: int = None) -> bool:
        """Waits until page title contains the given fragment."""
        log.debug("Waiting for title to contain: %s", title_fragment)
        return self._wait(timeout).until(EC.title_contains(title_fragment))

    def wait_for_all_visible(self, locator: Tuple[str, str], timeout: int = None):
        """Waits until all matching elements are visible; returns the list."""
        log.debug("Waiting for all elements to be visible: %s", locator)
        return self._wait(timeout).until(EC.visibility_of_all_elements_located(locator))

    def wait_for_element_count(self, locator: Tuple[str, str], count: int,
                                timeout: int = None) -> bool:
        """Waits until the number of matching elements equals `count`."""
        log.debug("Waiting for %d elements matching: %s", count, locator)

        def _predicate(driver):
            return len(driver.find_elements(*locator)) == count

        return self._wait(timeout).until(_predicate)
