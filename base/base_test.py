"""
base_test.py
-------------
Parent class for every test class in /tests.

Responsibilities:
    * Expose the active `self.driver` (injected via the `driver` pytest
      fixture defined in conftest.py)
    * Provide convenient page-object instantiation
    * Centralize any behavior every single test class should share

NOTE: Driver creation/teardown itself lives in conftest.py fixtures, NOT
here, since pytest fixtures (not plain base-class setup/teardown) are the
framework standard for resource lifecycle management. BaseTest simply
gives test classes a consistent, typed way to access that fixture-managed
driver plus shared helpers.
"""

from selenium.webdriver.remote.webdriver import WebDriver

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.search_page import SearchPage
from utilities.assertion_utility import AssertionUtility
from utilities.logger_utility import get_logger

log = get_logger(__name__)


class BaseTest:
    """Base class every test class should extend."""

    driver: WebDriver

    def get_pages(self):
        """
        Returns a simple namespace-like object exposing every page object,
        already wired to the current test's driver instance.

        Usage inside a test:
            pages = self.get_pages()
            pages.login_page.login(username, password)
        """
        return _PageRegistry(self.driver)

    @property
    def assertions(self) -> AssertionUtility:
        """Shorthand access to the reusable assertion utility."""
        return AssertionUtility()


class _PageRegistry:
    """Lazily instantiates and caches page objects for a single test."""

    def __init__(self, driver: WebDriver):
        self._driver = driver
        self._cache = {}

    def _get(self, cls):
        if cls not in self._cache:
            self._cache[cls] = cls(self._driver)
        return self._cache[cls]

    @property
    def login_page(self) -> LoginPage:
        return self._get(LoginPage)

    @property
    def home_page(self) -> HomePage:
        return self._get(HomePage)

    @property
    def search_page(self) -> SearchPage:
        return self._get(SearchPage)

    @property
    def product_page(self) -> ProductPage:
        return self._get(ProductPage)

    @property
    def cart_page(self) -> CartPage:
        return self._get(CartPage)

    @property
    def checkout_page(self) -> CheckoutPage:
        return self._get(CheckoutPage)
