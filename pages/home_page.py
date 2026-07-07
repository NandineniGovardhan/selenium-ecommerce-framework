"""
home_page.py
--------------
Page Object for the Home page (search bar, header navigation, cart badge,
login/logout entry points).
"""

from base.base_page import BasePage
from pages.locators.home_locators import HomePageLocators
from utilities.logger_utility import get_logger

log = get_logger(__name__)


class HomePage(BasePage):
    """Encapsulates all interactions available on the Home page."""

    def open(self) -> "HomePage":
        """Navigates to the site's home page."""
        self.navigate_to("")
        return self

    def search_for_product(self, product_name: str) -> None:
        """Types a product name into the search bar and submits it."""
        log.info("Searching for product: %s", product_name)
        self.actions.type_text(HomePageLocators.SEARCH_INPUT, product_name)
        self.actions.click(HomePageLocators.SEARCH_SUBMIT_BUTTON)

    def click_login_link(self) -> None:
        self.actions.click(HomePageLocators.LOGIN_LINK)

    def click_logout_link(self) -> None:
        log.info("Logging out current user")
        self.actions.click(HomePageLocators.LOGOUT_LINK)

    def click_cart_icon(self) -> None:
        self.actions.click(HomePageLocators.CART_ICON)

    def get_cart_item_count(self) -> int:
        """Returns the number displayed on the cart badge (0 if not shown)."""
        if not self.actions.is_displayed(HomePageLocators.CART_ITEM_COUNT_BADGE, timeout=3):
            return 0
        return int(self.actions.get_text(HomePageLocators.CART_ITEM_COUNT_BADGE))

    def is_user_logged_in(self) -> bool:
        """Returns True if the account menu (visible only when logged in) is shown."""
        return self.actions.is_displayed(HomePageLocators.USER_ACCOUNT_MENU, timeout=5)

    def is_guest_banner_displayed(self) -> bool:
        """Returns True if the guest/logged-out banner is visible."""
        return self.actions.is_displayed(HomePageLocators.LOGGED_OUT_BANNER, timeout=5)
