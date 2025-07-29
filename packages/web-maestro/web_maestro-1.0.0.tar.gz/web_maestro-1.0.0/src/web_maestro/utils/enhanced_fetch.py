"""Enhanced HTTP fetching utilities with production-ready features.

This module provides enhanced versions of maestro's fetch utilities with:
- Better error handling and retry logic
- Improved caching and connection pooling
- Rate limiting and concurrent request management
- Multi-format content processing
"""

import asyncio
import hashlib
import logging
import threading
import time
from typing import Any, Optional
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup
import chardet
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)

# Enhanced headers for better compatibility
ENHANCED_HTML_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; WebMaestro/2.0; +https://github.com/mx-maestro)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
}

# Global cache and session management
_thread_local = threading.local()
_session_lock = None
_response_cache: dict[str, tuple[Any, float]] = {}
_cache_ttl = 300  # 5 minutes default TTL


def get_session_lock():
    """Get or create the session lock for the current event loop."""
    global _session_lock
    if _session_lock is None:
        _session_lock = asyncio.Lock()
    return _session_lock


def validate_url(url: str) -> bool:
    """Check if a URL is absolute and uses HTTP/HTTPS protocol."""
    try:
        parsed = urlparse(url)
        return bool(parsed.netloc and parsed.scheme in {"http", "https"})
    except Exception:
        return False


def _get_cache_key(url: str, operation: str = "") -> str:
    """Generate a cache key for a URL and operation."""
    return hashlib.sha256(f"{url}:{operation}".encode()).hexdigest()


def _get_from_cache(cache_key: str) -> Any:
    """Get value from cache if not expired."""
    if cache_key in _response_cache:
        value, timestamp = _response_cache[cache_key]
        if time.time() - timestamp < _cache_ttl:
            return value
        else:
            del _response_cache[cache_key]
    return None


def _set_cache(cache_key: str, value: Any) -> None:
    """Set value in cache with current timestamp."""
    _response_cache[cache_key] = (value, time.time())


class ContentBlock:
    """Represents a block of processed content."""

    def __init__(
        self,
        content: str,
        content_type: str,
        source_url: str,
        processing_method: str = "static",
        metadata: Optional[dict[str, Any]] = None,
    ):
        self.content = content
        self.content_type = content_type
        self.source_url = source_url
        self.processing_method = processing_method
        self.metadata = metadata or {}
        self.token_count = len(content.split()) if content else 0

    def preview(self, length: int = 100) -> str:
        """Get a preview of the content."""
        if len(self.content) <= length:
            return self.content
        return self.content[:length] + "..."

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "content": self.content,
            "content_type": self.content_type,
            "source_url": self.source_url,
            "processing_method": self.processing_method,
            "token_count": self.token_count,
            "metadata": self.metadata,
        }


class HTMLProcessor:
    """Enhanced HTML processing with multiple output formats."""

    @staticmethod
    def detect_encoding(
        raw_content: bytes, charset: Optional[str], content_type: str
    ) -> str:
        """Detect the encoding of HTML content."""
        # Try charset from HTTP headers first
        if charset:
            try:
                raw_content.decode(charset)
                return charset
            except (UnicodeDecodeError, LookupError):
                pass

        # Try to detect encoding from content
        try:
            detected = chardet.detect(raw_content)
            if detected["encoding"] and detected["confidence"] > 0.7:
                return detected["encoding"]
        except Exception as e:
            logging.debug(f"Character encoding detection failed: {e}")

        # Fallback to UTF-8
        return "utf-8"

    @staticmethod
    def decode_html(raw_content: bytes, encoding: str) -> str:
        """Decode HTML content with fallback handling."""
        try:
            return raw_content.decode(encoding)
        except UnicodeDecodeError:
            try:
                return raw_content.decode("utf-8", errors="ignore")
            except UnicodeDecodeError:
                return raw_content.decode("latin-1", errors="ignore")

    @staticmethod
    def create_blocks(html: str, url: str) -> list[ContentBlock]:
        """Create multiple content blocks from HTML."""
        blocks = []

        # 1. Raw HTML block
        blocks.append(
            ContentBlock(
                content=html[:10000],  # Limit for efficiency
                content_type="raw_html",
                source_url=url,
                processing_method="static",
                metadata={"truncated": len(html) > 10000},
            )
        )

        # 2. Parse HTML
        try:
            soup = BeautifulSoup(html, "html.parser")

            # 3. Clean HTML block (remove scripts, styles)
            for tag in soup(["script", "style", "noscript", "iframe"]):
                tag.decompose()

            clean_html = str(soup)
            blocks.append(
                ContentBlock(
                    content=clean_html,
                    content_type="clean_html",
                    source_url=url,
                    processing_method="static",
                )
            )

            # 4. Text-only block
            text_content = soup.get_text(separator=" ", strip=True)
            # Clean up whitespace
            text_content = " ".join(text_content.split())

            blocks.append(
                ContentBlock(
                    content=text_content,
                    content_type="text",
                    source_url=url,
                    processing_method="static",
                )
            )

            # 5. Structured data block (JSON-LD, meta tags, etc.)
            structured_data = HTMLProcessor._extract_structured_data(soup)
            if structured_data:
                blocks.append(
                    ContentBlock(
                        content=str(structured_data),
                        content_type="structured_data",
                        source_url=url,
                        processing_method="static",
                        metadata={"data_types": list(structured_data.keys())},
                    )
                )

        except Exception as e:
            logger.warning(f"Error processing HTML for {url}: {e}")
            # Add error block
            blocks.append(
                ContentBlock(
                    content=f"HTML processing error: {e}",
                    content_type="error",
                    source_url=url,
                    processing_method="static",
                    metadata={"error": str(e)},
                )
            )

        return blocks

    @staticmethod
    def _extract_structured_data(soup: BeautifulSoup) -> dict[str, Any]:
        """Extract structured data from HTML."""
        structured = {}

        # JSON-LD
        json_ld_scripts = soup.find_all("script", type="application/ld+json")
        if json_ld_scripts:
            import json

            json_ld_data = []
            for script in json_ld_scripts:
                try:
                    data = json.loads(script.string)
                    json_ld_data.append(data)
                except json.JSONDecodeError:
                    continue
            if json_ld_data:
                structured["json_ld"] = json_ld_data

        # Meta tags
        meta_tags = {}
        for meta in soup.find_all("meta"):
            name = meta.get("name") or meta.get("property")
            content = meta.get("content")
            if name and content:
                meta_tags[name] = content

        if meta_tags:
            structured["meta_tags"] = meta_tags

        # Title
        title = soup.find("title")
        if title:
            structured["title"] = title.get_text(strip=True)

        return structured


class HTTPClient:
    """Enhanced async HTTP client with connection pooling and retry logic."""

    def __init__(
        self,
        timeout: int = 30,
        headers: Optional[dict[str, str]] = None,
        max_retries: int = 3,
        max_concurrent: int = 10,
        enable_cache: bool = True,
    ):
        self.timeout_seconds = timeout
        self.headers = headers or ENHANCED_HTML_HEADERS
        self.max_retries = max_retries
        self.max_concurrent = max_concurrent
        self.enable_cache = enable_cache

        # Create semaphore for concurrency control
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self._session: Optional[aiohttp.ClientSession] = None

    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session with connection pooling."""
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(
                limit=100,
                limit_per_host=30,
                ttl_dns_cache=300,
                enable_cleanup_closed=True,
                force_close=False,
                keepalive_timeout=30,
            )

            timeout = aiohttp.ClientTimeout(total=self.timeout_seconds)

            self._session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers=self.headers,
                raise_for_status=False,
            )

        return self._session

    async def close(self):
        """Close the HTTP session."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class EnhancedFetcher:
    """Enhanced fetcher with static-first strategy and intelligent fallback."""

    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 3,
        enable_cache: bool = True,
        cache_ttl: int = 300,
    ):
        self.timeout = timeout
        self.max_retries = max_retries
        self.enable_cache = enable_cache
        global _cache_ttl
        _cache_ttl = cache_ttl

        self._client: Optional[HTTPClient] = None

    async def _get_client(self) -> HTTPClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = HTTPClient(
                timeout=self.timeout, max_retries=self.max_retries
            )
        return self._client

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError)),
    )
    async def try_static_first(
        self, url: str, follow_redirects: bool = True, max_redirects: int = 5
    ) -> Optional[list[ContentBlock]]:
        """Try static fetch first with enhanced processing."""
        if not validate_url(url):
            logger.warning(f"Invalid URL: {url}")
            return None

        # Check cache
        cache_key = _get_cache_key(url, "enhanced_html")
        if self.enable_cache:
            cached = _get_from_cache(cache_key)
            if cached is not None:
                logger.debug(f"Cache hit for enhanced HTML: {url}")
                return cached

        logger.info(f"⚡ Fetching enhanced HTML: {url}")

        client = await self._get_client()
        session = await client.get_session()

        try:
            async with client.semaphore:
                async with session.get(
                    url,
                    allow_redirects=follow_redirects,
                    max_redirects=max_redirects,
                    ssl=False,  # Consider making configurable
                ) as response:
                    if response.status != 200:
                        logger.warning(f"HTTP {response.status} for {url}")
                        return None

                    # Read content
                    raw_content = await response.read()

                    # Detect encoding
                    charset = response.charset
                    content_type = response.headers.get("Content-Type", "")
                    encoding = HTMLProcessor.detect_encoding(
                        raw_content, charset, content_type
                    )

                    # Decode HTML
                    html = HTMLProcessor.decode_html(raw_content, encoding)

                    if not html.strip():
                        return None

                    # Process into blocks
                    blocks = HTMLProcessor.create_blocks(html, str(response.url))

                    # Cache the result
                    if self.enable_cache:
                        _set_cache(cache_key, blocks)

                    logger.info(
                        f"✅ Enhanced HTML fetch successful: {len(blocks)} blocks created"
                    )
                    return blocks

        except Exception as e:
            logger.error(f"Enhanced fetch failed for {url}: {e}")
            return None

    async def fetch_html(self, url: str) -> Optional[str]:
        """Simple HTML fetch for compatibility."""
        blocks = await self.try_static_first(url)
        if blocks:
            # Return the clean HTML block if available
            for block in blocks:
                if block.content_type == "clean_html":
                    return block.content
            # Fallback to first block
            return blocks[0].content if blocks else None
        return None

    async def get_content_type(self, url: str) -> str:
        """Get content type via HEAD request."""
        if not validate_url(url):
            return "text/html"

        client = await self._get_client()
        session = await client.get_session()

        try:
            async with session.head(url) as response:
                return response.headers.get("Content-Type", "text/html").split(";")[0]
        except Exception:
            return "text/html"  # Default fallback

    async def check_url_accessible(self, url: str) -> bool:
        """Check if URL is accessible."""
        if not validate_url(url):
            return False

        client = await self._get_client()
        session = await client.get_session()

        try:
            async with session.head(url) as response:
                return 200 <= response.status < 400
        except Exception:
            return False

    def needs_javascript(self, html: str) -> bool:
        """Detect if page likely requires JavaScript."""
        if not html:
            return True

        # Check for SPA frameworks
        spa_indicators = [
            'id="root"',
            'id="app"',
            "ng-app",
            "data-reactroot",
            "__NEXT_DATA__",
            "window.__INITIAL_STATE__",
        ]

        html_lower = html.lower()
        return any(indicator.lower() in html_lower for indicator in spa_indicators)

    def has_sufficient_content(self, blocks: list[ContentBlock]) -> bool:
        """Check if static content is sufficient."""
        if not blocks:
            return False

        # Find text block
        text_blocks = [b for b in blocks if b.content_type == "text"]
        if not text_blocks:
            return False

        text = text_blocks[0].content.lower()

        # Check for indicators of incomplete content
        insufficient_indicators = [
            "loading",
            "please wait",
            "javascript required",
            "enable javascript",
            "noscript",
        ]

        return not any(indicator in text for indicator in insufficient_indicators)

    async def close(self):
        """Close the fetcher and cleanup resources."""
        if self._client:
            await self._client.close()
