"""
cart_locators.py
-------------------
Centralized locators for the Shopping Cart page.
"""

from selenium.webdriver.common.by import By


class CartPageLocators:
    CART_ITEM_ROW = (By.CSS_SELECTOR, "div.cart-item-row")
    CART_ITEM_NAME = (By.CSS_SELECTOR, "div.cart-item-row span.item-name")
    CART_ITEM_REMOVE_BUTTON = (By.CSS_SELECTOR, "div.cart-item-row button.remove-item")
    CART_EMPTY_MESSAGE = (By.CSS_SELECTOR, "div.empty-cart-message")
    CART_SUBTOTAL = (By.CSS_SELECTOR, "span.cart-subtotal")
    PROCEED_TO_CHECKOUT_BUTTON = (By.CSS_SELECTOR, "button[data-testid='proceed-to-checkout']")
    QUANTITY_INPUT_IN_CART = (By.CSS_SELECTOR, "div.cart-item-row input.item-quantity")
    REMOVE_CONFIRM_DIALOG_YES = (By.CSS_SELECTOR, "button[data-testid='confirm-remove']")

    @staticmethod
    def remove_button_for_item(product_name: str):
        """Dynamic locator for the remove button of a specific cart item."""
        return (
            By.XPATH,
            f"//div[@class='cart-item-row'][.//span[contains(text(), '{product_name}')]]"
            f"//button[contains(@class,'remove-item')]",
        )
