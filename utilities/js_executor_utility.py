"""
js_executor_utility.py
------------------------
Wraps `driver.execute_script(...)` calls used as fallbacks for elements
that resist standard Selenium interaction (overlays, custom widgets,
off-screen elements, etc.).
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from utilities.logger_utility import get_logger

log = get_logger(__name__)


class JavaScriptExecutorUtility:
    """Reusable JavaScript execution helpers."""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def click(self, element: WebElement) -> None:
        """Clicks an element via JavaScript (bypasses overlay interception)."""
        self.driver.execute_script("arguments[0].click();", element)
        log.debug("Performed JS click")

    def scroll_into_view(self, element: WebElement) -> None:
        """Scrolls the element into the center of the viewport."""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", element
        )
        log.debug("Scrolled element into view via JS")

    def set_value(self, element: WebElement, value: str) -> None:
        """Sets an input's value directly via JavaScript."""
        self.driver.execute_script(
            "arguments[0].value = arguments[1];", element, value
        )
        log.debug("Set element value via JS")

    def highlight(self, element: WebElement) -> None:
        """Adds a red border around an element (useful for debugging)."""
        self.driver.execute_script(
            "arguments[0].style.border='3px solid red';", element
        )

    def scroll_to_bottom(self) -> None:
        """Scrolls the page to the very bottom."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        log.debug("Scrolled to bottom of page")

    def scroll_to_top(self) -> None:
        """Scrolls the page to the very top."""
        self.driver.execute_script("window.scrollTo(0, 0);")
        log.debug("Scrolled to top of page")

    def get_page_load_state(self) -> str:
        """Returns document.readyState, useful for custom wait predicates."""
        return self.driver.execute_script("return document.readyState;")
