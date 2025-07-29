"""Generic Element Detection Framework for Interactive Web Elements.

This module provides a flexible framework for detecting specific types of interactive
elements (buttons, tabs, links) that lead to target content. It uses an abstract
base class that can be specialized for different content types.
"""

from abc import ABC, abstractmethod
import logging
from typing import Any, Union
from urllib.parse import urljoin

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class ContentElementDetector(ABC):
    """Abstract base class for content-specific interactive element detection."""

    def __init__(self, detection_config: Union[dict[str, Any], None] = None):
        """Initialize the element detector with configuration.

        Args:
            detection_config: Configuration for detection.
        """
        self.config = detection_config or {}
        self.confidence_threshold = self.config.get("confidence_threshold", 0.6)
        self.max_elements = self.config.get("max_elements", 20)

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
    def element_selectors(self) -> list[str]:
        """CSS selectors for interactive elements to analyze."""
        pass

    @property
    @abstractmethod
    def content_type(self) -> str:
        """String identifier for the content type."""
        pass

    def analyze_element_for_content(
        self, element: Any, base_url: str = ""
    ) -> dict[str, Any]:
        """Analyze a single element for target content potential.

        Args:
            element: BeautifulSoup element to analyze
            base_url: Base URL for resolving relative links

        Returns:
            Dictionary with analysis results including score, reasoning, and confidence
        """
        analysis = {
            "element_tag": element.name,
            "element_text": element.get_text(strip=True),
            "element_attrs": dict(element.attrs),
            "is_likely_content": False,
            "confidence": 0.0,
            "score": 0.0,
            "reasoning": [],
            "category": "unknown",
            "content_type": self.content_type,
        }

        score = 0.0
        reasoning = []

        # 1. Analyze element text
        text_score = self._analyze_element_text(element, reasoning)
        score += text_score

        # 2. Analyze element attributes
        attr_score = self._analyze_element_attributes(element, reasoning)
        score += attr_score

        # 3. Analyze element CSS classes
        class_score = self._analyze_element_classes(element, reasoning)
        score += class_score

        # 4. Analyze element ID
        id_score = self._analyze_element_id(element, reasoning)
        score += id_score

        # 5. Analyze href/onclick attributes
        action_score = self._analyze_element_actions(element, base_url, reasoning)
        score += action_score

        # 6. Apply negative scoring
        negative_score = self._apply_negative_scoring(element, reasoning)
        score += negative_score

        # 7. Apply custom scoring rules
        custom_score = self._apply_custom_scoring(element, reasoning)
        score += custom_score

        # Normalize score to 0-1 range
        final_score = max(0.0, min(1.0, score / 10.0))

        # Determine if likely target content
        is_likely_content = final_score >= self.confidence_threshold
        confidence = final_score

        # Categorize the element
        category = self._categorize_element(element, final_score)

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

    def extract_content_elements_from_html(
        self, html: str, base_url: str = "", max_elements: Union[int, None] = None
    ) -> list[dict[str, Any]]:
        """Extract and analyze all potential content elements from HTML.

        Args:
            html: HTML content to analyze
            base_url: Base URL for resolving relative links
            max_elements: Maximum number of elements to return

        Returns:
            List of analyzed elements sorted by content potential score
        """
        max_elements = max_elements or self.max_elements
        soup = BeautifulSoup(html, "html.parser")
        analyzed_elements = []

        # Find elements using configured selectors
        for selector in self.element_selectors:
            try:
                elements = soup.select(selector)
                for element in elements:
                    # Skip if element has no meaningful content
                    if not element.get_text(strip=True) and not element.get("href"):
                        continue

                    # Analyze the element
                    analysis = self.analyze_element_for_content(element, base_url)

                    if (
                        analysis["score"] > 0.2
                    ):  # Only include elements with some potential
                        analyzed_elements.append(analysis)

            except Exception as e:
                logger.debug(f"Error processing selector '{selector}': {e}")
                continue

        # Sort by score (highest first) and limit results
        analyzed_elements.sort(key=lambda x: x["score"], reverse=True)
        return analyzed_elements[:max_elements]

    def _analyze_element_text(self, element: Any, reasoning: list[str]) -> float:
        """Analyze element text for content indicators."""
        text = element.get_text(strip=True).lower()
        if not text:
            return 0.0

        score = 0.0

        # Check for keywords in element text
        for keyword in self.positive_keywords:
            if keyword in text:
                # Give higher score for exact matches
                if keyword == text:
                    score += 2.5
                    reasoning.append(
                        f"Element text exactly matches {self.content_type} keyword: '{keyword}'"
                    )
                else:
                    score += 1.0
                    reasoning.append(
                        f"Element text contains {self.content_type} keyword: '{keyword}'"
                    )

        return score

    def _analyze_element_attributes(self, element: Any, reasoning: list[str]) -> float:
        """Analyze element attributes for content indicators."""
        score = 0.0

        # Common attributes to check
        for attr_name, attr_value in element.attrs.items():
            # Convert to string and lowercase
            attr_text = str(attr_value).lower() if attr_value else ""

            # Check data-* attributes
            if attr_name.startswith("data-") or attr_name in [
                "title",
                "alt",
                "aria-label",
            ]:
                for keyword in self.positive_keywords:
                    if keyword in attr_text:
                        score += 0.5
                        reasoning.append(
                            f"Attribute {attr_name} contains {self.content_type} keyword: '{keyword}'"
                        )

        return min(score, 2.0)  # Cap attribute score

    def _analyze_element_classes(self, element: Any, reasoning: list[str]) -> float:
        """Analyze element CSS classes for content indicators."""
        classes = element.get("class", [])
        if not classes:
            return 0.0

        score = 0.0
        class_text = " ".join(classes).lower()

        for keyword in self.positive_keywords:
            if keyword in class_text:
                score += 1.0
                reasoning.append(
                    f"CSS classes contain {self.content_type} keyword: '{keyword}'"
                )

        return min(score, 2.0)  # Cap class score

    def _analyze_element_id(self, element: Any, reasoning: list[str]) -> float:
        """Analyze element ID for content indicators."""
        element_id = element.get("id", "").lower()
        if not element_id:
            return 0.0

        score = 0.0

        for keyword in self.positive_keywords:
            if keyword in element_id:
                score += 1.5
                reasoning.append(
                    f"Element ID contains {self.content_type} keyword: '{keyword}'"
                )

        return score

    def _analyze_element_actions(
        self, element: Any, base_url: str, reasoning: list[str]
    ) -> float:
        """Analyze element actions (href, onclick) for content indicators."""
        score = 0.0

        # Check href attribute
        href = element.get("href", "")
        if href:
            # Resolve relative URLs
            if base_url and not href.startswith(
                ("http://", "https://", "#", "javascript:")
            ):
                href = urljoin(base_url, href)

            href_lower = href.lower()
            for keyword in self.positive_keywords:
                if keyword in href_lower:
                    score += 1.0
                    reasoning.append(
                        f"Link URL contains {self.content_type} keyword: '{keyword}'"
                    )

        # Check onclick attribute
        onclick = element.get("onclick", "").lower()
        if onclick:
            for keyword in self.positive_keywords:
                if keyword in onclick:
                    score += 0.5
                    reasoning.append(
                        f"onclick action contains {self.content_type} keyword: '{keyword}'"
                    )

        return score

    def _apply_negative_scoring(self, element: Any, reasoning: list[str]) -> float:
        """Apply negative scoring for non-target content indicators."""
        score = 0.0

        # Combine all text for negative keyword checking
        combined_text = []
        combined_text.append(element.get_text(strip=True))
        combined_text.extend(element.get("class", []))
        combined_text.append(element.get("id", ""))
        combined_text.append(element.get("href", ""))

        combined_lower = " ".join(str(t) for t in combined_text).lower()

        for keyword in self.negative_keywords:
            if keyword in combined_lower:
                score -= 1.0
                reasoning.append(f"Negative indicator found: '{keyword}'")

        return score

    def detect_high_confidence_elements(
        self, html: str, base_url: str = "", threshold: float = 0.8
    ) -> dict[str, Any]:
        """Detect high-confidence elements and recommend early exit.

        This method provides backward compatibility with the old interface.

        Args:
            html: HTML content to analyze
            base_url: Base URL for resolving relative links
            threshold: Confidence threshold for high-confidence elements

        Returns:
            Dictionary with early_exit_recommended, high_confidence_elements, and content_type
        """
        elements = self.extract_content_elements_from_html(html, base_url)

        # Filter for high-confidence elements
        high_confidence_elements = [
            elem for elem in elements if elem["confidence"] >= threshold
        ]

        # Recommend early exit if we have high-confidence elements
        early_exit_recommended = len(high_confidence_elements) > 0

        return {
            "early_exit_recommended": early_exit_recommended,
            "high_confidence_elements": high_confidence_elements,
            "content_type": self.content_type,
        }

    @abstractmethod
    def _apply_custom_scoring(self, element: Any, reasoning: list[str]) -> float:
        """Apply content-type specific custom scoring rules."""
        pass

    @abstractmethod
    def _categorize_element(self, element: Any, score: float) -> str:
        """Categorize the type of content element."""
        pass


class GenericContentElementDetector(ContentElementDetector):
    """Generic implementation of ContentElementDetector that can be configured for any content type."""

    def __init__(
        self,
        content_type: str,
        positive_keywords: set[str],
        negative_keywords: Union[set[str], None] = None,
        element_selectors: Union[list[str], None] = None,
        detection_config: Union[dict[str, Any], None] = None,
    ):
        """Initialize the generic element detector.

        Args:
            content_type: String identifier for the content type
            positive_keywords: Keywords that indicate target content
            negative_keywords: Keywords that indicate non-target content
            element_selectors: CSS selectors for interactive elements
            detection_config: Configuration for detection
        """
        super().__init__(detection_config)
        self._content_type = content_type
        self._positive_keywords = positive_keywords
        self._negative_keywords = negative_keywords or set()
        self._element_selectors = element_selectors or [
            "button",
            "a[href]",
            "[onclick]",
            ".btn",
            ".button",
            ".tab",
            ".menu-item",
            ".nav-item",
        ]

    @property
    def positive_keywords(self) -> set[str]:
        """Keywords that indicate target content type."""
        return self._positive_keywords

    @property
    def negative_keywords(self) -> set[str]:
        """Keywords that indicate non-target content."""
        return self._negative_keywords

    @property
    def element_selectors(self) -> list[str]:
        """CSS selectors for interactive elements to analyze."""
        return self._element_selectors

    @property
    def content_type(self) -> str:
        """String identifier for the content type."""
        return self._content_type

    def _apply_custom_scoring(self, element: Any, reasoning: list[str]) -> float:
        """Apply generic custom scoring rules."""
        score = 0.0

        # Bonus for interactive elements
        if element.name in ["button", "a"]:
            score += 0.5
            reasoning.append(f"Interactive element: {element.name}")

        # Bonus for elements with click handlers
        if element.get("onclick"):
            score += 0.5
            reasoning.append("Element has click handler")

        return score

    def _categorize_element(self, element: Any, score: float) -> str:
        """Categorize the type of content element."""
        if score < 0.3:
            return f"unlikely_{self.content_type}"
        elif score < 0.6:
            return f"possible_{self.content_type}"
        elif element.name == "button":
            return f"{self.content_type}_button"
        elif element.name == "a":
            return f"{self.content_type}_link"
        else:
            return f"{self.content_type}_element"


def create_element_detector(
    content_type: str,
    positive_keywords: set[str],
    negative_keywords: Union[set[str], None] = None,
    element_selectors: Union[list[str], None] = None,
    detection_config: Union[dict[str, Any], None] = None,
) -> ContentElementDetector:
    """Factory function to create a generic content element detector.

    Args:
        content_type: Type of content to detect
        positive_keywords: Keywords that indicate target content
        negative_keywords: Keywords that indicate non-target content
        element_selectors: CSS selectors for interactive elements
        detection_config: Configuration dictionary

    Returns:
        Configured GenericContentElementDetector instance
    """
    return GenericContentElementDetector(
        content_type=content_type,
        positive_keywords=positive_keywords,
        negative_keywords=negative_keywords,
        element_selectors=element_selectors,
        detection_config=detection_config,
    )


# Convenience function for quick element analysis
def analyze_elements_for_content(
    html: str,
    base_url: str,
    content_type: str,
    positive_keywords: set[str],
    negative_keywords: Union[set[str], None] = None,
    element_selectors: Union[list[str], None] = None,
    max_elements: int = 20,
    confidence_threshold: float = 0.6,
) -> list[dict[str, Any]]:
    """Analyze HTML for content-specific elements without creating a detector instance.

    Args:
        html: HTML content to analyze
        base_url: Base URL for resolving relative links
        content_type: Type of content to detect
        positive_keywords: Keywords that indicate target content
        negative_keywords: Keywords that indicate non-target content
        element_selectors: CSS selectors for interactive elements
        max_elements: Maximum number of elements to return
        confidence_threshold: Minimum confidence threshold for elements

    Returns:
        List of analyzed elements that meet the confidence threshold
    """
    detector = create_element_detector(
        content_type=content_type,
        positive_keywords=positive_keywords,
        negative_keywords=negative_keywords,
        element_selectors=element_selectors,
        detection_config={
            "max_elements": max_elements,
            "confidence_threshold": confidence_threshold,
        },
    )

    return detector.extract_content_elements_from_html(html, base_url, max_elements)
