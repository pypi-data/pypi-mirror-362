#!/usr/bin/env python3
"""
Example of the module usage
"""

import time

from filter_url import FilterURL

# pylint: disable=R0801
URLS_TO_FILTER = [
    "https://example.com/api/v1/get/data?user_id=123",
    "https://example.com/data?token=abc-123-xyz",
    "https://example.com/data?user_session_id=def-456",
    "https://john.doe:my_secret_password@example.com/data",
    "https://example.com/api/v1/SOME_API_KEY/resource",
    "https://example.com/user/12345/delete/confirm",
    "https://api_user:12345@example.com?api_secret=very-secret",
    "https://example.com/api/v1/KEY-123/resource?session=deadbeef",
    "https://admin:super-secret@exmpl.com/api/v1/BIG-KEY/res?token=abc&session_id=123&clean=true",
]


def run_class_based_example():
    """Demonstrates using a FilterURL class instance for batch processing."""
    print("--- 1. Testing with a pre-configured class instance ---")

    # --- Setup ---
    # Create a custom filter configuration
    custom_bad_keys = {"token", "password", "key"}
    custom_bad_keys_re = ["secret", "session"]
    custom_path_re_named = r"/api/v1/(?P<api_key>[^/]+)/resource"
    custom_path_re_simple = r"(?<=/user/)\d+(?=/delete)"

    # Instantiate the filter class ONCE
    custom_filter = FilterURL(
        bad_keys=custom_bad_keys,
        bad_keys_re=custom_bad_keys_re,
        bad_path_re=f"({custom_path_re_named})|({custom_path_re_simple})",  # Combine regexes
    )

    # Also create a default filter to show the difference
    default_filter = FilterURL()

    # --- Run with default filter ---
    print("\n--- Filtering with DEFAULT rules ---")
    start_time = time.perf_counter()
    for url in URLS_TO_FILTER:
        default_filter.remove_sensitive(url)  # Discard result, just measure time
    duration = time.perf_counter() - start_time
    print(f"Original: {URLS_TO_FILTER[8]}")
    print(f"Filtered: {default_filter.remove_sensitive(URLS_TO_FILTER[8])}")
    print(f"Processed {len(URLS_TO_FILTER)} URLs in {duration:.6f} seconds.")

    # --- Run with custom filter ---
    print("\n--- Filtering with CUSTOM rules ---")
    start_time = time.perf_counter()
    filtered_urls = []
    for url in URLS_TO_FILTER:
        filtered_urls.append(custom_filter.remove_sensitive(url))
    duration = time.perf_counter() - start_time

    print(f"Original: {URLS_TO_FILTER[8]}")
    print(f"Filtered: {filtered_urls[8]}")
    print(f"Processed {len(URLS_TO_FILTER)} URLs in {duration:.6f} seconds.")


if __name__ == "__main__":
    run_class_based_example()
