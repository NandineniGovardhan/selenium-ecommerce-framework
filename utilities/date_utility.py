"""
date_utility.py
----------------
Reusable date/time helpers (timestamped filenames, order date validation,
date arithmetic used by checkout/order test scenarios).
"""

from datetime import datetime, timedelta

from constants.constants import DATE_FORMAT, TIMESTAMP_FORMAT


class DateUtility:
    """Static helpers for date/time formatting and arithmetic."""

    @staticmethod
    def current_timestamp() -> str:
        """Returns current timestamp formatted for filenames/logs."""
        return datetime.now().strftime(TIMESTAMP_FORMAT)

    @staticmethod
    def current_date() -> str:
        """Returns current date in the framework's standard date format."""
        return datetime.now().strftime(DATE_FORMAT)

    @staticmethod
    def add_days(days: int, from_date: str = None) -> str:
        """
        Adds `days` to a given date (or today if not provided) and returns
        the result formatted as DATE_FORMAT.
        """
        base_date = (
            datetime.strptime(from_date, DATE_FORMAT) if from_date else datetime.now()
        )
        return (base_date + timedelta(days=days)).strftime(DATE_FORMAT)

    @staticmethod
    def is_future_date(date_str: str) -> bool:
        """Returns True if the given date string is later than today."""
        return datetime.strptime(date_str, DATE_FORMAT) > datetime.now()
