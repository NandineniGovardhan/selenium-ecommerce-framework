"""
search_locators.py
--------------------
Centralized locators for the Search Results page.
"""

from selenium.webdriver.common.by import By


class SearchPageLocators:
    RESULTS_CONTAINER = (By.CSS_SELECTOR, "div.search-results")
    RESULT_ITEM = (By.CSS_SELECTOR, "div.search-results div.product-card")
    RESULT_ITEM_TITLE = (By.CSS_SELECTOR, "div.product-card h3.product-title")
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, "div.no-results-found")
    SORT_DROPDOWN = (By.ID, "sort-by-select")
    RESULT_COUNT_LABEL = (By.CSS_SELECTOR, "span.result-count")

    @staticmethod
    def result_item_by_name(product_name: str):
        """Dynamic locator for a specific product card by its visible title."""
        return (
            By.XPATH,
            f"//div[@class='product-card'][.//h3[contains(text(), '{product_name}')]]",
        )
