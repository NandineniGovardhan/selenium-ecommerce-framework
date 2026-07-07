"""
checkout_page.py
-------------------
Page Object for the Checkout flow: shipping address, payment, and order
confirmation.
"""

from base.base_page import BasePage
from pages.locators.checkout_locators import CheckoutPageLocators
from utilities.logger_utility import get_logger

log = get_logger(__name__)


class CheckoutPage(BasePage):
    """Encapsulates all interactions available across the Checkout flow."""

    def fill_shipping_address(self, address: dict) -> "CheckoutPage":
        """
        Fills the shipping address form.

        Args:
            address: dict matching testdata/addresses/addresses.json schema,
                      e.g. {"full_name", "address_line1", "city", "state",
                            "zip_code", "country"}
        """
        log.info("Filling shipping address for: %s", address.get("full_name"))
        self.actions.type_text(CheckoutPageLocators.FULL_NAME_INPUT, address["full_name"])
        self.actions.type_text(CheckoutPageLocators.ADDRESS_LINE1_INPUT, address["address_line1"])
        self.actions.type_text(CheckoutPageLocators.CITY_INPUT, address["city"])
        self.dropdown.select_by_visible_text(CheckoutPageLocators.STATE_DROPDOWN, address["state"])
        self.actions.type_text(CheckoutPageLocators.ZIP_CODE_INPUT, address["zip_code"])
        self.dropdown.select_by_visible_text(CheckoutPageLocators.COUNTRY_DROPDOWN, address["country"])
        return self

    def click_continue_to_payment(self) -> None:
        self.actions.click(CheckoutPageLocators.CONTINUE_TO_PAYMENT_BUTTON)

    def fill_payment_details(self, card_number: str, expiry: str, cvv: str) -> "CheckoutPage":
        log.info("Filling payment details")
        self.actions.type_text(CheckoutPageLocators.CARD_NUMBER_INPUT, card_number)
        self.actions.type_text(CheckoutPageLocators.CARD_EXPIRY_INPUT, expiry)
        self.actions.type_text(CheckoutPageLocators.CARD_CVV_INPUT, cvv)
        return self

    def click_place_order(self) -> None:
        log.info("Placing order")
        self.actions.click(CheckoutPageLocators.PLACE_ORDER_BUTTON)

    def complete_checkout(self, address: dict, card_number: str, expiry: str, cvv: str) -> None:
        """Convenience method covering the entire checkout flow end-to-end."""
        self.fill_shipping_address(address)
        self.click_continue_to_payment()
        self.fill_payment_details(card_number, expiry, cvv)
        self.click_place_order()

    def get_order_confirmation_message(self) -> str:
        return self.actions.get_text(CheckoutPageLocators.ORDER_CONFIRMATION_MESSAGE)

    def get_order_number(self) -> str:
        return self.actions.get_text(CheckoutPageLocators.ORDER_NUMBER_LABEL)

    def is_order_successful(self) -> bool:
        return self.actions.is_displayed(CheckoutPageLocators.ORDER_CONFIRMATION_MESSAGE, timeout=15)

    def get_checkout_error_message(self) -> str:
        return self.actions.get_text(CheckoutPageLocators.CHECKOUT_ERROR_MESSAGE)
