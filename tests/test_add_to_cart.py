"""
test_add_to_cart.py
----------------------
Add-to-cart test scenarios.
"""

import pytest

from base.base_test import BaseTest
from constants.constants import TestDataFiles
from utilities.json_reader_utility import JsonReaderUtility


@pytest.mark.usefixtures("driver")
class TestAddToCart(BaseTest):

    @pytest.mark.smoke
    @pytest.mark.cart
    def test_add_single_product_to_cart(self):
        product = JsonReaderUtility.find_record(
            TestDataFiles.PRODUCTS, "products", "product_id", "P1001"
        )
        pages = self.get_pages()

        pages.home_page.open()
        pages.home_page.search_for_product(product["name"])
        pages.search_page.click_product_by_name(product["name"])
        pages.product_page.add_to_cart(
            quantity=1,
            size=product["available_sizes"][0],
            color=product["available_colors"][0],
        )

        self.assertions.assert_true(
            pages.product_page.is_add_to_cart_confirmation_displayed(),
            "Expected an add-to-cart confirmation toast to appear",
        )

        pages.home_page.click_cart_icon()
        self.assertions.assert_contains(
            pages.cart_page.get_cart_item_names(), product["name"],
            "Expected the added product to appear in the cart",
        )

    @pytest.mark.regression
    @pytest.mark.cart
    def test_add_multiple_quantity_updates_cart_count(self):
        product = JsonReaderUtility.find_record(
            TestDataFiles.PRODUCTS, "products", "product_id", "P1002"
        )
        pages = self.get_pages()

        pages.home_page.open()
        pages.home_page.search_for_product(product["name"])
        pages.search_page.click_product_by_name(product["name"])
        pages.product_page.add_to_cart(
            quantity=3,
            size=product["available_sizes"][0],
            color=product["available_colors"][0],
        )

        self.assertions.assert_equals(
            pages.home_page.get_cart_item_count(), 3,
            "Expected cart badge to reflect the quantity added",
        )

    @pytest.mark.regression
    @pytest.mark.cart
    @pytest.mark.negative
    def test_out_of_stock_product_cannot_be_added(self):
        product = JsonReaderUtility.find_record(
            TestDataFiles.PRODUCTS, "products", "product_id", "P1003"
        )
        pages = self.get_pages()

        pages.home_page.open()
        pages.home_page.search_for_product(product["name"])
        pages.search_page.click_product_by_name(product["name"])

        self.assertions.assert_true(
            pages.product_page.is_out_of_stock(),
            "Expected product to be marked out of stock",
        )
