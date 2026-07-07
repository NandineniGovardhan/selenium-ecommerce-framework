"""
assertion_utility.py
----------------------
Reusable assertion methods so test scripts never write raw `assert`
statements with inline logic. Every assertion here logs both success
and failure clearly, which vastly improves failure triage in reports.
"""

from typing import Any

from utilities.logger_utility import get_logger

log = get_logger(__name__)


class AssertionUtility:
    """Centralized, self-logging assertion helpers."""

    @staticmethod
    def assert_equals(actual: Any, expected: Any, message: str = "") -> None:
        if actual != expected:
            log.error("Assertion failed [%s]: expected='%s', actual='%s'",
                       message, expected, actual)
            raise AssertionError(
                f"{message} | Expected: '{expected}' but got: '{actual}'"
            )
        log.info("Assertion passed [%s]: '%s' == '%s'", message, actual, expected)

    @staticmethod
    def assert_not_equals(actual: Any, not_expected: Any, message: str = "") -> None:
        if actual == not_expected:
            log.error("Assertion failed [%s]: value should not equal '%s'",
                       message, not_expected)
            raise AssertionError(f"{message} | Value should not equal: '{not_expected}'")
        log.info("Assertion passed [%s]: '%s' != '%s'", message, actual, not_expected)

    @staticmethod
    def assert_true(condition: bool, message: str = "") -> None:
        if not condition:
            log.error("Assertion failed [%s]: expected True but got False", message)
            raise AssertionError(f"{message} | Expected condition to be True")
        log.info("Assertion passed [%s]: condition is True", message)

    @staticmethod
    def assert_false(condition: bool, message: str = "") -> None:
        if condition:
            log.error("Assertion failed [%s]: expected False but got True", message)
            raise AssertionError(f"{message} | Expected condition to be False")
        log.info("Assertion passed [%s]: condition is False", message)

    @staticmethod
    def assert_contains(container: Any, item: Any, message: str = "") -> None:
        if item not in container:
            log.error("Assertion failed [%s]: '%s' not found in '%s'",
                       message, item, container)
            raise AssertionError(f"{message} | '{item}' not found in '{container}'")
        log.info("Assertion passed [%s]: '%s' found in container", message, item)

    @staticmethod
    def assert_greater_than(actual: Any, minimum: Any, message: str = "") -> None:
        if not actual > minimum:
            log.error("Assertion failed [%s]: '%s' is not greater than '%s'",
                       message, actual, minimum)
            raise AssertionError(f"{message} | '{actual}' is not greater than '{minimum}'")
        log.info("Assertion passed [%s]: '%s' > '%s'", message, actual, minimum)
