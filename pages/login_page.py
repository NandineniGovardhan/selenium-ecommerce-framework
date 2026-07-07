"""
login_page.py
---------------
Page Object for the Login page. Contains ONLY business-meaningful methods;
all locators live in pages/locators/login_locators.py and all raw Selenium
calls are delegated to self.actions (SeleniumActionsUtility).
"""

from base.base_page import BasePage
from pages.locators.login_locators import LoginPageLocators
from utilities.logger_utility import get_logger

log = get_logger(__name__)


class LoginPage(BasePage):
    """Encapsulates all interactions available on the Login page."""

    def open(self) -> "LoginPage":
        """Navigates directly to the login page."""
        self.navigate_to("login")
        return self

    def enter_username(self, username: str) -> "LoginPage":
        self.actions.type_text(LoginPageLocators.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        self.actions.type_text(LoginPageLocators.PASSWORD_INPUT, password)
        return self

    def click_login_button(self) -> None:
        self.actions.click(LoginPageLocators.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        """Performs a complete login using the given credentials."""
        log.info("Logging in with username: %s", username)
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def get_error_message(self) -> str:
        """Returns the visible login error message text, if any."""
        return self.actions.get_text(LoginPageLocators.ERROR_MESSAGE)

    def is_error_message_displayed(self) -> bool:
        return self.actions.is_displayed(LoginPageLocators.ERROR_MESSAGE)

    def is_login_successful(self) -> bool:
        """Returns True once the logged-in user menu becomes visible."""
        return self.actions.is_displayed(LoginPageLocators.LOGGED_IN_USER_MENU, timeout=10)
