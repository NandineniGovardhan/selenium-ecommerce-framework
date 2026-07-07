"""
test_remove_from_cart.py
---------------------------
Remove-from-cart test scenarios.
"""

import pytest

from base.base_test import BaseTest
from constants.constants import TestDataFiles
from utilities.json_reader_utility import JsonReaderUtility


@pytest.mark.usefixtures("driver")
class TestRemoveFromCart(BaseTest):

    @pytest.mark.smoke
    @pytest.mark.cart
    def test_remove_single_item_from_cart(self):
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

        pages.home_page.click_cart_icon()
        pages.cart_page.remove_item(product["name"])

        self.assertions.assert_true(
            pages.cart_page.is_cart_empty(),
            "Expected cart to be empty after removing the only item",
        )

    @pytest.mark.regression
    @pytest.mark.cart
    def test_removing_one_of_multiple_items_keeps_others(self):
        product_a = JsonReaderUtility.find_record(
            TestDataFiles.PRODUCTS, "products", "product_id", "P1001"
        )
        product_b = JsonReaderUtility.find_record(
            TestDataFiles.PRODUCTS, "products", "product_id", "P1002"
        )
        pages = self.get_pages()

        for product in (product_a, product_b):
            pages.home_page.open()
            pages.home_page.search_for_product(product["name"])
            pages.search_page.click_product_by_name(product["name"])
            pages.product_page.add_to_cart(
                quantity=1,
                size=product["available_sizes"][0],
                color=product["available_colors"][0],
            )

        pages.home_page.click_cart_icon()
        pages.cart_page.remove_item(product_a["name"])

        remaining_items = pages.cart_page.get_cart_item_names()
        self.assertions.assert_not_equals(
            product_a["name"] in remaining_items, True,
            f"Expected '{product_a['name']}' to be removed from the cart",
        )
        self.assertions.assert_contains(
            remaining_items, product_b["name"],
            f"Expected '{product_b['name']}' to remain in the cart",
        )
