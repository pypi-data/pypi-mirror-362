"""
tests for filter_url module
"""
import logging
from typing import Any, Dict

import pytest

# Import all components from your module with the correct name
from filter_url import (
    FilterURL,
    URLFilter,
    filter_url,
)

# ======================================================================
# Test data setup: We now define separate configs for separate path regexes
# ======================================================================

# A config with NO path regex
config_no_path = {
    "bad_keys": {"token", "password", "key"},
    "bad_keys_re": ["secret", "session"],
    "bad_path_re": None,
}

# A config ONLY for the path regex with a NAMED group
config_named_path = {
    "bad_keys": set(),  # No key filters for this specific test
    "bad_keys_re": [],
    "bad_path_re": r"/api/v1/(?P<api_key>[^/]+)/resource",
}

# A config ONLY for the path regex with a SIMPLE match (using lookarounds)
config_simple_path = {
    "bad_keys": set(),
    "bad_keys_re": [],
    "bad_path_re": r"(?<=/user/)\d+(?=/delete)",
}

# A config for the "Full House" combination test
config_full_house = {
    "bad_keys": {"token", "password", "key"},
    "bad_keys_re": ["secret", "session"],
    "bad_path_re": r"/api/v1/(?P<api_key>[^/]+)/resource",  # Use one specific path regex
}


# Structure: (test_id, input_url, expected_url, config_to_use)
URL_TEST_CASES = [
    # --- Tests with no path filtering ---
    (
        "clean_url_no_change",
        "https://example.com/data?id=123",
        "https://example.com/data?id=123",
        config_no_path,
    ),
    (
        "query_exact_key",
        "https://example.com/data?token=abc-123",
        "https://example.com/data?token=[...]",
        config_no_path,
    ),
    (
        "query_regex_key",
        "https://example.com/data?user_session=def-456",
        "https://example.com/data?user_session=[...]",
        config_no_path,
    ),
    (
        "netloc_password",
        "https://user:my_pass@example.com/data",
        "https://user:[...]@example.com/data",
        config_no_path,
    ),
    # --- ISOLATED path tests ---
    (
        "path_named_group",
        "https://example.com/api/v1/SOME_KEY/resource",
        "https://example.com/api/v1/[...]/resource",
        config_named_path,
    ),
    # This test now uses its own, simple regex config and will pass
    (
        "path_simple_match",
        "https://example.com/user/12345/delete",
        "https://example.com/user/[...]/delete",
        config_simple_path,
    ),
    # --- Combination test ---
    (
        "full_house",
        "https://admin:secret@site.com/api/v1/KEY/resource?token=abc&session=123",
        "https://admin:[...]@site.com/api/v1/[...]/resource?token=[...]&session=[...]",
        config_full_house,
    ),
]


# pylint: disable=W0613
@pytest.mark.parametrize("test_id,input_url,expected_url,config", URL_TEST_CASES)
def test_filter_url_function_and_class(
    test_id: str, input_url: str, expected_url: str, config: Dict[str, Any]
):
    """
    Tests both the standalone function and the FilterURL class.
    """
    result_func = filter_url(
        url=input_url,
        censored="[...]",
        bad_keys=config["bad_keys"],
        bad_keys_re=config["bad_keys_re"],
        bad_path_re=config["bad_path_re"],
    )
    assert result_func == expected_url

    filter_instance = FilterURL(
        bad_keys=config["bad_keys"],
        bad_keys_re=config["bad_keys_re"],
        bad_path_re=config["bad_path_re"],
    )
    result_class = filter_instance.remove_sensitive(input_url, censored="[...]")
    assert result_class == expected_url


def test_logging_filter_with_extra(caplog):
    """
    Tests that the filter correctly uses the 'extra' dictionary.
    """
    logger = logging.getLogger("test_extra")
    logger.setLevel(logging.INFO)
    logger.addFilter(URLFilter())

    dirty_url = "https://example.com?token=123"
    logger.info("Test message", extra={"url": dirty_url})

    # The filter modifies the record in place
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert "token=[...]" in record.msg  # The 'magic' now puts it in the message
    assert "URL data" in record.msg


def test_logging_filter_fallback_enabled(caplog):
    """
    Tests the fallback mechanism when it's enabled (default).
    """
    logger = logging.getLogger("test_fallback_on")
    logger.setLevel(logging.INFO)
    logger.addFilter(URLFilter(fallback=True))

    dirty_url = "https://example.com?secret_key=456"
    logger.info("API call to %s", dirty_url)

    assert len(caplog.records) == 1
    record = caplog.records[0]
    # The message itself is now fully composed by the filter
    assert "secret_key=[...]" in record.getMessage()
    assert "URL data" in record.getMessage()


def test_logging_filter_fallback_disabled(caplog):
    """
    Tests that the fallback mechanism does nothing when disabled.
    """
    logger = logging.getLogger("test_fallback_off")
    logger.setLevel(logging.INFO)
    logger.addFilter(URLFilter(fallback=False))

    dirty_url = "https://example.com?secret_key=456"
    logger.info("API call to %s", dirty_url)

    assert len(caplog.records) == 1
    record = caplog.records[0]
    # The message should be unchanged as fallback is off and no 'extra' was used
    assert "secret_key=456" in record.getMessage()
    assert "URL data" not in record.getMessage()


def test_logging_filter_no_url(caplog):
    """
    Tests that no suffix is added when there is no URL in the message.
    """
    logger = logging.getLogger("test_no_url")
    logger.setLevel(logging.INFO)
    logger.addFilter(URLFilter())

    logger.info("A regular log message.")

    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.getMessage() == "A regular log message."


def test_malformed_url_handling():
    """
    Covers the try...except ValueError block in remove_sensitive().
    A malformed URL should not crash the function but return a specific string.
    """
    malformed_url = "http://[::1"  # Unclosed bracket is invalid
    result = filter_url(malformed_url)
    assert result == "MALFORMED_URL"


def test_logging_filter_init_with_instance(caplog):
    """
    Covers passing a pre-configured FilterURL instance to URLFilter.
    """
    # Create a custom, pre-configured instance first
    custom_rules = FilterURL(bad_keys={"special_key"})

    # Pass this instance during the logging filter's creation
    logger = logging.getLogger("test_init_with_instance")
    logger.setLevel(logging.INFO)
    logger.addFilter(URLFilter(url_filter_instance=custom_rules))

    dirty_url = "https://example.com/?special_key=123&token=abc"
    logger.info("Test with pre-configured instance: %s", dirty_url)

    # Check that our custom rule ('special_key') was applied, but default
    # rules (like 'token') were NOT, because we provided a whole new instance.
    record = caplog.records[0]
    assert "special_key=[...]" in record.getMessage()
    assert "token=abc" in record.getMessage()  # Default rule for 'token' is ignored


def test_logging_filter_fallback_mixed_args(caplog):
    """
    Covers the `else` branch in the fallback loop, when a log argument
    is not a URL string.
    """
    logger = logging.getLogger("test_mixed_args")
    logger.setLevel(logging.INFO)
    logger.addFilter(URLFilter(fallback=True))

    dirty_url = "https://example.com/data?secret=xyz"
    # Log with multiple arguments of different types
    logger.info("Request %s to %s for user_id %d", "GET", dirty_url, 12345)

    record = caplog.records[0]
    final_message = record.getMessage()

    # Assert that the URL was filtered
    assert "secret=[...]" in final_message
    # Assert that other arguments remained untouched
    assert "Request GET" in final_message
    assert "for user_id 12345" in final_message
