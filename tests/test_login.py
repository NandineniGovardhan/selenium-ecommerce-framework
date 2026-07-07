"""
test_login.py
---------------
Login test scenarios. Test methods contain ONLY business flow calls
(page object methods + assertions) — no locators, no raw Selenium calls.
"""

import pytest

from base.base_test import BaseTest
from constants.constants import TestDataFiles
from utilities.json_reader_utility import JsonReaderUtility


@pytest.mark.usefixtures("driver")
class TestLogin(BaseTest):

    @pytest.mark.smoke
    @pytest.mark.login
    def test_successful_login_with_valid_credentials(self):
        user = JsonReaderUtility.find_record(
            TestDataFiles.USERS, "users", "role", "standard_user"
        )
        pages = self.get_pages()

        pages.login_page.open()
        pages.login_page.login(user["username"], user["password"])

        self.assertions.assert_true(
            pages.login_page.is_login_successful(),
            "Expected user to be redirected to the logged-in home state",
        )

    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.negative
    def test_login_fails_for_locked_out_user(self):
        user = JsonReaderUtility.find_record(
            TestDataFiles.USERS, "users", "role", "locked_out_user"
        )
        pages = self.get_pages()

        pages.login_page.open()
        pages.login_page.login(user["username"], user["password"])

        self.assertions.assert_true(
            pages.login_page.is_error_message_displayed(),
            "Expected an error message for a locked-out user",
        )

    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.negative
    def test_login_fails_with_invalid_credentials(self):
        user = JsonReaderUtility.find_record(
            TestDataFiles.USERS, "users", "role", "invalid_user"
        )
        pages = self.get_pages()

        pages.login_page.open()
        pages.login_page.login(user["username"], user["password"])

        error_message = pages.login_page.get_error_message()
        self.assertions.assert_contains(
            error_message.lower(), "invalid",
            "Expected error message to mention invalid credentials",
        )
