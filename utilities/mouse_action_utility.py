"""
mouse_action_utility.py
--------------------------
Helpers built on Selenium's ActionChains for mouse-based interactions:
hover menus (e.g. category mega-menus), drag-and-drop, double-click,
and right-click context menus.
"""

from typing import Tuple

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver

from utilities.logger_utility import get_logger
from utilities.wait_utility import WaitUtility

log = get_logger(__name__)


class MouseActionUtility:
    """Reusable ActionChains-based mouse interaction helpers."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WaitUtility(driver)
        self.actions = ActionChains(driver)

    def hover(self, locator: Tuple[str, str]) -> None:
        """Moves the mouse over the given element (e.g. to reveal a menu)."""
        element = self.wait.wait_for_visible(locator)
        self.actions.move_to_element(element).perform()
        log.debug("Hovered over element: %s", locator)

    def double_click(self, locator: Tuple[str, str]) -> None:
        """Performs a double-click on the given element."""
        element = self.wait.wait_for_clickable(locator)
        self.actions.double_click(element).perform()
        log.info("Double-clicked element: %s", locator)

    def right_click(self, locator: Tuple[str, str]) -> None:
        """Performs a right-click (context click) on the given element."""
        element = self.wait.wait_for_visible(locator)
        self.actions.context_click(element).perform()
        log.info("Right-clicked element: %s", locator)

    def drag_and_drop(self, source_locator: Tuple[str, str],
                       target_locator: Tuple[str, str]) -> None:
        """Drags an element from source and drops it onto target."""
        source = self.wait.wait_for_visible(source_locator)
        target = self.wait.wait_for_visible(target_locator)
        self.actions.drag_and_drop(source, target).perform()
        log.info("Dragged element %s onto %s", source_locator, target_locator)

    def click_and_hold(self, locator: Tuple[str, str]) -> None:
        """Presses and holds the mouse button on the given element."""
        element = self.wait.wait_for_visible(locator)
        self.actions.click_and_hold(element).perform()
        log.debug("Clicked and held element: %s", locator)
