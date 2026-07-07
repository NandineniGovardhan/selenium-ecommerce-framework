"""
config_reader.py
-----------------
Centralized configuration reader for the framework.

Responsibilities:
    * Read global defaults from config.ini
    * Read environment-specific values (base_url, api_url, db, etc.)
      from the matching <env>_config.json file
    * Allow runtime override of environment/browser via pytest CLI options
    * Provide a single, cached, thread-safe access point for configuration
      so that no module needs to re-parse files repeatedly.

No other module should read config.ini or *_config.json directly. Every
component (drivers, pages, tests, utilities) must go through ConfigReader.
"""

import configparser
import json
import os
import threading
from typing import Any, Dict, Optional

_CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
_INI_PATH = os.path.join(_CONFIG_DIR, "config.ini")


class ConfigReader:
    """Singleton-style configuration reader with runtime override support."""

    _instance: Optional["ConfigReader"] = None
    _lock = threading.Lock()

    def __new__(cls) -> "ConfigReader":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize()
            return cls._instance

    def _initialize(self) -> None:
        self._ini = configparser.ConfigParser()
        if not os.path.exists(_INI_PATH):
            raise FileNotFoundError(f"Global config file not found: {_INI_PATH}")
        self._ini.read(_INI_PATH)

        # Runtime overrides (set by conftest.py from CLI options / env vars)
        self._override_env: Optional[str] = os.getenv("FRAMEWORK_ENV")
        self._override_browser: Optional[str] = os.getenv("FRAMEWORK_BROWSER")
        self._env_config_cache: Dict[str, Dict[str, Any]] = {}

    # ------------------------------------------------------------------ #
    # Runtime override setters (called once from conftest.py)
    # ------------------------------------------------------------------ #
    def set_environment(self, environment: str) -> None:
        self._override_env = environment

    def set_browser(self, browser: str) -> None:
        self._override_browser = browser

    # ------------------------------------------------------------------ #
    # Global (config.ini) accessors
    # ------------------------------------------------------------------ #
    def get_environment(self) -> str:
        return (self._override_env or self._ini["DEFAULT"].get("environment", "qa")).lower()

    def get_browser(self) -> str:
        return (self._override_browser or self._ini["DEFAULT"].get("browser", "chrome")).lower()

    def get_headless(self) -> bool:
        return self._ini["DEFAULT"].getboolean("headless", fallback=False)

    def get_implicit_wait(self) -> int:
        return self._ini["DEFAULT"].getint("implicit_wait", fallback=5)

    def get_explicit_wait(self) -> int:
        return self._ini["DEFAULT"].getint("explicit_wait", fallback=15)

    def get_page_load_timeout(self) -> int:
        return self._ini["DEFAULT"].getint("page_load_timeout", fallback=30)

    def get_retry_count(self) -> int:
        return self._ini["DEFAULT"].getint("retry_count", fallback=1)

    def get_screenshot_on_failure(self) -> bool:
        return self._ini["DEFAULT"].getboolean("screenshot_on_failure", fallback=True)

    def get_report_dir(self) -> str:
        return self._ini["REPORT"].get("report_dir", "reports")

    def get_report_title(self) -> str:
        return self._ini["REPORT"].get("report_title", "Automation Report")

    def get_log_dir(self) -> str:
        return self._ini["LOGGING"].get("log_dir", "logs")

    def get_log_level(self) -> str:
        return self._ini["LOGGING"].get("log_level", "INFO")

    # ------------------------------------------------------------------ #
    # Environment specific (json) accessors
    # ------------------------------------------------------------------ #
    def _load_env_config(self, environment: str) -> Dict[str, Any]:
        if environment in self._env_config_cache:
            return self._env_config_cache[environment]

        json_path = os.path.join(_CONFIG_DIR, f"{environment}_config.json")
        if not os.path.exists(json_path):
            raise FileNotFoundError(
                f"No configuration file found for environment '{environment}' "
                f"(expected: {json_path})"
            )
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self._env_config_cache[environment] = data
        return data

    def get_base_url(self) -> str:
        return self._load_env_config(self.get_environment())["base_url"]

    def get_api_base_url(self) -> str:
        return self._load_env_config(self.get_environment())["api_base_url"]

    def get_env_value(self, key: str, default: Any = None) -> Any:
        """Generic accessor for any key inside the active environment's JSON file."""
        return self._load_env_config(self.get_environment()).get(key, default)


# Module-level singleton instance used across the framework
config_reader = ConfigReader()
