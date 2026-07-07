"""
base_page.py
-------------
Parent class for every Page Object in the framework.

Responsibilities:
    * Hold the shared WebDriver reference
    * Expose ready-to-use utility instances (actions, waits, dropdowns,
      alerts, windows, mouse, keyboard, JS executor) so page classes never
      instantiate Selenium primitives themselves
    * Provide generic navigation helpers common to every page

Page classes should inherit from BasePage and ONLY contain:
    * Locators (imported from pages/locators/*.py)
    * Business-meaningful methods (e.g. `login()`, `add_to_cart()`)

Page classes must NEVER contain raw `driver.find_element` calls; always
go through `self.actions`.
"""

from selenium.webdriver.remote.webdriver import WebDriver

from config.config_reader import config_reader
from utilities.alert_utility import AlertUtility
from utilities.dropdown_utility import DropdownUtility
from utilities.js_executor_utility import JavaScriptExecutorUtility
from utilities.keyboard_action_utility import KeyboardActionUtility
from utilities.logger_utility import get_logger
from utilities.mouse_action_utility import MouseActionUtility
from utilities.selenium_actions_utility import SeleniumActionsUtility
from utilities.wait_utility import WaitUtility
from utilities.window_utility import WindowUtility

log = get_logger(__name__)


class BasePage:
    """Base class every Page Object must extend."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.base_url = config_reader.get_base_url()

        # Reusable utility instances available to every page object
        self.actions = SeleniumActionsUtility(driver)
        self.wait = WaitUtility(driver)
        self.js = JavaScriptExecutorUtility(driver)
        self.dropdown = DropdownUtility(driver)
        self.alert = AlertUtility(driver)
        self.window = WindowUtility(driver)
        self.mouse = MouseActionUtility(driver)
        self.keyboard = KeyboardActionUtility(driver)

    def navigate_to(self, relative_path: str = "") -> None:
        """Navigates to `base_url + relative_path`."""
        url = f"{self.base_url.rstrip('/')}/{relative_path.lstrip('/')}" if relative_path else self.base_url
        log.info("Navigating to: %s", url)
        self.driver.get(url)

    def get_current_url(self) -> str:
        """Returns the browser's current URL."""
        return self.driver.current_url

    def get_page_title(self) -> str:
        """Returns the browser's current page title."""
        return self.driver.title

    def refresh_page(self) -> None:
        """Refreshes the current page."""
        log.info("Refreshing page")
        self.driver.refresh()

    def go_back(self) -> None:
        """Navigates back in browser history."""
        self.driver.back()

    def go_forward(self) -> None:
        """Navigates forward in browser history."""
        self.driver.forward()
