"""
Provides a logging.Filter subclass to automatically censor URLs in log records.
"""

import logging
from typing import List, Optional, Set

from .filterurl import FilterURL


# pylint: disable=R0903
class URLFilter(logging.Filter):
    """
    A logging filter that automatically finds, censors, and conditionally
    appends URL information to the log message itself.
    This filter is designed to work with standard formatters.
    """

    # pylint: disable=R0913, R0917
    def __init__(
        self,
        bad_keys: Optional[Set[str]] = None,
        bad_keys_re: Optional[List[str]] = None,
        bad_path_re: Optional[str] = None,
        url_filter_instance: Optional[FilterURL] = None,
        fallback: bool = True,
        name: str = "",
    ):
        """Initializes the filter."""
        super().__init__(name)
        self.fallback = fallback
        if url_filter_instance:
            self.url_filter = url_filter_instance
        else:
            self.url_filter = FilterURL(bad_keys, bad_keys_re, bad_path_re)

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Finds and censors URLs, then modifies the log record's message
        to include the censored URL, hiding complexity from the formatter.
        """
        found_and_censored_url = None

        # Preferred method: Check for 'url' in 'extra'
        if hasattr(record, "url") and isinstance(record.url, str):
            found_and_censored_url = self.url_filter.remove_sensitive(record.url)
            # We don't need the original 'url' on the record anymore
            del record.url

        # Fallback method: Search in message arguments
        elif self.fallback and isinstance(record.args, tuple) and record.args:
            new_args = []
            for arg in record.args:
                if isinstance(arg, str) and ("http://" in arg or "https://" in arg):
                    censored_arg = self.url_filter.remove_sensitive(arg)
                    # We only store the first URL found for the suffix
                    if not found_and_censored_url:
                        found_and_censored_url = censored_arg
                    new_args.append(censored_arg)
                else:
                    new_args.append(arg)
            record.args = tuple(new_args)

        # Pre-render the message and add our suffix if needed,
        # AFTER arguments in record.args have been censored.
        message = record.getMessage()

        if found_and_censored_url:
            message += f" | (URL data: {found_and_censored_url})"

        record.msg = message
        record.args = ()

        return True
