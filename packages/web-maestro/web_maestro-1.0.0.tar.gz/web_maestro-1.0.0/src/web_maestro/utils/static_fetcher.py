"""Static HTML fetching functionality for web_maestro.

This module provides fast, lightweight HTML fetching without JavaScript
execution, suitable for simple content extraction.
"""

import logging
from typing import Union
from urllib.parse import urlparse

import aiohttp

from ..models.types import CapturedBlock
from .html_processor import CapturedBlockHTMLProcessor as HTMLProcessor

logger = logging.getLogger(__name__)

# Enhanced headers for better HTML fetching
ENHANCED_HTML_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


def validate_url(url: str) -> bool:
    """Validate that URL is properly formatted."""
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


async def try_static_first(
    url: str,
    timeout: int = 10,
    follow_redirects: bool = True,
    max_redirects: int = 5,
) -> Union[list[CapturedBlock], None]:
    """Attempts a fast, static HTML fetch with enhanced parsing and cleaning.

    Args:
        url: Target URL to fetch. Must be an absolute URL with http/https scheme.
        timeout: Maximum timeout in seconds. Defaults to 10.
        follow_redirects: Whether to follow redirects. Defaults to True.
        max_redirects: Maximum number of redirects to follow. Defaults to 5.

    Returns:
        A list of CapturedBlock objects, or None on failure.
    """
    if not validate_url(url):
        logger.warning(f"Invalid URL: {url}")
        return None

    logger.info(f"⚡ Fetching static HTML: {url}")

    try:
        # Create timeout for this specific request
        request_timeout = aiohttp.ClientTimeout(total=timeout)

        async with aiohttp.ClientSession(
            timeout=request_timeout, headers=ENHANCED_HTML_HEADERS
        ) as session:
            async with session.get(
                url,
                allow_redirects=follow_redirects,
                max_redirects=max_redirects,
                ssl=False,  # Consider making this configurable
            ) as response:
                # Store response details before closing
                status = response.status
                headers = dict(response.headers)
                final_url = str(response.url)
                charset = response.charset

                # Log redirects
                if response.history:
                    logger.info(
                        f"Followed {len(response.history)} redirects to {final_url}"
                    )

                if status != 200:
                    logger.warning(f"HTTP {status} for {url}")
                    return None

                # Stream and process large responses
                content_length = headers.get("Content-Length")
                if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB
                    logger.info(
                        f"Large response detected ({content_length} bytes), using streaming"
                    )
                    chunks = []
                    async for chunk in response.content.iter_chunked(8192):
                        chunks.append(chunk)
                    raw_content = b"".join(chunks)
                else:
                    raw_content = await response.read()

                encoding = HTMLProcessor.detect_encoding(
                    raw_content, charset, headers.get("Content-Type", "")
                )
                html = HTMLProcessor.decode_html(raw_content, encoding)

                if not html.strip():
                    return None

                # Process into multiple formats
                blocks = HTMLProcessor.create_blocks(html, final_url)

                logger.info(f"✅ Successfully fetched {len(blocks)} blocks from {url}")
                return blocks

    except aiohttp.ClientError as e:
        logger.warning(f"Client error during HTML fetch: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during HTML fetch: {e}")
        return None


# Backward compatibility alias
try_static_request_first = try_static_first
