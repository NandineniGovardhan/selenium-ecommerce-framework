"""
test_checkout.py
------------------
End-to-end checkout / order placement test scenarios.
"""

import pytest

from base.base_test import BaseTest
from constants.constants import TestDataFiles
from utilities.json_reader_utility import JsonReaderUtility


@pytest.mark.usefixtures("driver")
class TestCheckout(BaseTest):

    @pytest.mark.smoke
    @pytest.mark.checkout
    def test_successful_checkout_with_valid_details(self):
        order = JsonReaderUtility.find_record(
            TestDataFiles.ORDERS, "orders", "order_reference", "ORD-DEMO-0001"
        )
        product = JsonReaderUtility.find_record(
            TestDataFiles.PRODUCTS, "products", "product_id", order["product_id"]
        )
        address = JsonReaderUtility.find_record(
            TestDataFiles.ADDRESSES, "addresses", "label", order["address_label"]
        )
        pages = self.get_pages()

        pages.home_page.open()
        pages.home_page.search_for_product(product["name"])
        pages.search_page.click_product_by_name(product["name"])
        pages.product_page.add_to_cart(
            quantity=order["quantity"], size=order["size"], color=order["color"]
        )

        pages.home_page.click_cart_icon()
        pages.cart_page.click_proceed_to_checkout()

        pages.checkout_page.complete_checkout(
            address=address,
            card_number=order["payment"]["card_number"],
            expiry=order["payment"]["expiry"],
            cvv=order["payment"]["cvv"],
        )

        self.assertions.assert_true(
            pages.checkout_page.is_order_successful(),
            "Expected order confirmation message after placing the order",
        )
        self.assertions.assert_true(
            len(pages.checkout_page.get_order_number()) > 0,
            "Expected a non-empty order number on the confirmation page",
        )

    @pytest.mark.regression
    @pytest.mark.checkout
    @pytest.mark.negative
    def test_checkout_fails_with_incomplete_address(self):
        order = JsonReaderUtility.find_record(
            TestDataFiles.ORDERS, "orders", "order_reference", "ORD-DEMO-0002"
        )
        product = JsonReaderUtility.find_record(
            TestDataFiles.PRODUCTS, "products", "product_id", order["product_id"]
        )
        pages = self.get_pages()

        pages.home_page.open()
        pages.home_page.search_for_product(product["name"])
        pages.search_page.click_product_by_name(product["name"])
        pages.product_page.add_to_cart(
            quantity=order["quantity"], size=order["size"], color=order["color"]
        )

        pages.home_page.click_cart_icon()
        pages.cart_page.click_proceed_to_checkout()

        # Intentionally leave the shipping address form untouched and
        # attempt to proceed straight to payment.
        pages.checkout_page.click_continue_to_payment()

        error_message = pages.checkout_page.get_checkout_error_message()
        self.assertions.assert_contains(
            error_message.lower(), "address",
            "Expected a validation error mentioning the missing address",
        )
