"""
conftest.py
------------
Root pytest configuration. This is the ONLY place where:
    * Custom CLI options are registered (--env, --browser, --headless)
    * The `driver` fixture (setup/teardown of WebDriver) is defined
    * The failure-screenshot pytest hook is wired up

Test classes/modules never create a WebDriver directly; they always
receive one through the `driver` fixture.
"""

import os

import pytest

from base.driver_factory import DriverFactory
from config.config_reader import config_reader
from constants.constants import Environments
from utilities.logger_utility import get_logger
from utilities.screenshot_utility import ScreenshotUtility

log = get_logger(__name__)


# --------------------------------------------------------------------- #
# CLI options
# --------------------------------------------------------------------- #
def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="Environment to run tests against: qa | dev | prod "
             "(overrides config.ini default)",
    )
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        help="Browser to run tests on: chrome | firefox | edge "
             "(overrides config.ini default)",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run the browser in headless mode",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Applies CLI overrides to the singleton ConfigReader before any test runs."""
    env = config.getoption("--env")
    browser = config.getoption("--browser")
    headless = config.getoption("--headless")

    if env:
        if env.lower() not in Environments.ALL:
            raise ValueError(f"Invalid --env '{env}'. Must be one of {Environments.ALL}")
        config_reader.set_environment(env.lower())
        os.environ["FRAMEWORK_ENV"] = env.lower()

    if browser:
        config_reader.set_browser(browser.lower())
        os.environ["FRAMEWORK_BROWSER"] = browser.lower()

    if headless:
        os.environ["FRAMEWORK_HEADLESS"] = "true"

    log.info(
        "Test run configured | environment=%s | browser=%s | headless=%s",
        config_reader.get_environment(), config_reader.get_browser(),
        config_reader.get_headless() or headless,
    )


# --------------------------------------------------------------------- #
# Driver fixture — function-scoped so every test gets an isolated browser
# --------------------------------------------------------------------- #
@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest):
    """
    Creates a fresh WebDriver for each test function and guarantees teardown
    even if the test fails or raises.
    """
    log.info("========== SETUP: %s ==========", request.node.name)
    web_driver = DriverFactory.create_driver()

    # Expose the driver on the test instance so BaseTest.get_pages() works
    request.instance.driver = web_driver

    yield web_driver

    log.info("========== TEARDOWN: %s ==========", request.node.name)
    web_driver.quit()


# --------------------------------------------------------------------- #
# Automatic screenshot capture on failure
# --------------------------------------------------------------------- #
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    """
    Hooks into pytest's reporting to capture a screenshot the moment a test
    fails, and attaches it to the pytest-html report automatically.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed and config_reader.get_screenshot_on_failure():
        test_instance = getattr(item, "instance", None)
        web_driver = getattr(test_instance, "driver", None)

        if web_driver is not None:
            screenshot_path = ScreenshotUtility.capture(web_driver, item.name)

            if screenshot_path and hasattr(item.config, "_html"):
                # Embed screenshot inline into the pytest-html report
                extra = getattr(report, "extra", [])
                try:
                    from pytest_html import extras
                    extra.append(extras.image(screenshot_path))
                    report.extra = extra
                except ImportError:
                    log.debug("pytest-html not available for inline image embedding")
