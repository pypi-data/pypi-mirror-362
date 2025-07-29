# filterurl.py

"""
A small and efficient module to filter sensitive data from URLs for logging.
"""

import re
from re import Pattern
from typing import List, Optional, Set
from urllib.parse import parse_qsl, urlencode, urlparse

# ======================================================================
# Default filter settings that can be imported and used
# ======================================================================

DEFAULT_BAD_KEYS: Set[str] = {
    "password",
    "token",
    "key",
    "secret",
    "auth",
    "apikey",
    "credentials",
}

DEFAULT_BAD_KEYS_RE: List[str] = [
    r"session",
    r"csrf",
    r".*_secret",
    r".*_token",
    r".*_key",
]

DEFAULT_BAD_PATH_RE: Optional[str] = None

# ======================================================================
# The main class for filtering
# ======================================================================


# pylint: disable=R0903
class FilterURL:
    """
    A class that holds filtering configuration and performs URL censoring.

    It takes lists of uncompiled regular expressions during initialization
    and stores them as compiled objects for performance.
    """

    def __init__(
        self,
        bad_keys: Optional[Set[str]] = None,
        bad_keys_re: Optional[List[str]] = None,
        bad_path_re: Optional[str] = None,
    ):
        """
        Initializes the FilterURL instance.

        Args:
            bad_keys: A set of exact, case-insensitive keys to censor.
                      If None, uses DEFAULT_BAD_KEYS.
            bad_keys_re: A list of regex patterns to find sensitive keys.
                         If None, uses DEFAULT_BAD_KEYS_RE.
            bad_path_re: A regex pattern to find and censor parts of the URL path.
                         If None, uses DEFAULT_BAD_PATH_RE.
        """
        self.bad_keys: Set[str] = bad_keys if bad_keys is not None else DEFAULT_BAD_KEYS

        # Compile regexes for keys for efficient reuse
        keys_re_to_compile = (bad_keys_re if bad_keys_re is not None else DEFAULT_BAD_KEYS_RE)
        self.bad_keys_comp: List[Pattern] = [re.compile(p) for p in keys_re_to_compile]

        # Compile path regex if it exists
        path_re_to_compile = (bad_path_re if bad_path_re is not None else DEFAULT_BAD_PATH_RE)
        self.bad_path_comp: Optional[Pattern] = (
            re.compile(path_re_to_compile) if path_re_to_compile else None
        )

    # pylint: disable=too-many-locals, R0912
    def remove_sensitive(self, url: str, censored: str = "[...]") -> str:
        """
        Takes a URL and censors parts of it based on the filter's configuration.

        This method contains the core filtering logic.

        Args:
            url: The original URL string.
            censored: The string to use for replacing sensitive data.

        Returns:
            A new URL string with sensitive parts censored.
        """
        try:
            parsed = urlparse(url)
        except ValueError:  # Handle potential malformed URLs gracefully
            return "MALFORMED_URL"

        new_netloc = parsed.netloc
        new_path = parsed.path

        # Censor query string values (preserving order)
        qs_list = parse_qsl(parsed.query, keep_blank_values=True)
        censored_qs_list = []
        for k, v in qs_list:
            if k.lower() in self.bad_keys or any(
                r.search(k) for r in self.bad_keys_comp
            ):
                censored_qs_list.append((k, censored))
            else:
                censored_qs_list.append((k, v))
        new_query = urlencode(censored_qs_list, safe="[]")

        # Censor password in netloc
        if parsed.password:
            new_netloc = parsed.hostname or ""
            if parsed.username:
                new_netloc = f"{parsed.username}:{censored}@{new_netloc}"
            if parsed.port:
                new_netloc += f":{parsed.port}"

        # Censor path using the provided regex
        if self.bad_path_comp:
            match = self.bad_path_comp.search(new_path)
            if match:
                if match.groupdict():
                    temp_path_list = list(new_path)
                    for group_name in sorted(
                        self.bad_path_comp.groupindex.keys(), reverse=True
                    ):
                        start, end = match.span(group_name)
                        if start != -1 and end != -1:
                            temp_path_list[start:end] = list(censored)
                    new_path = "".join(temp_path_list)
                else:
                    new_path = self.bad_path_comp.sub(censored, new_path, count=1)

        return parsed._replace(
            netloc=new_netloc, query=new_query, path=new_path
        ).geturl()


# ======================================================================
# A convenient standalone function for one-off filtering
# ======================================================================

def filter_url(
    url: str,
    censored: str = "[...]",
    bad_keys: Optional[Set[str]] = None,
    bad_keys_re: Optional[List[str]] = None,
    bad_path_re: Optional[str] = None,
) -> str:
    """
    A convenience wrapper function that creates a one-time FilterURL instance
    and uses it to censor the given URL.

    Args:
        url: The original URL string.
        censored: The string to use for replacing sensitive data.
        bad_keys: A set of exact, case-insensitive keys to censor.
        bad_keys_re: A list of regex patterns to find sensitive keys.
        bad_path_re: A regex pattern to find and censor parts of the URL path.

    Returns:
        The censored URL string.
    """
    filter_instance = FilterURL(bad_keys, bad_keys_re, bad_path_re)
    return filter_instance.remove_sensitive(url, censored)
