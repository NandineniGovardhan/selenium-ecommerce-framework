"""
login_locators.py
-------------------
Centralized locators for the Login page. Locators NEVER live inside page
methods or tests — they are declared once, here, and imported wherever
needed. This is the single place to update if the UI changes.
"""

from selenium.webdriver.common.by import By


class LoginPageLocators:
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit'][data-testid='login-button']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.error-message")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot Password?")
    LOGGED_IN_USER_MENU = (By.CSS_SELECTOR, "div.user-account-menu")
