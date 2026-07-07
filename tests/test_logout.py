"""
test_logout.py
----------------
Logout test scenarios.
"""

import pytest

from base.base_test import BaseTest
from constants.constants import TestDataFiles
from utilities.json_reader_utility import JsonReaderUtility


@pytest.mark.usefixtures("driver")
class TestLogout(BaseTest):

    @pytest.mark.smoke
    @pytest.mark.login
    def test_successful_logout_after_login(self):
        user = JsonReaderUtility.find_record(
            TestDataFiles.USERS, "users", "role", "standard_user"
        )
        pages = self.get_pages()

        pages.login_page.open()
        pages.login_page.login(user["username"], user["password"])
        self.assertions.assert_true(
            pages.login_page.is_login_successful(),
            "Precondition failed: user must be logged in before logout",
        )

        pages.home_page.open()
        pages.home_page.click_logout_link()

        self.assertions.assert_true(
            pages.home_page.is_guest_banner_displayed(),
            "Expected guest banner to be visible after logout",
        )

    @pytest.mark.regression
    @pytest.mark.login
    def test_logged_out_user_cannot_access_account_menu(self):
        pages = self.get_pages()
        pages.home_page.open()

        self.assertions.assert_false(
            pages.home_page.is_user_logged_in(),
            "Expected no account menu for a guest (logged-out) session",
        )
