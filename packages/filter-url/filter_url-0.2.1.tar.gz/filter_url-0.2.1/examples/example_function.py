#!/usr/bin/env python3
"""
Example of the simplest module usage, with the stand-alone function.
It is not efficient though if you have a lot of URL filtering because
it re-compiles regexes every time.
"""

import time

from filter_url import filter_url

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


def run_function_based_example():
    """Demonstrates using the standalone filter_url function."""
    print("--- 2. Testing with the standalone function ---")

    # --- Setup ---
    # The same custom filter configuration as uncompiled strings/sets
    custom_bad_keys = {"token", "password", "key"}
    custom_bad_keys_re = ["secret", "session"]
    custom_path_re_named = r"/api/v1/(?P<api_key>[^/]+)/resource"
    custom_path_re_simple = r"(?<=/user/)\d+(?=/delete)"
    combined_path_re = f"({custom_path_re_named})|({custom_path_re_simple})"

    # --- Run with default filter ---
    print("\n--- Filtering with DEFAULT rules ---")
    start_time = time.perf_counter()
    for url in URLS_TO_FILTER:
        filter_url(url)  # This uses the default filters built into the module
    duration = time.perf_counter() - start_time
    print(f"Original: {URLS_TO_FILTER[8]}")
    print(f"Filtered: {filter_url(URLS_TO_FILTER[8])}")
    print(f"Processed {len(URLS_TO_FILTER)} URLs in {duration:.6f} seconds.")

    # --- Run with custom filter ---
    # NOTE: This is less efficient for loops as it re-creates the FilterURL
    # instance and re-compiles regexes on every single call.
    print("\n--- Filtering with CUSTOM rules ---")
    start_time = time.perf_counter()
    filtered_urls = []
    for url in URLS_TO_FILTER:
        filtered_urls.append(
            filter_url(
                url,
                bad_keys=custom_bad_keys,
                bad_keys_re=custom_bad_keys_re,
                bad_path_re=combined_path_re,
            )
        )
    duration = time.perf_counter() - start_time

    print(f"Original: {URLS_TO_FILTER[8]}")
    print(f"Filtered: {filtered_urls[8]}")
    print(f"Processed {len(URLS_TO_FILTER)} URLs in {duration:.6f} seconds.")


if __name__ == "__main__":
    run_function_based_example()
