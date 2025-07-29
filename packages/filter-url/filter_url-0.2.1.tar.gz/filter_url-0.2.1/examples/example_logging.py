#!/usr/bin/env python3
"""
Example of the module usage integrated with logging
"""

import logging
import sys

from filter_url import UrlFilteringFilter


def run_final_logging_example():
    """
    Demonstration itself
    """
    #  Configure a logger
    logger = logging.getLogger("my_final_logger")
    logger.setLevel(logging.INFO)
    if logger.hasHandlers():
        logger.handlers.clear()

    # Simply add our filter. All the magic is inside.
    logger.addFilter(UrlFilteringFilter())

    # 3. Use a standard, simple Formatter.
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("LOG: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    print("--- Testing the 'magic' logging filter ---")

    # Case 1: URL provided via 'extra'. The suffix will be added by the filter.
    dirty_url_1 = "https://user:my_pass@example.com/data?token=123"
    logger.info("User auth attempt.", extra={"url": dirty_url_1})

    # Case 2: URL in the message body (fallback). The suffix will be added.
    dirty_url_2 = "https://api.service.com/data?session_id=abc-xyz"
    logger.info("API call to %s was made.", dirty_url_2)

    # Case 3: No URL in the message at all
    logger.info("System startup complete.")


if __name__ == "__main__":
    run_final_logging_example()
