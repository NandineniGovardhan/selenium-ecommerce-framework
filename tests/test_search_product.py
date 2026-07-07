"""
test_search_product.py
------------------------
Product search test scenarios.
"""

import pytest

from base.base_test import BaseTest
from constants.constants import TestDataFiles
from utilities.json_reader_utility import JsonReaderUtility


@pytest.mark.usefixtures("driver")
class TestSearchProduct(BaseTest):

    @pytest.mark.smoke
    @pytest.mark.search
    def test_search_returns_matching_results(self):
        product = JsonReaderUtility.find_record(
            TestDataFiles.PRODUCTS, "products", "product_id", "P1001"
        )
        pages = self.get_pages()

        pages.home_page.open()
        pages.home_page.search_for_product(product["name"])

        self.assertions.assert_greater_than(
            pages.search_page.get_result_count(), 0,
            "Expected at least one search result for a valid product name",
        )
        self.assertions.assert_contains(
            pages.search_page.get_result_titles(), product["name"],
            "Expected the searched product to appear in the results",
        )

    @pytest.mark.regression
    @pytest.mark.search
    @pytest.mark.negative
    def test_search_with_no_matching_results(self):
        pages = self.get_pages()

        pages.home_page.open()
        pages.home_page.search_for_product("zzz_nonexistent_product_zzz")

        self.assertions.assert_true(
            pages.search_page.is_no_results_message_displayed(),
            "Expected a 'no results found' message for a nonsense search term",
        )

    @pytest.mark.regression
    @pytest.mark.search
    def test_search_result_can_be_opened(self):
        product = JsonReaderUtility.find_record(
            TestDataFiles.PRODUCTS, "products", "product_id", "P1002"
        )
        pages = self.get_pages()

        pages.home_page.open()
        pages.home_page.search_for_product(product["name"])
        pages.search_page.click_product_by_name(product["name"])

        self.assertions.assert_equals(
            pages.product_page.get_product_title(), product["name"],
            "Expected product detail page title to match the selected product",
        )
