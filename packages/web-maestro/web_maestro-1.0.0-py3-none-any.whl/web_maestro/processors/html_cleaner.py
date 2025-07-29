"""HTML cleaning utility for efficient text extraction.

This module provides configurable HTML cleaning to remove unnecessary elements
like scripts, styles, and other non-content tags, significantly reducing the
amount of text to process during extraction.
"""

import logging
import re
from typing import Any, ClassVar

from bs4 import BeautifulSoup, Comment

logger = logging.getLogger(__name__)


class HTMLCleaner:
    """Clean HTML content by removing non-essential elements."""

    # Default tags to remove completely (including content)
    DEFAULT_REMOVE_TAGS: ClassVar[set[str]] = {
        "script",
        "style",
        "meta",
        "link",
        "noscript",
        "iframe",
        "embed",
        "object",
        "param",
        "source",
        "track",
        "canvas",
        "map",
        "area",
        "audio",
        "video",
    }

    # Tags to unwrap (keep content but remove tag)
    DEFAULT_UNWRAP_TAGS: ClassVar[set[str]] = {
        "font",
        "center",
        "b",
        "i",
        "u",
        "strong",
        "em",
        "mark",
        "small",
        "del",
        "ins",
        "sub",
        "sup",
    }

    # Attributes to remove from all tags
    DEFAULT_REMOVE_ATTRS: ClassVar[set[str]] = {
        "style",
        "onclick",
        "onload",
        "onmouseover",
        "onmouseout",
        "onfocus",
        "onblur",
        "onchange",
        "onsubmit",
        "onkeydown",
        "onkeyup",
        "onkeypress",
        "class",
        "id",
        "data-*",
    }

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize HTML cleaner with configuration.

        Args:
            config: Configuration dictionary with optional keys:
                - clean_level: 'minimal', 'moderate', 'aggressive' (default: 'moderate')
                - remove_tags: Set of additional tags to remove
                - keep_tags: Set of tags to explicitly keep
                - remove_attrs: Set of additional attributes to remove
                - keep_links: Whether to preserve link hrefs (default: True)
                - keep_images: Whether to preserve image info (default: True)
                - remove_comments: Whether to remove HTML comments (default: True)
                - remove_empty: Whether to remove empty tags (default: True)
                - normalize_whitespace: Whether to normalize whitespace (default: True)
        """
        self.config = config or {}
        self.clean_level = self.config.get("clean_level", "moderate")

        # Configure based on cleaning level
        self._configure_cleaning_level()

        # Apply custom configurations
        if "remove_tags" in self.config:
            self.remove_tags.update(self.config["remove_tags"])
        if "keep_tags" in self.config:
            self.remove_tags -= set(self.config["keep_tags"])
        if "unwrap_tags" in self.config:
            self.unwrap_tags.update(self.config["unwrap_tags"])
        if "remove_attrs" in self.config:
            self.remove_attrs.update(self.config["remove_attrs"])

        self.keep_links = self.config.get("keep_links", True)
        self.keep_images = self.config.get("keep_images", True)
        self.remove_comments = self.config.get("remove_comments", True)
        self.remove_empty = self.config.get("remove_empty", True)
        self.normalize_whitespace = self.config.get("normalize_whitespace", True)

        logger.info(f"Initialized HTMLCleaner with {self.clean_level} cleaning level")
        logger.debug(
            f"Remove tags: {len(self.remove_tags)}, Keep links: {self.keep_links}, "
            f"Keep images: {self.keep_images}"
        )

    def _configure_cleaning_level(self):
        """Configure cleaning parameters based on level."""
        if self.clean_level == "minimal":
            # Only remove scripts and styles
            self.remove_tags = {"script", "style", "noscript"}
            self.unwrap_tags = set()
            self.remove_attrs = {"onclick", "onload"}

        elif self.clean_level == "aggressive":
            # Remove almost everything except text
            self.remove_tags = self.DEFAULT_REMOVE_TAGS.copy()
            self.remove_tags.update({"svg", "img", "picture", "figure"})
            self.unwrap_tags = self.DEFAULT_UNWRAP_TAGS.copy()
            self.unwrap_tags.update({"a", "span", "div", "section", "article"})
            self.remove_attrs = {"*"}  # Remove all attributes

        else:  # moderate (default)
            self.remove_tags = self.DEFAULT_REMOVE_TAGS.copy()
            self.unwrap_tags = self.DEFAULT_UNWRAP_TAGS.copy()
            self.remove_attrs = self.DEFAULT_REMOVE_ATTRS.copy()

    def clean_html(self, html_content: str, source_url: str = "") -> str:
        """Clean HTML content according to configuration.

        Args:
            html_content: Raw HTML content
            source_url: Source URL for logging context

        Returns:
            Cleaned HTML with unnecessary elements removed
        """
        if not html_content:
            return ""

        logger.info(
            f"🧹 Cleaning HTML from {source_url or 'unknown source'} "
            f"(level: {self.clean_level})"
        )

        original_size = len(html_content)

        try:
            # Parse HTML
            soup = BeautifulSoup(html_content, "html.parser")

            # Remove comments
            if self.remove_comments:
                for comment in soup.find_all(
                    text=lambda text: isinstance(text, Comment)
                ):
                    comment.extract()

            # Remove specified tags completely
            for tag_name in self.remove_tags:
                for tag in soup.find_all(tag_name):
                    tag.decompose()

            # Unwrap specified tags (keep content)
            for tag_name in self.unwrap_tags:
                for tag in soup.find_all(tag_name):
                    tag.unwrap()

            # Process remaining tags
            for tag in soup.find_all(True):  # All tags
                # Remove unwanted attributes
                if self.remove_attrs:
                    attrs_to_remove = []
                    for attr in tag.attrs:
                        if "*" in self.remove_attrs or attr in self.remove_attrs:
                            attrs_to_remove.append(attr)
                        # Handle data-* attributes
                        elif "data-*" in self.remove_attrs and attr.startswith("data-"):
                            attrs_to_remove.append(attr)

                    for attr in attrs_to_remove:
                        del tag[attr]

                # Special handling for links
                if tag.name == "a" and self.keep_links:
                    # Keep href but remove other attributes
                    href = tag.get("href", "")
                    tag.attrs = {"href": href} if href else {}

                # Special handling for images
                if tag.name == "img" and self.keep_images:
                    # Keep src and alt
                    src = tag.get("src", "")
                    alt = tag.get("alt", "")
                    tag.attrs = {}
                    if src:
                        tag.attrs["src"] = src
                    if alt:
                        tag.attrs["alt"] = alt

            # Remove empty tags
            if self.remove_empty:
                # Multiple passes to handle nested empty tags
                for _ in range(3):
                    empty_tags = soup.find_all(
                        lambda tag: tag.name not in ["br", "hr", "img", "input"]
                        and not tag.get_text(strip=True)
                        and not tag.find_all(True)  # No child tags
                    )
                    for tag in empty_tags:
                        tag.decompose()

            # Convert back to string
            cleaned_html = str(soup)

            # Additional text cleaning
            if self.normalize_whitespace:
                # Remove excessive whitespace
                cleaned_html = re.sub(r"\s+", " ", cleaned_html)
                # Remove whitespace between tags
                cleaned_html = re.sub(r">\s+<", "><", cleaned_html)

            # Final check for empty/whitespace-only content
            if not cleaned_html.strip():
                cleaned_html = ""

            cleaned_size = len(cleaned_html)
            reduction_pct = (
                (1 - cleaned_size / original_size) * 100 if original_size > 0 else 0
            )

            logger.info(
                f"✨ HTML cleaned: {original_size:,} → {cleaned_size:,} chars "
                f"({reduction_pct:.1f}% reduction)"
            )

            # Log sample of what was removed
            if logger.isEnabledFor(logging.DEBUG):
                scripts_removed = html_content.count("<script") - cleaned_html.count(
                    "<script"
                )
                styles_removed = html_content.count("<style") - cleaned_html.count(
                    "<style"
                )
                logger.debug(
                    f"Removed: {scripts_removed} scripts, {styles_removed} styles"
                )

            return cleaned_html

        except Exception as e:
            logger.error(f"Error cleaning HTML: {e}")
            # Return original on error
            return html_content

    def extract_text_only(self, html_content: str) -> str:
        """Extract only visible text from HTML.

        Args:
            html_content: Raw HTML content

        Returns:
            Plain text with minimal formatting
        """
        if not html_content:
            return ""

        try:
            # First clean the HTML
            cleaned = self.clean_html(html_content)

            # Parse and extract text
            soup = BeautifulSoup(cleaned, "html.parser")

            # Get text with some structure preserved
            # Add newlines for block elements
            for tag in soup.find_all(
                ["p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr"]
            ):
                tag.append("\n")

            text = soup.get_text()

            # Clean up text
            if self.normalize_whitespace:
                # Remove excessive newlines
                text = re.sub(r"\n\s*\n", "\n\n", text)
                # Remove trailing spaces
                text = re.sub(r" +\n", "\n", text)
                text = re.sub(r"\n +", "\n", text)
                # Normalize spaces
                text = re.sub(r" +", " ", text)

            return text.strip()

        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return ""

    def get_stats(self) -> dict[str, Any]:
        """Get current configuration stats."""
        return {
            "clean_level": self.clean_level,
            "remove_tags_count": len(self.remove_tags),
            "unwrap_tags_count": len(self.unwrap_tags),
            "keep_links": self.keep_links,
            "keep_images": self.keep_images,
            "remove_comments": self.remove_comments,
            "normalize_whitespace": self.normalize_whitespace,
        }


def create_html_cleaner(config: dict[str, Any] | None = None) -> HTMLCleaner:
    """Factory function to create an HTML cleaner.

    Args:
        config: Optional configuration dict

    Returns:
        Configured HTMLCleaner instance
    """
    return HTMLCleaner(config)


# Convenience functions for common use cases
def clean_html_minimal(html_content: str, source_url: str = "") -> str:
    """Clean HTML with minimal processing (scripts and styles only).

    Args:
        html_content: Raw HTML content
        source_url: Source URL for logging context

    Returns:
        Minimally cleaned HTML
    """
    cleaner = HTMLCleaner({"clean_level": "minimal"})
    return cleaner.clean_html(html_content, source_url)


def clean_html_moderate(html_content: str, source_url: str = "") -> str:
    """Clean HTML with moderate processing (default).

    Args:
        html_content: Raw HTML content
        source_url: Source URL for logging context

    Returns:
        Moderately cleaned HTML
    """
    cleaner = HTMLCleaner({"clean_level": "moderate"})
    return cleaner.clean_html(html_content, source_url)


def clean_html_aggressive(html_content: str, source_url: str = "") -> str:
    """Clean HTML with aggressive processing (text-focused).

    Args:
        html_content: Raw HTML content
        source_url: Source URL for logging context

    Returns:
        Aggressively cleaned HTML
    """
    cleaner = HTMLCleaner({"clean_level": "aggressive"})
    return cleaner.clean_html(html_content, source_url)


def extract_text_from_html(html_content: str, clean_level: str = "moderate") -> str:
    """Extract plain text from HTML with configurable cleaning.

    Args:
        html_content: Raw HTML content
        clean_level: Cleaning level ('minimal', 'moderate', 'aggressive')

    Returns:
        Extracted plain text
    """
    cleaner = HTMLCleaner({"clean_level": clean_level})
    return cleaner.extract_text_only(html_content)
