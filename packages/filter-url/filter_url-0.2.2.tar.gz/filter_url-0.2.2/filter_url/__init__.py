"""
A simple, fast, and configurable URL sensitve data filter.
"""

import importlib.metadata

from .filterurl import (
    DEFAULT_BAD_KEYS,
    DEFAULT_BAD_KEYS_RE,
    DEFAULT_BAD_PATH_RE,
    FilterURL,
    filter_url,
)
from .logging_format import UrlFilteringFilter

_metadata = importlib.metadata.metadata("filter_url")
__version__ = _metadata["Version"]
__author__ = _metadata["Author-email"]
__license__ = _metadata["License"]

# This defines the public API of the module
__all__ = [
    "FilterURL",
    "filter_url",
    "UrlFilteringFilter",
    "DEFAULT_BAD_KEYS",
    "DEFAULT_BAD_KEYS_RE",
    "DEFAULT_BAD_PATH_RE",
]
