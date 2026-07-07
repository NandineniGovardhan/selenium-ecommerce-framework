"""
home_locators.py
------------------
Centralized locators for the Home page (header, navigation, search bar).
"""

from selenium.webdriver.common.by import By


class HomePageLocators:
    SEARCH_INPUT = (By.ID, "search-field")
    SEARCH_SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[data-testid='search-submit']")
    LOGIN_LINK = (By.LINK_TEXT, "Sign In")
    LOGOUT_LINK = (By.LINK_TEXT, "Sign Out")
    USER_ACCOUNT_MENU = (By.CSS_SELECTOR, "div.user-account-menu")
    CART_ICON = (By.CSS_SELECTOR, "a[data-testid='cart-icon']")
    CART_ITEM_COUNT_BADGE = (By.CSS_SELECTOR, "span.cart-item-count")
    CATEGORY_NAV_MENU = (By.CSS_SELECTOR, "nav.category-menu")
    LOGGED_OUT_BANNER = (By.CSS_SELECTOR, "div.guest-banner")
