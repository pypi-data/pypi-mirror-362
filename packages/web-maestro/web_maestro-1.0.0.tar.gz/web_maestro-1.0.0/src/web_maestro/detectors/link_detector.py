"""Generic Link Detection Framework with Abstract Base Class.

This module provides a flexible, extensible framework for detecting specific types
of content-related links in HTML. It uses an abstract base class that can be
specialized for different content types like menus, products, articles, etc.
"""

from abc import ABC, abstractmethod
import logging
import re
from typing import Any, Union
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class ContentLinkDetector(ABC):
    """Abstract base class for content-specific link detection."""

    def __init__(self, detection_config: Union[dict[str, Any], None] = None):
        """Initialize the link detector with configuration.

        Args:
            detection_config: Configuration for detection.
        """
        self.config = detection_config or {}
        self.confidence_threshold = self.config.get("confidence_threshold", 0.6)
        self.max_links = self.config.get("max_links", 20)

    @property
    @abstractmethod
    def positive_keywords(self) -> set[str]:
        """Keywords that indicate target content type."""
        pass

    @property
    @abstractmethod
    def negative_keywords(self) -> set[str]:
        """Keywords that indicate non-target content."""
        pass

    @property
    @abstractmethod
    def positive_path_patterns(self) -> list[str]:
        """Regex patterns for URL paths that likely contain target content."""
        pass

    @property
    @abstractmethod
    def target_file_extensions(self) -> set[str]:
        """File extensions that might contain target content."""
        pass

    @property
    @abstractmethod
    def content_type(self) -> str:
        """String identifier for the content type (e.g., 'menu', 'product')."""
        pass

    def analyze_link_for_content(
        self, url: str, link_text: str = "", context: str = "", base_url: str = ""
    ) -> dict[str, Any]:
        """Analyze a single link for target content potential.

        Args:
            url: The URL to analyze
            link_text: The anchor text of the link
            context: Surrounding text context
            base_url: Base URL for relative link resolution

        Returns:
            Dictionary with analysis results including score, reasoning, and confidence
        """
        # Resolve relative URLs
        if base_url and not url.startswith(("http://", "https://")):
            url = urljoin(base_url, url)

        parsed_url = urlparse(url)
        path = parsed_url.path.lower()
        query = parsed_url.query.lower()

        analysis = {
            "url": url,
            "is_likely_content": False,
            "confidence": 0.0,
            "score": 0.0,
            "reasoning": [],
            "category": "unknown",
            "content_type": self.content_type,
        }

        score = 0.0
        reasoning = []

        # 1. Analyze URL path
        path_score = self._analyze_url_path(path, reasoning)
        score += path_score

        # 2. Analyze query parameters
        query_score = self._analyze_query_params(query, reasoning)
        score += query_score

        # 3. Analyze link text
        text_score = self._analyze_link_text(link_text, reasoning)
        score += text_score

        # 4. Analyze context
        context_score = self._analyze_context(context, reasoning)
        score += context_score

        # 5. File extension bonus
        ext_score = self._analyze_file_extension(url, reasoning)
        score += ext_score

        # 6. Apply negative scoring
        negative_score = self._apply_negative_scoring(
            url, link_text, context, reasoning
        )
        score += negative_score

        # 7. Apply custom scoring rules
        custom_score = self._apply_custom_scoring(url, link_text, context, reasoning)
        score += custom_score

        # Normalize score to 0-1 range
        final_score = max(0.0, min(1.0, score / 10.0))

        # Determine if likely target content
        is_likely_content = final_score >= self.confidence_threshold
        confidence = final_score

        # Categorize the link
        category = self._categorize_link(url, link_text, final_score)

        analysis.update(
            {
                "is_likely_content": is_likely_content,
                "confidence": confidence,
                "score": final_score,
                "reasoning": reasoning,
                "category": category,
            }
        )

        return analysis

    def extract_content_links_from_html(
        self, html: str, base_url: str = "", max_links: Union[int, None] = None
    ) -> list[dict[str, Any]]:
        """Extract and analyze all potential content links from HTML.

        Args:
            html: HTML content to analyze
            base_url: Base URL for resolving relative links
            max_links: Maximum number of links to return (uses instance default if None)

        Returns:
            List of analyzed links sorted by content potential score
        """
        max_links = max_links or self.max_links
        soup = BeautifulSoup(html, "html.parser")
        analyzed_links = []

        # Find all anchor tags with href attributes
        links = soup.find_all("a", href=True)

        for link in links:
            href = link.get("href", "").strip()
            if not href or href.startswith(("#", "javascript:", "mailto:", "tel:")):
                continue

            # Get link text and context
            link_text = link.get_text(strip=True)

            # Get surrounding context (parent element text)
            context = ""
            if link.parent:
                context = link.parent.get_text(strip=True)

            # Analyze the link
            analysis = self.analyze_link_for_content(
                url=href, link_text=link_text, context=context, base_url=base_url
            )

            if analysis["score"] > 0.2:  # Only include links with some potential
                analyzed_links.append(analysis)

        # Sort by score (highest first) and limit results
        analyzed_links.sort(key=lambda x: x["score"], reverse=True)
        return analyzed_links[:max_links]

    def _analyze_url_path(self, path: str, reasoning: list[str]) -> float:
        """Analyze URL path for content indicators."""
        score = 0.0

        # Check positive path patterns
        for pattern in self.positive_path_patterns:
            if re.search(pattern, path):
                score += 3.0
                reasoning.append(
                    f"URL path matches {self.content_type} pattern: {pattern}"
                )
                break

        # Check for keywords in path
        for keyword in self.positive_keywords:
            if keyword in path:
                score += 1.5
                reasoning.append(
                    f"Path contains {self.content_type} keyword: '{keyword}'"
                )

        return score

    def _analyze_query_params(self, query: str, reasoning: list[str]) -> float:
        """Analyze query parameters for content indicators."""
        score = 0.0

        if not query:
            return score

        for keyword in self.positive_keywords:
            if keyword in query:
                score += 1.0
                reasoning.append(
                    f"Query contains {self.content_type} keyword: '{keyword}'"
                )

        return score

    def _analyze_link_text(self, link_text: str, reasoning: list[str]) -> float:
        """Analyze anchor text for content indicators."""
        if not link_text:
            return 0.0

        score = 0.0
        text_lower = link_text.lower().strip()

        # Check for keywords in link text
        for keyword in self.positive_keywords:
            if keyword in text_lower:
                # Give higher score for exact matches
                if keyword == text_lower:
                    score += 2.5
                    reasoning.append(
                        f"Link text exactly matches {self.content_type} keyword: '{keyword}'"
                    )
                else:
                    score += 1.0
                    reasoning.append(
                        f"Link text contains {self.content_type} keyword: '{keyword}'"
                    )

        return score

    def _analyze_context(self, context: str, reasoning: list[str]) -> float:
        """Analyze surrounding context for content indicators."""
        if not context:
            return 0.0

        score = 0.0
        context_lower = context.lower()

        for keyword in self.positive_keywords:
            if keyword in context_lower:
                score += 0.5
                reasoning.append(
                    f"Context contains {self.content_type} keyword: '{keyword}'"
                )

        return min(score, 2.0)  # Cap context score

    def _analyze_file_extension(self, url: str, reasoning: list[str]) -> float:
        """Analyze file extension for content potential."""
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()

        for ext in self.target_file_extensions:
            if path.endswith(ext):
                score = self._get_extension_score(ext)
                reasoning.append(
                    f"File extension {ext} indicates potential {self.content_type} content"
                )
                return score

        return 0.0

    def _apply_negative_scoring(
        self, url: str, link_text: str, context: str, reasoning: list[str]
    ) -> float:
        """Apply negative scoring for non-target content indicators."""
        score = 0.0
        combined_text = f"{url} {link_text} {context}".lower()

        for keyword in self.negative_keywords:
            if keyword in combined_text:
                score -= 1.0
                reasoning.append(f"Negative indicator found: '{keyword}'")

        return score

    @abstractmethod
    def _apply_custom_scoring(
        self, url: str, link_text: str, context: str, reasoning: list[str]
    ) -> float:
        """Apply content-type specific custom scoring rules."""
        pass

    @abstractmethod
    def _get_extension_score(self, extension: str) -> float:
        """Get score for specific file extension."""
        pass

    @abstractmethod
    def _categorize_link(self, url: str, link_text: str, score: float) -> str:
        """Categorize the type of content link."""
        pass


class GenericContentLinkDetector(ContentLinkDetector):
    """Generic implementation of ContentLinkDetector that can be configured for any content type."""

    def __init__(
        self,
        content_type: str,
        positive_keywords: set[str],
        negative_keywords: Union[set[str], None] = None,
        positive_path_patterns: Union[list[str], None] = None,
        target_file_extensions: Union[set[str], None] = None,
        detection_config: Union[dict[str, Any], None] = None,
    ):
        """Initialize the generic link detector.

        Args:
            content_type: String identifier for the content type
            positive_keywords: Keywords that indicate target content
            negative_keywords: Keywords that indicate non-target content
            positive_path_patterns: Regex patterns for target URL paths
            target_file_extensions: File extensions that might contain target content
            detection_config: Configuration for detection
        """
        super().__init__(detection_config)
        self._content_type = content_type
        self._positive_keywords = positive_keywords
        self._negative_keywords = negative_keywords or set()
        self._positive_path_patterns = positive_path_patterns or []
        self._target_file_extensions = target_file_extensions or set()

    @property
    def positive_keywords(self) -> set[str]:
        """Keywords that indicate target content type."""
        return self._positive_keywords

    @property
    def negative_keywords(self) -> set[str]:
        """Keywords that indicate non-target content."""
        return self._negative_keywords

    @property
    def positive_path_patterns(self) -> list[str]:
        """Regex patterns for URL paths that likely contain target content."""
        return self._positive_path_patterns

    @property
    def target_file_extensions(self) -> set[str]:
        """File extensions that might contain target content."""
        return self._target_file_extensions

    @property
    def content_type(self) -> str:
        """String identifier for the content type."""
        return self._content_type

    def _apply_custom_scoring(
        self, url: str, link_text: str, context: str, reasoning: list[str]
    ) -> float:
        """Apply generic custom scoring rules."""
        score = 0.0

        # Basic action word detection
        action_words = {"view", "see", "browse", "download", "read"}
        text_lower = link_text.lower()

        for action in action_words:
            if action in text_lower:
                score += 0.5
                reasoning.append(f"Action word found: '{action}'")

        return score

    def _get_extension_score(self, extension: str) -> float:
        """Get score for specific file extension."""
        # Default scoring - can be overridden
        extension_scores = {
            ".pdf": 2.0,
            ".doc": 1.5,
            ".docx": 1.5,
            ".jpg": 1.0,
            ".jpeg": 1.0,
            ".png": 1.0,
            ".webp": 1.0,
        }
        return extension_scores.get(extension, 0.5)

    def _categorize_link(self, url: str, link_text: str, score: float) -> str:
        """Categorize the type of content link."""
        if score < 0.3:
            return f"unlikely_{self.content_type}"
        elif score < 0.6:
            return f"possible_{self.content_type}"
        elif ".pdf" in url.lower():
            return f"{self.content_type}_document"
        elif any(ext in url.lower() for ext in [".jpg", ".jpeg", ".png", ".webp"]):
            return f"{self.content_type}_image"
        else:
            return f"{self.content_type}_page"


def create_link_detector(
    content_type: str,
    positive_keywords: set[str],
    negative_keywords: Union[set[str], None] = None,
    positive_path_patterns: Union[list[str], None] = None,
    target_file_extensions: Union[set[str], None] = None,
    detection_config: Union[dict[str, Any], None] = None,
) -> ContentLinkDetector:
    """Factory function to create a generic content link detector.

    Args:
        content_type: Type of content to detect (e.g., 'menu', 'product', 'article')
        positive_keywords: Keywords that indicate target content
        negative_keywords: Keywords that indicate non-target content
        positive_path_patterns: Regex patterns for target URL paths
        target_file_extensions: File extensions that might contain target content
        detection_config: Configuration dictionary

    Returns:
        Configured GenericContentLinkDetector instance
    """
    return GenericContentLinkDetector(
        content_type=content_type,
        positive_keywords=positive_keywords,
        negative_keywords=negative_keywords,
        positive_path_patterns=positive_path_patterns,
        target_file_extensions=target_file_extensions,
        detection_config=detection_config,
    )


# Convenience function for quick link analysis
def analyze_links_for_content(
    html: str,
    base_url: str,
    content_type: str,
    positive_keywords: set[str],
    negative_keywords: Union[set[str], None] = None,
    positive_path_patterns: Union[list[str], None] = None,
    target_file_extensions: Union[set[str], None] = None,
    max_links: int = 20,
    confidence_threshold: float = 0.6,
) -> list[dict[str, Any]]:
    """Analyze HTML for content-specific links without creating a detector instance.

    Args:
        html: HTML content to analyze
        base_url: Base URL for resolving relative links
        content_type: Type of content to detect
        positive_keywords: Keywords that indicate target content
        negative_keywords: Keywords that indicate non-target content
        positive_path_patterns: Regex patterns for target URL paths
        target_file_extensions: File extensions that might contain target content
        max_links: Maximum number of links to return
        confidence_threshold: Minimum confidence threshold for links

    Returns:
        List of analyzed links that meet the confidence threshold
    """
    detector = create_link_detector(
        content_type=content_type,
        positive_keywords=positive_keywords,
        negative_keywords=negative_keywords,
        positive_path_patterns=positive_path_patterns,
        target_file_extensions=target_file_extensions,
        detection_config={
            "max_links": max_links,
            "confidence_threshold": confidence_threshold,
        },
    )

    return detector.extract_content_links_from_html(html, base_url, max_links)
