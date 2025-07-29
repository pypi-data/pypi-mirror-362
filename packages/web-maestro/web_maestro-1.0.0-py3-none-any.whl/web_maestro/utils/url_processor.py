"""Enhanced URL processing utilities for web extraction.

This module provides enhanced versions of maestro's URL utilities with:
- URL normalization and validation
- Relative to absolute URL conversion
- File type detection and filtering
- URL deduplication and canonicalization
"""

import logging
import re
from typing import Optional
from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse

logger = logging.getLogger(__name__)


def validate_url_format(url: str) -> bool:
    """Validate URL format for browser navigation.

    Args:
        url: URL to validate

    Returns:
        True if valid, False otherwise
    """
    if not url or not isinstance(url, str):
        return False

    try:
        parsed = urlparse(url.strip())

        # Must have scheme and netloc
        if not parsed.scheme or not parsed.netloc:
            return False

        # Only HTTP/HTTPS
        if parsed.scheme not in ("http", "https"):
            return False

        # Basic domain validation
        domain = parsed.netloc.split(":")[0]
        if not re.match(r"^[a-zA-Z0-9.-]+$", domain):
            return False

        # Check for consecutive dots or leading/trailing dots
        if ".." in domain or domain.startswith(".") or domain.endswith("."):
            return False

        return True

    except Exception:
        return False


def normalize_url(
    url: str,
    remove_query: bool = False,
    remove_fragment: bool = True,
    lowercase_scheme_netloc: bool = True,
    sort_query: bool = False,
) -> str:
    """Normalize URL for deduplication and comparison.

    Args:
        url: URL to normalize
        remove_query: Remove query parameters
        remove_fragment: Remove URL fragment
        lowercase_scheme_netloc: Convert scheme and netloc to lowercase
        sort_query: Sort query parameters

    Returns:
        Normalized URL
    """
    if not url:
        return url

    try:
        original_url = url.strip()
        parsed = urlparse(original_url)

        # Preserve original case if needed
        if lowercase_scheme_netloc:
            scheme = parsed.scheme.lower()
            netloc = parsed.netloc.lower()
        else:
            # Extract original scheme from the URL since urlparse lowercases it
            scheme_end = original_url.find("://")
            if scheme_end > 0:
                scheme = original_url[:scheme_end]
            else:
                scheme = parsed.scheme
            netloc = parsed.netloc
        path = parsed.path
        query = parsed.query
        fragment = parsed.fragment

        # Remove trailing slash from path unless it's the root
        if path.endswith("/") and len(path) > 1:
            path = path.rstrip("/")

        # Handle query parameters
        if remove_query:
            query = ""
        elif sort_query and query:
            # Parse and sort query parameters
            params = parse_qs(query, keep_blank_values=True)
            sorted_params = sorted(params.items())
            query = urlencode(sorted_params, doseq=True)

        # Handle fragment
        if remove_fragment:
            fragment = ""

        # Reconstruct URL
        normalized = urlunparse((scheme, netloc, path, "", query, fragment))

        return normalized

    except Exception as e:
        logger.warning(f"Failed to normalize URL {url}: {e}")
        return url


def normalize_url_for_navigation(url: str, base_url: str) -> str:
    """Convert relative URLs to absolute URLs for navigation.

    Args:
        url: URL to normalize (may be relative)
        base_url: Base URL for resolving relative URLs

    Returns:
        Absolute URL
    """
    if not url:
        return url

    try:
        # Handle already absolute URLs
        if url.startswith(("http://", "https://")):
            return normalize_url(url)

        # Handle protocol-relative URLs
        if url.startswith("//"):
            parsed_base = urlparse(base_url)
            return f"{parsed_base.scheme}:{url}"

        # Handle relative URLs
        absolute_url = urljoin(base_url, url)
        return normalize_url(absolute_url)

    except Exception as e:
        logger.warning(f"Failed to normalize URL {url} with base {base_url}: {e}")
        return url


def is_downloadable_file_url(url: str) -> bool:
    """Detect if URL points to a downloadable file.

    Args:
        url: URL to check

    Returns:
        True if URL points to downloadable file
    """
    if not url:
        return False

    # Common downloadable file extensions
    downloadable_extensions = {
        # Documents
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".txt",
        ".rtf",
        ".odt",
        ".ods",
        ".odp",
        # Images
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".tiff",
        ".svg",
        ".webp",
        # Audio/Video
        ".mp3",
        ".wav",
        ".mp4",
        ".avi",
        ".mkv",
        ".mov",
        ".wmv",
        ".flv",
        # Archives
        ".zip",
        ".rar",
        ".tar",
        ".gz",
        ".7z",
        ".bz2",
        # Executables
        ".exe",
        ".msi",
        ".dmg",
        ".deb",
        ".rpm",
        ".apk",
        # Data
        ".json",
        ".xml",
        ".csv",
        ".sql",
    }

    try:
        parsed = urlparse(url.lower())
        path = parsed.path

        # Check file extension
        for ext in downloadable_extensions:
            if path.endswith(ext):
                return True

        return False

    except Exception:
        return False


def extract_base_url(url: str) -> str:
    """Extract base URL (protocol + domain).

    Args:
        url: Full URL

    Returns:
        Base URL (e.g., 'https://example.com')
    """
    if not url:
        return ""

    try:
        parsed = urlparse(url)
        # Validate that we have proper scheme and netloc
        if not parsed.scheme or not parsed.netloc:
            return ""
        return f"{parsed.scheme}://{parsed.netloc}"
    except Exception:
        return ""


def get_url_path_key(url: str) -> str:
    """Extract normalized path for deduplication.

    Args:
        url: URL to extract path from

    Returns:
        Normalized path key
    """
    if not url:
        return ""

    try:
        parsed = urlparse(url.lower())
        # Validate that this is a proper URL
        if not parsed.scheme or not parsed.netloc:
            return ""

        path = parsed.path

        # Normalize path
        if path.endswith("/") and len(path) > 1:
            path = path.rstrip("/")

        if not path:
            path = "/"

        return path

    except Exception:
        return ""


def format_url_for_display(url: str, max_length: int = 80) -> str:
    """Format URL for user-friendly display.

    Args:
        url: URL to format
        max_length: Maximum display length

    Returns:
        Formatted URL for display
    """
    if not url:
        return ""

    if len(url) <= max_length:
        return url

    try:
        parsed = urlparse(url)

        # Show domain + path truncated
        display_url = f"{parsed.netloc}{parsed.path}"

        if len(display_url) > max_length - 3:  # Reserve space for "..."
            domain = parsed.netloc

            # If domain itself is too long, truncate it
            if len(domain) > max_length - 3:
                display_url = domain[: max_length - 3] + "..."
            else:
                remaining = max_length - len(domain) - 6  # "..." + "..."

                if remaining > 10 and parsed.path:
                    path_start = parsed.path[: remaining // 2]
                    path_end = parsed.path[-(remaining // 2) :]
                    display_url = f"{domain}{path_start}...{path_end}"
                else:
                    display_url = f"{domain}..."

        return display_url

    except Exception:
        # Fallback to simple truncation
        return url[: max_length - 3] + "..."


def extract_domain(url: str) -> str:
    """Extract domain from URL.

    Args:
        url: URL to extract domain from

    Returns:
        Domain name
    """
    if not url:
        return ""

    try:
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except Exception:
        return ""


def get_url_depth(url: str) -> int:
    """Get URL path depth (number of path segments).

    Args:
        url: URL to analyze

    Returns:
        Path depth
    """
    if not url:
        return 0

    try:
        parsed = urlparse(url)
        # For invalid URLs, return 0
        if not parsed.scheme:
            return 0

        path = parsed.path.strip("/")

        if not path:
            return 0

        segments = [seg for seg in path.split("/") if seg]
        return len(segments)

    except Exception:
        return 0


def is_same_domain(url1: str, url2: str) -> bool:
    """Check if two URLs are from the same domain.

    Args:
        url1: First URL
        url2: Second URL

    Returns:
        True if same domain
    """
    domain1 = extract_domain(url1)
    domain2 = extract_domain(url2)

    return bool(domain1 and domain2 and domain1 == domain2)


def filter_urls_by_patterns(
    urls: list[str],
    include_patterns: Optional[list[str]] = None,
    exclude_patterns: Optional[list[str]] = None,
) -> list[str]:
    """Filter URLs by regex patterns.

    Args:
        urls: List of URLs to filter
        include_patterns: Regex patterns that URLs must match
        exclude_patterns: Regex patterns that URLs must not match

    Returns:
        Filtered list of URLs
    """
    if not urls:
        return []

    filtered = []

    for url in urls:
        # Check include patterns
        if include_patterns:
            include_match = any(
                re.search(pattern, url, re.IGNORECASE) for pattern in include_patterns
            )
            if not include_match:
                continue

        # Check exclude patterns
        if exclude_patterns:
            exclude_match = any(
                re.search(pattern, url, re.IGNORECASE) for pattern in exclude_patterns
            )
            if exclude_match:
                continue

        filtered.append(url)

    return filtered


def deduplicate_urls(
    urls: list[str], normalize_first: bool = True, preserve_order: bool = True
) -> list[str]:
    """Remove duplicate URLs from list.

    Args:
        urls: List of URLs to deduplicate
        normalize_first: Normalize URLs before deduplication
        preserve_order: Preserve original order

    Returns:
        Deduplicated list of URLs
    """
    if not urls:
        return []

    seen: set[str] = set()
    result = []

    for url in urls:
        # Normalize if requested
        key = normalize_url(url) if normalize_first else url

        if key not in seen:
            seen.add(key)
            result.append(url)  # Keep original URL
        elif not preserve_order:
            # If not preserving order, we could do additional processing
            pass

    return result


class URLProcessor:
    """Enhanced URL processor with caching and batch operations."""

    def __init__(self):
        self._normalization_cache = {}
        self._validation_cache = {}

    def normalize_cached(self, url: str, **kwargs) -> str:
        """Normalize URL with caching."""
        cache_key = f"{url}:{str(sorted(kwargs.items()))}"

        if cache_key in self._normalization_cache:
            return self._normalization_cache[cache_key]

        normalized = normalize_url(url, **kwargs)
        self._normalization_cache[cache_key] = normalized

        return normalized

    def validate_cached(self, url: str) -> bool:
        """Validate URL with caching."""
        if url in self._validation_cache:
            return self._validation_cache[url]

        is_valid = validate_url_format(url)
        self._validation_cache[url] = is_valid

        return is_valid

    def process_url_list(
        self,
        urls: list[str],
        normalize: bool = True,
        deduplicate: bool = True,
        filter_invalid: bool = True,
        include_patterns: Optional[list[str]] = None,
        exclude_patterns: Optional[list[str]] = None,
    ) -> list[str]:
        """Process a list of URLs with multiple operations.

        Args:
            urls: List of URLs to process
            normalize: Whether to normalize URLs
            deduplicate: Whether to remove duplicates
            filter_invalid: Whether to filter invalid URLs
            include_patterns: Regex patterns for inclusion
            exclude_patterns: Regex patterns for exclusion

        Returns:
            Processed list of URLs
        """
        if not urls:
            return []

        result = urls.copy()

        # Filter invalid URLs
        if filter_invalid:
            result = [url for url in result if self.validate_cached(url)]

        # Apply include/exclude patterns
        if include_patterns or exclude_patterns:
            result = filter_urls_by_patterns(result, include_patterns, exclude_patterns)

        # Normalize URLs
        if normalize:
            result = [self.normalize_cached(url) for url in result]

        # Deduplicate
        if deduplicate:
            result = deduplicate_urls(
                result, normalize_first=False
            )  # Already normalized

        return result

    def clear_cache(self):
        """Clear processing caches."""
        self._normalization_cache.clear()
        self._validation_cache.clear()

    def get_cache_stats(self):
        """Get cache statistics."""
        return {
            "normalization_cache_size": len(self._normalization_cache),
            "validation_cache_size": len(self._validation_cache),
        }
