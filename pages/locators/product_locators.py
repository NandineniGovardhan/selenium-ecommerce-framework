"""
product_locators.py
----------------------
Centralized locators for the Product Detail page.
"""

from selenium.webdriver.common.by import By


class ProductPageLocators:
    PRODUCT_TITLE = (By.CSS_SELECTOR, "h1.product-title")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "span.product-price")
    QUANTITY_INPUT = (By.ID, "product-quantity")
    SIZE_DROPDOWN = (By.ID, "product-size")
    COLOR_DROPDOWN = (By.ID, "product-color")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[data-testid='add-to-cart']")
    ADD_TO_CART_CONFIRMATION = (By.CSS_SELECTOR, "div.add-to-cart-success-toast")
    OUT_OF_STOCK_LABEL = (By.CSS_SELECTOR, "span.out-of-stock-label")
