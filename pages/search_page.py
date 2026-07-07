"""
search_page.py
----------------
Page Object for the Search Results page.
"""

from typing import List

from base.base_page import BasePage
from pages.locators.search_locators import SearchPageLocators
from utilities.logger_utility import get_logger

log = get_logger(__name__)


class SearchPage(BasePage):
    """Encapsulates all interactions available on the Search Results page."""

    def get_result_titles(self) -> List[str]:
        """Returns the visible titles of every product card in the results."""
        elements = self.actions.find_all(SearchPageLocators.RESULT_ITEM_TITLE)
        return [el.text.strip() for el in elements]

    def get_result_count(self) -> int:
        """Returns how many product cards are currently displayed."""
        return len(self.actions.find_all(SearchPageLocators.RESULT_ITEM))

    def click_product_by_name(self, product_name: str) -> None:
        """Clicks a specific product card, identified by its visible name."""
        log.info("Opening product from search results: %s", product_name)
        self.actions.click(SearchPageLocators.result_item_by_name(product_name))

    def is_no_results_message_displayed(self) -> bool:
        return self.actions.is_displayed(SearchPageLocators.NO_RESULTS_MESSAGE, timeout=5)

    def sort_results_by(self, sort_option_text: str) -> None:
        """Selects a sort option (e.g. 'Price: Low to High') from the dropdown."""
        self.dropdown.select_by_visible_text(SearchPageLocators.SORT_DROPDOWN, sort_option_text)
