"""
checkout_locators.py
-----------------------
Centralized locators for the Checkout flow (address, payment, review).
"""

from selenium.webdriver.common.by import By


class CheckoutPageLocators:
    FULL_NAME_INPUT = (By.ID, "checkout-full-name")
    ADDRESS_LINE1_INPUT = (By.ID, "checkout-address-line1")
    CITY_INPUT = (By.ID, "checkout-city")
    STATE_DROPDOWN = (By.ID, "checkout-state")
    ZIP_CODE_INPUT = (By.ID, "checkout-zip")
    COUNTRY_DROPDOWN = (By.ID, "checkout-country")
    CONTINUE_TO_PAYMENT_BUTTON = (By.CSS_SELECTOR, "button[data-testid='continue-to-payment']")

    CARD_NUMBER_INPUT = (By.ID, "checkout-card-number")
    CARD_EXPIRY_INPUT = (By.ID, "checkout-card-expiry")
    CARD_CVV_INPUT = (By.ID, "checkout-card-cvv")
    PLACE_ORDER_BUTTON = (By.CSS_SELECTOR, "button[data-testid='place-order']")

    ORDER_CONFIRMATION_MESSAGE = (By.CSS_SELECTOR, "div.order-confirmation-message")
    ORDER_NUMBER_LABEL = (By.CSS_SELECTOR, "span.order-number")
    CHECKOUT_ERROR_MESSAGE = (By.CSS_SELECTOR, "div.checkout-error-message")
