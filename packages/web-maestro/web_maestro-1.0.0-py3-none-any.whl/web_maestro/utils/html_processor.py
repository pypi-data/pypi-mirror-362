"""HTML processing utilities for web_maestro.

This module contains the HTMLProcessor class that creates CapturedBlock instances.
It provides HTML parsing, cleaning, and content extraction functionality.
"""

import logging
from typing import ClassVar, Union
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import chardet

from ..models.types import CapturedBlock

logger = logging.getLogger(__name__)


class CapturedBlockHTMLProcessor:
    """Process HTML content into CapturedBlock formats.

    This is the HTMLProcessor that creates CapturedBlock instances,
    migrated from utils/fetch.py to avoid circular dependencies.
    """

    # Cache parsed BeautifulSoup objects to avoid re-parsing
    _soup_cache: ClassVar[dict[int, BeautifulSoup]] = {}
    _cache_size_limit: ClassVar[int] = 50

    @classmethod
    def _get_cached_soup(cls, html: str) -> BeautifulSoup:
        """Get or create a cached BeautifulSoup object."""
        html_hash = hash(html)

        if html_hash not in cls._soup_cache:
            # Limit cache size
            if len(cls._soup_cache) >= cls._cache_size_limit:
                # Remove oldest entries (simple FIFO)
                oldest_key = next(iter(cls._soup_cache))
                del cls._soup_cache[oldest_key]

            # Use lxml parser if available for better performance
            try:
                cls._soup_cache[html_hash] = BeautifulSoup(html, "lxml")
            except Exception:
                cls._soup_cache[html_hash] = BeautifulSoup(html, "html.parser")

        return cls._soup_cache[html_hash]

    @staticmethod
    def detect_encoding(
        raw_content: bytes, response_charset: Union[str, None], content_type_header: str
    ) -> str:
        """Detect the correct encoding for HTML content.

        Args:
            raw_content: Raw bytes of HTML
            response_charset: Charset from response
            content_type_header: Content-Type header value

        Returns:
            Detected encoding string
        """
        # Try response charset first
        if response_charset:
            return response_charset

        # Try content-type header
        if "charset=" in content_type_header:
            return content_type_header.split("charset=")[-1].strip()

        # Fall back to chardet with sampling for performance
        sample_size = min(len(raw_content), 10000)  # Only check first 10KB
        detected = chardet.detect(raw_content[:sample_size])
        encoding = detected.get("encoding", "utf-8")
        confidence = detected.get("confidence", 0)

        if confidence > 0.7:  # Only trust high confidence results
            logger.debug(f"Detected encoding: {encoding} (confidence: {confidence})")
            return encoding

        return "utf-8"  # Safe default

    @staticmethod
    def decode_html(raw_content: bytes, encoding: str) -> str:
        """Decode HTML content with fallback handling.

        Args:
            raw_content: Raw HTML bytes
            encoding: Encoding to try first

        Returns:
            Decoded HTML string
        """
        try:
            return raw_content.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            logger.warning(
                f"Failed to decode with {encoding}, using utf-8 with error replacement"
            )
            return raw_content.decode("utf-8", errors="replace")

    @classmethod
    def create_blocks(
        cls, html: str, base_url: str, lightweight: bool = False
    ) -> list[CapturedBlock]:
        """Create multiple processed versions of HTML content.

        Args:
            html: Raw HTML string
            base_url: Base URL for resolving relative links
            lightweight: Skip heavy processing steps

        Returns:
            List of CapturedBlock objects with different processing levels
        """
        blocks = []

        # Always include raw HTML
        blocks.append(
            CapturedBlock(
                content=html.strip(), source_id="full_html_raw", capture_type="html"
            )
        )

        if lightweight:
            return blocks

        try:
            # Get cached soup object
            soup = cls._get_cached_soup(html)

            # Light cleaning version
            blocks.extend(cls._create_light_clean_blocks(html, base_url, soup))

            # Text extraction
            text_block = cls._extract_text(soup)
            if text_block:
                blocks.append(text_block)

            # Structured data extraction
            blocks.extend(cls._extract_structured_data(soup))

        except Exception as e:
            logger.warning(f"Error processing HTML: {e}. Using raw HTML only.")

        return blocks

    @classmethod
    def _create_light_clean_blocks(
        cls, html: str, base_url: str, soup: Union[BeautifulSoup, None] = None
    ) -> list[CapturedBlock]:
        """Create lightly cleaned HTML with fixed URLs."""
        blocks = []

        try:
            if soup is None:
                soup = cls._get_cached_soup(html)

            # Clone soup to avoid modifying cache
            soup = BeautifulSoup(str(soup), "html.parser")

            # Remove only styles and comments
            for element in soup(["style"]):
                element.decompose()

            # Remove comments efficiently
            for comment in soup.find_all(
                string=lambda text: isinstance(text, str)
                and text.strip().startswith("<!--")
            ):
                comment.extract()

            # Fix relative URLs - batch process for efficiency
            url_mappings = []
            for tag_name, attr_name in [
                ("a", "href"),
                ("img", "src"),
                ("link", "href"),
            ]:
                for tag in soup.find_all(tag_name):
                    if tag.get(attr_name):
                        original = tag[attr_name]
                        resolved = urljoin(base_url, original)
                        if original != resolved:
                            url_mappings.append((tag, attr_name, resolved))

            # Apply URL fixes
            for tag, attr_name, resolved_url in url_mappings:
                tag[attr_name] = resolved_url

            blocks.append(
                CapturedBlock(
                    content=str(soup),
                    source_id="full_html_light_clean",
                    capture_type="html",
                )
            )

        except Exception as e:
            logger.debug(f"Light cleaning failed: {e}")

        return blocks

    @staticmethod
    def _extract_text(soup: BeautifulSoup) -> Union[CapturedBlock, None]:
        """Extract visible text from HTML."""
        try:
            # Clone soup to avoid modifying original
            soup_copy = BeautifulSoup(str(soup), "html.parser")

            # Remove script, style, and noscript elements
            for element in soup_copy(["script", "style", "noscript"]):
                element.decompose()

            # Extract text with proper spacing - more efficient approach
            text_content = soup_copy.get_text(separator="\n", strip=True)

            if text_content:
                return CapturedBlock(
                    content=text_content,
                    source_id="extracted_text",
                    capture_type="text",
                )

        except Exception as e:
            logger.debug(f"Text extraction failed: {e}")

        return None

    @staticmethod
    def _extract_structured_data(soup: BeautifulSoup) -> list[CapturedBlock]:
        """Extract structured data like JSON-LD and data-rich scripts."""
        blocks = []

        # Extract JSON-LD
        json_ld_scripts = soup.find_all("script", type="application/ld+json")
        for i, script in enumerate(json_ld_scripts):
            if script.string:
                blocks.append(
                    CapturedBlock(
                        content=script.string.strip(),
                        source_id=f"json_ld_{i}",
                        capture_type="structured_data",
                    )
                )

        # Extract potentially data-rich scripts more efficiently
        data_keywords = {"menu", "product", "item", "price", "catalog", "inventory"}
        data_scripts = []

        for script in soup.find_all("script"):
            if script.string:
                script_lower = script.string.lower()
                # Use set intersection for faster keyword matching
                if any(keyword in script_lower for keyword in data_keywords):
                    data_scripts.append(script.string)

        if data_scripts:
            blocks.append(
                CapturedBlock(
                    content="\n\n".join(data_scripts),
                    source_id="potential_data_scripts",
                    capture_type="scripts",
                )
            )

        return blocks
