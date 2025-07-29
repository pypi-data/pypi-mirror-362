"""Core interface definitions for playwright utilities."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Protocol, runtime_checkable

from playwright.async_api import Page

# Import the types from models
from ..models.types import CapturedBlock, DOMElement, InteractionResult, PageMetrics


# Core interfaces that other modules expect
class DOMNavigator(ABC):
    """Abstract interface for DOM navigation."""

    @abstractmethod
    async def navigate_to(self, url: str) -> None:
        """Navigate to a URL."""
        pass

    @abstractmethod
    async def find_elements(self, selector: str) -> list[DOMElement]:
        """Find elements by CSS selector."""
        pass


class ContentExtractor(ABC):
    """Abstract interface for content extraction."""

    @abstractmethod
    async def extract_content(self, html: str, context: dict[str, Any]) -> Any:
        """Extract structured content from HTML."""
        pass

    @abstractmethod
    def get_stats(self) -> dict[str, Any]:
        """Get extraction statistics."""
        pass


class MenuClassifier(ABC):
    """Abstract interface for menu classification."""

    @abstractmethod
    async def classify_content(self, content: str) -> dict[str, Any]:
        """Classify content as menu or non-menu."""
        pass

    @abstractmethod
    def get_confidence(self) -> float:
        """Get classification confidence."""
        pass


# Additional interfaces for compatibility
class Navigator(ABC):
    """Abstract navigator interface."""

    @abstractmethod
    async def navigate(self, page: Page, url: str, timeout_ms: int) -> None:
        """Navigate to a URL."""
        pass


class Storage(ABC):
    """Abstract storage interface."""

    @abstractmethod
    async def store(self, key: str, data: Any) -> None:
        """Store data."""
        pass

    @abstractmethod
    async def retrieve(self, key: str) -> Any:
        """Retrieve data."""
        pass


class Tool(ABC):
    """Abstract tool interface."""

    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """Execute the tool."""
        pass


class Cache(ABC):
    """Abstract cache interface."""

    @abstractmethod
    async def get(self, key: str) -> Any:
        """Get cached value."""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any) -> None:
        """Set cached value."""
        pass


class Validator(ABC):
    """Abstract validator interface."""

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate data."""
        pass


class ModelProvider(ABC):
    """Abstract model provider interface."""

    @abstractmethod
    async def get_model(self) -> Any:
        """Get model instance."""
        pass


# Re-export all the original interfaces from models/base.py for compatibility
class ContentFilter(ABC):
    """Abstract interface for filtering elements during scraping."""

    @abstractmethod
    async def should_interact(self, element: DOMElement) -> bool:
        """Determine if an element should be interacted with."""
        pass

    @abstractmethod
    async def should_capture(self, content: str, source_id: str) -> bool:
        """Determine if content should be captured."""
        pass


class ExtractionStrategy(ABC):
    """Abstract interface for content extraction strategies."""

    @abstractmethod
    async def extract(self, page: Page, config: dict[str, Any]) -> list[CapturedBlock]:
        """Extract content from a page."""
        pass

    @abstractmethod
    def get_selectors(self) -> dict[str, str]:
        """Get CSS selectors used by this strategy."""
        pass


class NavigationStrategy(ABC):
    """Abstract interface for navigation strategies."""

    @abstractmethod
    async def navigate(self, page: Page, url: str, timeout_ms: int) -> None:
        """Navigate to a URL with specific strategy."""
        pass

    @abstractmethod
    async def wait_for_ready(self, page: Page) -> None:
        """Wait for the page to be ready for interaction."""
        pass


class InteractionStrategy(ABC):
    """Abstract interface for DOM interaction strategies."""

    @abstractmethod
    async def interact(self, page: Page, element: DOMElement) -> InteractionResult:
        """Interact with a DOM element."""
        pass

    @abstractmethod
    def get_interaction_type(self) -> str:
        """Get the type of interaction this strategy performs."""
        pass


class StabilityDetector(ABC):
    """Abstract interface for DOM stability detection."""

    @abstractmethod
    async def is_stable(
        self, page: Page, previous_state: Any | None
    ) -> tuple[bool, Any]:
        """Check if the DOM is stable."""
        pass

    @abstractmethod
    async def wait_for_stability(self, page: Page, timeout_ms: int) -> bool:
        """Wait for DOM to become stable."""
        pass


@runtime_checkable
class ContentProcessor(Protocol):
    """Protocol for content post-processing."""

    def process(self, blocks: list[CapturedBlock]) -> list[CapturedBlock]:
        """Process captured content blocks."""
        ...

    def get_name(self) -> str:
        """Get processor name for logging."""
        ...


@runtime_checkable
class MetricsCollector(Protocol):
    """Protocol for collecting page metrics."""

    async def collect(self, page: Page) -> PageMetrics:
        """Collect metrics from the page."""
        ...
