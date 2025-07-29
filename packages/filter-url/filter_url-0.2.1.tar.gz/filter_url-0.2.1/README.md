filter-url
==========

![PyPI](https://img.shields.io/pypi/v/filter-url.svg?style=flat-square) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/filter-url.svg?style=flat-square) ![License](https://img.shields.io/pypi/l/filter-url.svg?style=flat-square)

A simple, fast, and configurable Python utility to censor sensitive data (passwords, API keys, tokens) from URLs, making them safe for logging, monitoring, and debugging.

Key Features
------------

* **Comprehensive Censoring**: Censors passwords in userinfo (`user:[...]@host`), query parameter values, and parts of the URL path.
* **Flexible Rules**: Filter query parameters by exact key names or by powerful regular expressions.
* **Advanced Path Filtering**: Use regex with named capture groups to censor specific dynamic parts of a URL path while leaving the rest intact.
* **Order Preserving**: Guarantees that the order of query parameters in the output is identical to the input.
* **Logging Integration**: Provides a ready-to-use `logging.Filter` subclass for seamless integration into your application's logging setup.
* **Lightweight**: Zero external dependencies.

Installation
------------

    pip install filter-url

Quick Start
-----------

The quickest way to use the library is the standalone `filter_url()` function, which uses a default set of rules to catch common sensitive keys.

    from filter_url import filter_url

    dirty_url = "https://user:my-secret-password@example.com/data?token=abc-123-xyz"

    # Use the function with default filters
    clean_url = filter_url(dirty_url)

    print(clean_url)
    # >> https://user:[...]@example.com/data?token=[...]

Usage & Examples
----------------

### Basic Filtering (Standalone Function)

The `filter_url()` function is great for one-off tasks. You can pass your own filtering rules directly to it. If a rule is not provided, a sensible default is used.

    from filter_url import filter_url

    # Define custom rules
    custom_path_re = r'/user/(?P<user_id>\d+)/profile'

    dirty_url = "https://example.com/user/123456/profile?credit_card_number=5555"

    # Censor using a custom path regex
    clean_url = filter_url(
        url=dirty_url,
        bad_path_re=custom_path_re
    )

    print(clean_url)
    # >> https://example.com/user/[...]/profile?credit_card_number=5555

### Advanced: Using the `FilterURL` Class for Performance

When you need to filter a large number of URLs with the same configuration, it's much more efficient to instantiate the `FilterURL` class once. This pre-compiles the regular expressions and avoids redundant work in a loop.

    from filter_url import FilterURL

    # Create the filter instance ONCE with your custom rules.
    # The regexes are compiled here.
    my_filter = FilterURL(
        bad_keys={'api_key'},
        bad_keys_re=[r'session']
    )

    urls_to_process = [
        "https://service.com/api?api_key=key-1",
        "https://service.com/api?user_session=sess-2",
        "https://service.com/api?id=3"
    ]

    # Reuse the same instance in a loop for high performance
    clean_urls = [my_filter.remove_sensitive(url) for url in urls_to_process]

    # clean_urls will be:
    # [
    #   'https://service.com/api?api_key=[...]',
    #   'https://service.com/api?user_session=[...]',
    #   'https://service.com/api?id=3'
    # ]

### Integration with Python's `logging` Module

This is the most powerful feature for real-world applications. The `UrlFilteringFilter` automatically censors URLs in your logs. The filter works in two ways:
1. **(Preferred)** It looks for a `url` key in the `extra` dictionary of your logging call.
2. **(Fallback)** If `fallback=True` (the default), it searches for URLs in the positional arguments of the log message.


```python
    import logging
    import sys
    from filter_url import UrlFilteringFilter

    # 1. Configure a logger

    logger = logging.getLogger('my_app')
    logger.setLevel(logging.INFO)
    if logger.hasHandlers():
        logger.handlers.clear()

    # 2. Simply add our filter. Let's use custom rules for this example

    custom_filter = UrlFilteringFilter(
        bad_keys={'access_token'},
        fallback=True # Default, but shown for clarity
    )
    logger.addFilter(custom_filter)

    # 3. Use a standard Formatter. No special formatter is needed

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # --- Usage Examples ---

    # Case 1: (Preferred) Pass the URL via 'extra'

    logger.info(
        "User login attempt failed",
        extra={'url': "<https://auth.service.com/login?access_token=12345"}>
    )

    # Case 2: (Fallback) The URL is an argument in the message string

    logger.info(
        "API call to %s resulted in a 404 error.",
        "<https://api.service.com/data/v1/user?password=abc>"
    )

    # Case 3: No URL in the message. Nothing extra is added

    logger.info("Application started successfully.")
```

**Expected Output:**

    INFO: User login attempt failed | (URL data: https://auth.service.com/login?access_token=[...])
    INFO: API call to https://api.service.com/data/v1/user?password=[...] was made. | (URL data: https://api.service.com/data/v1/user?password=[...])
    INFO: Application started successfully.

Corner Cases & Considerations
-----------------------------

* **Log String vs. Valid URL**: The primary goal of this library is to produce a human-readable, safe string for logging. The output string containing `[...]` in the userinfo (password) section is not a valid URL according to RFC standards and may fail if you try to parse it again with `urllib.parse`.
* **Performance**: For filtering a large number of URLs, always instantiate the `FilterURL` class once and reuse the instance. The standalone `filter_url()` function re-compiles regexes on every call and is less performant for batch jobs.
* **Logging Filter Precedence**: When using `UrlFilteringFilter`, providing a URL in the `extra` dictionary is always the preferred method. The `fallback` search will only trigger if a `url` key is not found in `extra`.

API Reference
-------------

* `filter_url(url, censored, bad_keys, bad_keys_re, bad_path_re)`: A standalone function for one-off URL censoring.
* `FilterURL(bad_keys, bad_keys_re, bad_path_re)`: A class that holds a compiled filter configuration for efficient, repeated use.
  * `.remove_sensitive(url, censored)`: The method that performs the censoring.
* `UrlFilteringFilter(bad_keys, bad_keys_re, bad_path_re, fallback)`: A `logging.Filter` subclass for easy integration with Python's logging module.

License
-------

This project is licensed under the MIT License.
