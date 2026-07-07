"""
file_reader_utility.py
-----------------------
Generic, format-agnostic file reading helpers. JSON-specific logic lives
in json_reader_utility.py; this module handles plain text/CSV style reads
and common path resolution so utilities don't duplicate os.path logic.
"""

import os
from typing import List

from utilities.logger_utility import get_logger

log = get_logger(__name__)


class FileReaderUtility:
    """Reusable helpers for reading plain files from disk."""

    @staticmethod
    def read_text_file(file_path: str) -> str:
        """Reads and returns the full contents of a text file."""
        FileReaderUtility._assert_exists(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        log.debug("Read text file: %s", file_path)
        return content

    @staticmethod
    def read_lines(file_path: str) -> List[str]:
        """Reads a text file and returns a list of stripped lines."""
        FileReaderUtility._assert_exists(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]
        log.debug("Read %d lines from file: %s", len(lines), file_path)
        return lines

    @staticmethod
    def _assert_exists(file_path: str) -> None:
        if not os.path.exists(file_path):
            log.error("File not found: %s", file_path)
            raise FileNotFoundError(f"File not found: {file_path}")
