"""
driver_factory.py
------------------
Single responsibility: create and configure a Selenium WebDriver instance
for the requested browser.

Why this exists as its own class (and not inside BaseTest):
    Browser creation logic (options, driver managers, headless flags) is
    complex enough that mixing it into BaseTest would violate Single
    Responsibility. DriverFactory ONLY knows how to build a driver;
    BaseTest/fixtures decide WHEN to build/destroy one.

Uses `webdriver-manager` so no browser driver binaries are ever committed
to source control or manually downloaded by engineers.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from config.config_reader import config_reader
from constants.constants import Browsers
from utilities.logger_utility import get_logger

log = get_logger(__name__)


class DriverFactory:
    """Builds a configured WebDriver instance for the requested browser."""

    @staticmethod
    def create_driver(browser: str = None) -> WebDriver:
        """
        Creates and returns a ready-to-use WebDriver.

        Args:
            browser: Optional override. Defaults to the value resolved by
                     ConfigReader (config.ini, or CLI --browser override).

        Returns:
            A configured selenium.webdriver instance.
        """
        browser_name = (browser or config_reader.get_browser()).lower().strip()
        headless = config_reader.get_headless()

        log.info("Initializing '%s' browser driver (headless=%s)", browser_name, headless)

        if browser_name == Browsers.CHROME:
            driver = DriverFactory._create_chrome_driver(headless)
        elif browser_name == Browsers.FIREFOX:
            driver = DriverFactory._create_firefox_driver(headless)
        elif browser_name == Browsers.EDGE:
            driver = DriverFactory._create_edge_driver(headless)
        else:
            log.error("Unsupported browser requested: %s", browser_name)
            raise ValueError(
                f"Unsupported browser '{browser_name}'. "
                f"Supported browsers: {Browsers.ALL}"
            )

        driver.implicitly_wait(config_reader.get_implicit_wait())
        driver.set_page_load_timeout(config_reader.get_page_load_timeout())
        driver.maximize_window()

        log.info("Driver initialized successfully for browser: %s", browser_name)
        return driver

    @staticmethod
    def _create_chrome_driver(headless: bool) -> WebDriver:
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")

        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    @staticmethod
    def _create_firefox_driver(headless: bool) -> WebDriver:
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")

        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)

    @staticmethod
    def _create_edge_driver(headless: bool) -> WebDriver:
        options = EdgeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")

        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)
