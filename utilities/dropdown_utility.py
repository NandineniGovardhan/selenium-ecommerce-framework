"""
dropdown_utility.py
----------------------
Helpers for native <select> dropdowns (e.g. country/state selection at
checkout, product size/color selectors).
"""

from typing import List, Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select

from utilities.logger_utility import get_logger
from utilities.wait_utility import WaitUtility

log = get_logger(__name__)


class DropdownUtility:
    """Reusable helpers for native HTML <select> dropdown elements."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WaitUtility(driver)

    def select_by_visible_text(self, locator: Tuple[str, str], text: str) -> None:
        """Selects a dropdown option by its visible text."""
        element = self.wait.wait_for_visible(locator)
        Select(element).select_by_visible_text(text)
        log.info("Selected dropdown option by text '%s' on %s", text, locator)

    def select_by_value(self, locator: Tuple[str, str], value: str) -> None:
        """Selects a dropdown option by its underlying `value` attribute."""
        element = self.wait.wait_for_visible(locator)
        Select(element).select_by_value(value)
        log.info("Selected dropdown option by value '%s' on %s", value, locator)

    def select_by_index(self, locator: Tuple[str, str], index: int) -> None:
        """Selects a dropdown option by its zero-based index."""
        element = self.wait.wait_for_visible(locator)
        Select(element).select_by_index(index)
        log.info("Selected dropdown option by index %d on %s", index, locator)

    def get_selected_option_text(self, locator: Tuple[str, str]) -> str:
        """Returns the currently selected option's visible text."""
        element = self.wait.wait_for_visible(locator)
        return Select(element).first_selected_option.text.strip()

    def get_all_options(self, locator: Tuple[str, str]) -> List[str]:
        """Returns the visible text of all options in the dropdown."""
        element = self.wait.wait_for_visible(locator)
        return [option.text.strip() for option in Select(element).options]
