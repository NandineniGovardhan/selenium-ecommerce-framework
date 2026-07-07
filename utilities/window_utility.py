"""
window_utility.py
-------------------
Helpers for multi-window/tab handling (e.g. payment gateways or external
links opening in a new tab during checkout flows).
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from config.config_reader import config_reader
from utilities.logger_utility import get_logger

log = get_logger(__name__)


class WindowUtility:
    """Reusable window/tab handling helpers."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.timeout = config_reader.get_explicit_wait()

    def switch_to_new_window(self, current_handles: list) -> None:
        """Waits for a new window handle to appear, then switches to it."""
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: len(d.window_handles) > len(current_handles)
        )
        new_handle = [h for h in self.driver.window_handles if h not in current_handles][0]
        self.driver.switch_to.window(new_handle)
        log.info("Switched to new window: %s", new_handle)

    def switch_to_window_by_index(self, index: int) -> None:
        """Switches to a window by its index in `window_handles`."""
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[index])
        log.info("Switched to window at index %d", index)

    def close_current_and_switch_back(self, original_handle: str) -> None:
        """Closes the active window and switches back to the given handle."""
        self.driver.close()
        self.driver.switch_to.window(original_handle)
        log.info("Closed current window, switched back to: %s", original_handle)

    def get_current_handle(self) -> str:
        """Returns the handle of the currently active window."""
        return self.driver.current_window_handle

    def get_all_handles(self) -> list:
        """Returns all open window handles."""
        return self.driver.window_handles
