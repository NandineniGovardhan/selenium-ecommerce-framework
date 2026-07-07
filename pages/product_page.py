"""
product_page.py
------------------
Page Object for the Product Detail page (add-to-cart flow, options).
"""

from base.base_page import BasePage
from pages.locators.product_locators import ProductPageLocators
from utilities.logger_utility import get_logger

log = get_logger(__name__)


class ProductPage(BasePage):
    """Encapsulates all interactions available on the Product Detail page."""

    def get_product_title(self) -> str:
        return self.actions.get_text(ProductPageLocators.PRODUCT_TITLE)

    def get_product_price(self) -> str:
        return self.actions.get_text(ProductPageLocators.PRODUCT_PRICE)

    def set_quantity(self, quantity: int) -> "ProductPage":
        self.actions.type_text(ProductPageLocators.QUANTITY_INPUT, str(quantity))
        return self

    def select_size(self, size: str) -> "ProductPage":
        self.dropdown.select_by_visible_text(ProductPageLocators.SIZE_DROPDOWN, size)
        return self

    def select_color(self, color: str) -> "ProductPage":
        self.dropdown.select_by_visible_text(ProductPageLocators.COLOR_DROPDOWN, color)
        return self

    def click_add_to_cart(self) -> None:
        log.info("Adding product to cart: %s", self.get_product_title())
        self.actions.click(ProductPageLocators.ADD_TO_CART_BUTTON)

    def add_to_cart(self, quantity: int = 1, size: str = None, color: str = None) -> None:
        """Convenience method covering the full add-to-cart interaction."""
        if size:
            self.select_size(size)
        if color:
            self.select_color(color)
        self.set_quantity(quantity)
        self.click_add_to_cart()

    def is_add_to_cart_confirmation_displayed(self) -> bool:
        return self.actions.is_displayed(ProductPageLocators.ADD_TO_CART_CONFIRMATION, timeout=10)

    def is_out_of_stock(self) -> bool:
        return self.actions.is_displayed(ProductPageLocators.OUT_OF_STOCK_LABEL, timeout=3)
