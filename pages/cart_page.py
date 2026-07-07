"""
cart_page.py
--------------
Page Object for the Shopping Cart page.
"""

from typing import List

from base.base_page import BasePage
from pages.locators.cart_locators import CartPageLocators
from utilities.logger_utility import get_logger

log = get_logger(__name__)


class CartPage(BasePage):
    """Encapsulates all interactions available on the Shopping Cart page."""

    def get_cart_item_names(self) -> List[str]:
        """Returns the visible names of every item currently in the cart."""
        elements = self.actions.find_all(CartPageLocators.CART_ITEM_NAME)
        return [el.text.strip() for el in elements]

    def get_cart_item_count(self) -> int:
        return len(self.actions.find_all(CartPageLocators.CART_ITEM_ROW))

    def remove_item(self, product_name: str) -> None:
        """Removes a specific item from the cart by its visible name."""
        log.info("Removing item from cart: %s", product_name)
        self.actions.click(CartPageLocators.remove_button_for_item(product_name))
        if self.alert.is_alert_present():
            self.alert.accept_alert()
        elif self.actions.is_displayed(CartPageLocators.REMOVE_CONFIRM_DIALOG_YES, timeout=3):
            self.actions.click(CartPageLocators.REMOVE_CONFIRM_DIALOG_YES)

    def is_cart_empty(self) -> bool:
        return self.actions.is_displayed(CartPageLocators.CART_EMPTY_MESSAGE, timeout=5)

    def get_subtotal(self) -> str:
        return self.actions.get_text(CartPageLocators.CART_SUBTOTAL)

    def update_item_quantity(self, quantity: int) -> None:
        self.actions.type_text(CartPageLocators.QUANTITY_INPUT_IN_CART, str(quantity))

    def click_proceed_to_checkout(self) -> None:
        log.info("Proceeding to checkout")
        self.actions.click(CartPageLocators.PROCEED_TO_CHECKOUT_BUTTON)
