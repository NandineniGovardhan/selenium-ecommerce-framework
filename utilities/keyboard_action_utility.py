"""
keyboard_action_utility.py
-----------------------------
Helpers for keyboard interactions (e.g. pressing ENTER in a search box,
using TAB to move focus, keyboard shortcuts).
"""

from typing import Tuple

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from utilities.logger_utility import get_logger
from utilities.wait_utility import WaitUtility

log = get_logger(__name__)


class KeyboardActionUtility:
    """Reusable keyboard interaction helpers."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WaitUtility(driver)
        self.actions = ActionChains(driver)

    def press_enter(self, locator: Tuple[str, str]) -> None:
        """Sends the ENTER key to the given element."""
        element = self.wait.wait_for_visible(locator)
        element.send_keys(Keys.ENTER)
        log.debug("Pressed ENTER on element: %s", locator)

    def press_tab(self, locator: Tuple[str, str]) -> None:
        """Sends the TAB key to move focus away from the given element."""
        element = self.wait.wait_for_visible(locator)
        element.send_keys(Keys.TAB)
        log.debug("Pressed TAB on element: %s", locator)

    def press_escape(self) -> None:
        """Sends the ESCAPE key at the page/body level."""
        self.actions.send_keys(Keys.ESCAPE).perform()
        log.debug("Pressed ESCAPE")

    def select_all_and_type(self, locator: Tuple[str, str], text: str) -> None:
        """Selects existing text (Ctrl+A) and replaces it with new text."""
        element = self.wait.wait_for_visible(locator)
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(text)
        log.debug("Replaced text via select-all + type on element: %s", locator)

    def key_combo(self, *keys: str) -> None:
        """Sends an arbitrary key combination (e.g. Keys.CONTROL, 'c')."""
        self.actions.key_down(keys[0])
        for key in keys[1:]:
            self.actions.send_keys(key)
        self.actions.key_up(keys[0]).perform()
        log.debug("Sent key combo: %s", keys)
