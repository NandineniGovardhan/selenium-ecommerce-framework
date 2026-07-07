"""
json_reader_utility.py
------------------------
Reads JSON test data files (users, products, addresses, orders) so that
NO test data is ever hardcoded inside test scripts or page objects.

All test data files live under /testdata and are referenced through
constants.TestDataFiles to avoid hardcoded paths scattered across the
codebase.
"""

import json
import os
import re
from typing import Any, Dict, List, Union

from constants.constants import TESTDATA_DIR
from utilities.logger_utility import get_logger

log = get_logger(__name__)

_ENV_PLACEHOLDER_PATTERN = re.compile(r"^\$\{([A-Z0-9_]+)\}$")


class JsonReaderUtility:
    """Reusable helpers for reading and querying JSON test data."""

    _cache: Dict[str, Any] = {}

    @classmethod
    def read_json(cls, relative_path: str) -> Union[Dict, List]:
        """
        Reads a JSON file located under the testdata directory.

        Values written as "${ENV_VAR_NAME}" are resolved from environment
        variables at load time. This lets credential-shaped fields (e.g.
        passwords) be referenced by JSON test data files WITHOUT ever
        hardcoding the actual secret value in source control.

        Args:
            relative_path: Path relative to TESTDATA_DIR,
                            e.g. constants.TestDataFiles.USERS

        Returns:
            Parsed JSON content (dict or list) with env placeholders resolved.
        """
        if relative_path in cls._cache:
            return cls._cache[relative_path]

        full_path = os.path.join(TESTDATA_DIR, relative_path)
        if not os.path.exists(full_path):
            log.error("Test data file not found: %s", full_path)
            raise FileNotFoundError(f"Test data file not found: {full_path}")

        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        data = cls._resolve_env_placeholders(data)

        cls._cache[relative_path] = data
        log.debug("Loaded test data file: %s", full_path)
        return data

    @classmethod
    def _resolve_env_placeholders(cls, value: Any) -> Any:
        """Recursively replaces '${VAR}' string values with os.environ['VAR']."""
        if isinstance(value, dict):
            return {k: cls._resolve_env_placeholders(v) for k, v in value.items()}
        if isinstance(value, list):
            return [cls._resolve_env_placeholders(v) for v in value]
        if isinstance(value, str):
            match = _ENV_PLACEHOLDER_PATTERN.match(value)
            if match:
                env_var = match.group(1)
                resolved = os.getenv(env_var)
                if resolved is None:
                    log.warning(
                        "Environment variable '%s' is not set; leaving placeholder "
                        "unresolved. Set it in your local .env or CI secrets.",
                        env_var,
                    )
                    return value
                return resolved
        return value

    @classmethod
    def get_by_key(cls, relative_path: str, key: str) -> Any:
        """Fetches a specific top-level key's value from a JSON data file."""
        data = cls.read_json(relative_path)
        if key not in data:
            raise KeyError(f"Key '{key}' not found in {relative_path}")
        return data[key]

    @classmethod
    def find_record(cls, relative_path: str, collection_key: str,
                     match_field: str, match_value: Any) -> Dict[str, Any]:
        """
        Finds a single record inside a named collection by matching a field.

        Example:
            find_record(TestDataFiles.USERS, "users", "role", "standard_user")
        """
        collection = cls.get_by_key(relative_path, collection_key)
        for record in collection:
            if record.get(match_field) == match_value:
                return record
        raise ValueError(
            f"No record found where {match_field}='{match_value}' "
            f"in '{collection_key}' of {relative_path}"
        )
