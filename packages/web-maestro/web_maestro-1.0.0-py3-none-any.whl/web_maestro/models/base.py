"""Abstract interfaces for extensibility in the web_maestro package."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Protocol, runtime_checkable

from playwright.async_api import BrowserContext, Page

from .types import (
    CapturedBlock,
    CaptureResult,
    DOMElement,
    InteractionResult,
    PageMetrics,
    ScrollPosition,
)


class ContentFilter(ABC):
    """Abstract interface for filtering elements during scraping."""

    @abstractmethod
    async def should_interact(self, element: DOMElement) -> bool:
        """Determine if an element should be interacted with.

        Args:
            element: The DOM element to evaluate

        Returns:
            True if the element should be interacted with, False otherwise
        """
        pass

    @abstractmethod
    async def should_capture(self, content: str, source_id: str) -> bool:
        """Determine if content should be captured.

        Args:
            content: The content to evaluate
            source_id: The source identifier of the content

        Returns:
            True if the content should be captured, False otherwise
        """
        pass


class ExtractionStrategy(ABC):
    """Abstract interface for content extraction strategies."""

    @abstractmethod
    async def extract(self, page: Page, config: dict[str, Any]) -> list[CapturedBlock]:
        """Extract content from a page.

        Args:
            page: The Playwright page object
            config: Configuration dictionary

        Returns:
            List of captured content blocks
        """
        pass

    @abstractmethod
    def get_selectors(self) -> dict[str, str]:
        """Get CSS selectors used by this strategy.

        Returns:
            Dictionary mapping selector names to CSS selectors
        """
        pass


class NavigationStrategy(ABC):
    """Abstract interface for navigation strategies."""

    @abstractmethod
    async def navigate(self, page: Page, url: str, timeout_ms: int) -> None:
        """Navigate to a URL with specific strategy.

        Args:
            page: The Playwright page object
            url: The URL to navigate to
            timeout_ms: Navigation timeout in milliseconds
        """
        pass

    @abstractmethod
    async def wait_for_ready(self, page: Page) -> None:
        """Wait for the page to be ready for interaction.

        Args:
            page: The Playwright page object
        """
        pass


class InteractionStrategy(ABC):
    """Abstract interface for DOM interaction strategies."""

    @abstractmethod
    async def interact(self, page: Page, element: DOMElement) -> InteractionResult:
        """Interact with a DOM element.

        Args:
            page: The Playwright page object
            element: The element to interact with

        Returns:
            Result of the interaction
        """
        pass

    @abstractmethod
    def get_interaction_type(self) -> str:
        """Get the type of interaction this strategy performs.

        Returns:
            String identifier for the interaction type
        """
        pass


class ScrollStrategy(ABC):
    """Abstract interface for scrolling strategies."""

    @abstractmethod
    async def scroll(self, page: Page, position: ScrollPosition) -> ScrollPosition:
        """Perform scrolling on the page.

        Args:
            page: The Playwright page object
            position: Current scroll position

        Returns:
            New scroll position after scrolling
        """
        pass

    @abstractmethod
    async def should_continue_scrolling(
        self,
        page: Page,
        position: ScrollPosition,
        previous_positions: list[ScrollPosition],
    ) -> bool:
        """Determine if scrolling should continue.

        Args:
            page: The Playwright page object
            position: Current scroll position
            previous_positions: History of scroll positions

        Returns:
            True if scrolling should continue, False otherwise
        """
        pass


class StabilityDetector(ABC):
    """Abstract interface for DOM stability detection."""

    @abstractmethod
    async def is_stable(
        self, page: Page, previous_state: Any | None
    ) -> tuple[bool, Any]:
        """Check if the DOM is stable.

        Args:
            page: The Playwright page object
            previous_state: Previous DOM state for comparison

        Returns:
            Tuple of (is_stable, current_state)
        """
        pass

    @abstractmethod
    async def wait_for_stability(self, page: Page, timeout_ms: int) -> bool:
        """Wait for DOM to become stable.

        Args:
            page: The Playwright page object
            timeout_ms: Maximum time to wait in milliseconds

        Returns:
            True if DOM became stable, False if timeout
        """
        pass


@runtime_checkable
class ContentProcessor(Protocol):
    """Protocol for content post-processing."""

    def process(self, blocks: list[CapturedBlock]) -> list[CapturedBlock]:
        """Process captured content blocks.

        Args:
            blocks: Raw captured blocks

        Returns:
            Processed blocks
        """
        ...

    def get_name(self) -> str:
        """Get processor name for logging."""
        ...


@runtime_checkable
class MetricsCollector(Protocol):
    """Protocol for collecting page metrics."""

    async def collect(self, page: Page) -> PageMetrics:
        """Collect metrics from the page.

        Args:
            page: The Playwright page object

        Returns:
            Page metrics
        """
        ...


class CapturePhaseStrategy(ABC):
    """Abstract interface for capture phase strategies."""

    @abstractmethod
    async def execute(
        self, page: Page, context: BrowserContext, config: dict[str, Any]
    ) -> CaptureResult:
        """Execute a capture phase.

        Args:
            page: The Playwright page object
            context: The browser context
            config: Configuration dictionary

        Returns:
            Result of the capture phase
        """
        pass

    @abstractmethod
    def get_phase_name(self) -> str:
        """Get the name of this capture phase.

        Returns:
            Phase name for logging and tracking
        """
        pass

    @abstractmethod
    def get_dependencies(self) -> list[str]:
        """Get names of phases this phase depends on.

        Returns:
            List of phase names that must run before this phase
        """
        pass


class ResourceBlocker(ABC):
    """Abstract interface for resource blocking strategies."""

    @abstractmethod
    async def should_block(self, resource_type: str, url: str) -> bool:
        """Determine if a resource should be blocked.

        Args:
            resource_type: Type of the resource
            url: URL of the resource

        Returns:
            True if resource should be blocked, False otherwise
        """
        pass

    @abstractmethod
    def get_blocked_patterns(self) -> list[str]:
        """Get URL patterns to block.

        Returns:
            List of URL patterns to block
        """
        pass


class SessionManager(ABC):
    """Abstract interface for session management."""

    @abstractmethod
    async def create_context(self) -> BrowserContext:
        """Create a new browser context.

        Returns:
            New browser context
        """
        pass

    @abstractmethod
    async def cleanup_context(self, context: BrowserContext) -> None:
        """Clean up a browser context.

        Args:
            context: Context to clean up
        """
        pass

    @abstractmethod
    async def get_active_contexts(self) -> list[BrowserContext]:
        """Get all active browser contexts.

        Returns:
            List of active contexts
        """
        pass


class ErrorHandler(ABC):
    """Abstract interface for error handling strategies."""

    @abstractmethod
    async def handle_error(
        self, error: Exception, context: dict[str, Any], page: Page | None = None
    ) -> bool:
        """Handle an error during scraping.

        Args:
            error: The exception that occurred
            context: Context information about the error
            page: The page object if available

        Returns:
            True if error was handled and execution should continue,
            False if error should be re-raised
        """
        pass

    @abstractmethod
    def should_retry(self, error: Exception, attempt: int) -> bool:
        """Determine if an operation should be retried.

        Args:
            error: The exception that occurred
            attempt: Current attempt number (1-based)

        Returns:
            True if operation should be retried, False otherwise
        """
        pass
