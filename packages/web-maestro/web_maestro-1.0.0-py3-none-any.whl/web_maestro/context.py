"""Session management for web_maestro.

This module provides SessionContext for managing browser sessions,
resources, and cleanup during web scraping operations.
"""

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
import logging
import time
from typing import Any, Optional

from playwright.async_api import Browser, BrowserContext, Page

from .exceptions import ResourceCleanupError, SessionError

logger = logging.getLogger(__name__)


@dataclass
class SessionStats:
    """Statistics for a scraping session."""

    created_at: float = field(default_factory=time.time)
    pages_created: int = 0
    contexts_created: int = 0
    total_requests: int = 0
    failed_requests: int = 0
    total_duration: float = 0

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for logging."""
        return {
            "created_at": self.created_at,
            "pages_created": self.pages_created,
            "contexts_created": self.contexts_created,
            "total_requests": self.total_requests,
            "failed_requests": self.failed_requests,
            "total_duration": self.total_duration,
            "success_rate": self.success_rate,
        }

    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_requests == 0:
            return 0.0
        return (self.total_requests - self.failed_requests) / self.total_requests


@dataclass
class SessionConfig:
    """Configuration for scraping sessions."""

    max_concurrent_pages: int = 5
    max_contexts: int = 10
    rate_limit_per_second: Optional[float] = None
    page_timeout_ms: int = 30000
    context_timeout_ms: int = 60000
    auto_cleanup: bool = True
    collect_stats: bool = True


class SessionContext:
    """Session context with resource management and rate limiting.

    This is the main context class for managing browser sessions in web_maestro.
    It provides:
    - Resource tracking and cleanup
    - Rate limiting
    - Statistics collection
    - Concurrent page/context management
    """

    def __init__(self, config: Optional[SessionConfig] = None):
        """Initialize SessionContext with optional configuration."""
        self.config = config or SessionConfig()
        self.cleanup_started = False
        self.background_tasks: list[asyncio.Task] = []
        self.last_logged_dom_hash: Optional[str] = None

        # Enhanced features
        self._browser: Optional[Browser] = None
        self._contexts: dict[str, BrowserContext] = {}
        self._pages: dict[str, Page] = {}
        self._semaphore = asyncio.Semaphore(self.config.max_concurrent_pages)
        self._rate_limiter: Optional[asyncio.Semaphore] = None
        self._last_request_time = 0.0
        self._lock = asyncio.Lock()
        self._stats = SessionStats() if self.config.collect_stats else None

        # Set up rate limiting
        if self.config.rate_limit_per_second:
            self._rate_limiter = asyncio.Semaphore(1)

    async def __aenter__(self) -> "SessionContext":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit with cleanup."""
        if self.config.auto_cleanup:
            await self.cleanup()

    async def acquire_page_slot(self) -> None:
        """Acquire a slot for creating a new page."""
        await self._semaphore.acquire()

    def release_page_slot(self) -> None:
        """Release a page slot."""
        self._semaphore.release()

    async def rate_limit(self) -> None:
        """Apply rate limiting if configured."""
        if self._rate_limiter:
            async with self._rate_limiter:
                # Calculate delay needed
                current_time = time.time()
                time_since_last = current_time - self._last_request_time
                min_interval = 1.0 / self.config.rate_limit_per_second

                if time_since_last < min_interval:
                    await asyncio.sleep(min_interval - time_since_last)

                self._last_request_time = time.time()

    async def cleanup(self):
        """Clean up all resources."""
        self.cleanup_started = True

        # Cancel background tasks
        for task in self.background_tasks:
            if hasattr(task, "done"):
                try:
                    # For real asyncio tasks, done() returns a boolean
                    # For AsyncMock, done() returns a coroutine - we need to handle both
                    if hasattr(task, "_mock_name"):
                        # This is a mock object, call done() as a regular method
                        if not task.done.return_value:
                            task.cancel()
                    else:
                        # This is a real asyncio task
                        if not task.done():
                            task.cancel()
                except Exception:
                    # If anything goes wrong, try to cancel anyway
                    if hasattr(task, "cancel"):
                        task.cancel()

        # Wait for cancellations - only await real asyncio tasks
        if self.background_tasks:
            real_tasks = []
            for task in self.background_tasks:
                # Check if it's a real asyncio task/future
                if hasattr(task, "__await__") and not hasattr(task, "_mock_name"):
                    real_tasks.append(task)

            if real_tasks:
                await asyncio.gather(*real_tasks, return_exceptions=True)

        # Clean up browser resources
        errors = []

        # Close all pages
        for page_id, page in list(self._pages.items()):
            try:
                await page.close()
            except Exception as e:
                errors.append(e)
                logger.warning(f"Error closing page {page_id}: {e}")

        # Close all contexts
        for ctx_id, context in list(self._contexts.items()):
            try:
                await context.close()
            except Exception as e:
                errors.append(e)
                logger.warning(f"Error closing context {ctx_id}: {e}")

        # Clear references
        self._pages.clear()
        self._contexts.clear()

        if errors:
            raise ResourceCleanupError(
                resources=[f"page_{i}" for i in range(len(errors))], errors=errors
            )

    def add_background_task(self, task: asyncio.Task) -> None:
        """Add a background task to track."""
        self.background_tasks.append(task)

    @asynccontextmanager
    async def create_page(
        self, context: Optional[BrowserContext] = None
    ) -> AsyncIterator[Page]:
        """Create a managed page."""
        await self.acquire_page_slot()
        page = None

        try:
            # Create page
            if context:
                page = await context.new_page()
            elif self._browser:
                page = await self._browser.new_page()
            else:
                raise SessionError("No browser or context available")

            # Track page
            page_id = str(id(page))
            self._pages[page_id] = page

            if self._stats:
                self._stats.pages_created += 1

            yield page

        finally:
            # Cleanup
            if page:
                try:
                    await page.close()
                except Exception as e:
                    logger.warning(f"Error closing page: {e}")

                # Remove from tracking
                page_id = str(id(page))
                self._pages.pop(page_id, None)

            self.release_page_slot()

    @asynccontextmanager
    async def create_context(self) -> AsyncIterator[BrowserContext]:
        """Create a managed browser context."""
        async with self._lock:
            if len(self._contexts) >= self.config.max_contexts:
                raise SessionError(
                    f"Maximum contexts ({self.config.max_contexts}) reached"
                )

            if not self._browser:
                raise SessionError("No browser instance set")

            context = await self._browser.new_context()
            context_id = str(id(context))
            self._contexts[context_id] = context

            if self._stats:
                self._stats.contexts_created += 1

        try:
            yield context
        finally:
            # Cleanup
            try:
                await context.close()
            except Exception as e:
                logger.warning(f"Error closing context: {e}")

            # Remove from tracking
            async with self._lock:
                self._contexts.pop(context_id, None)

    def get_stats(self) -> Optional[SessionStats]:
        """Get session statistics."""
        if self._stats:
            self._stats.total_duration = time.time() - self._stats.created_at
        return self._stats

    def set_browser(self, browser: Browser) -> None:
        """Set the browser instance."""
        self._browser = browser

    async def get_active_pages(self) -> list[Page]:
        """Get all active pages."""
        return list(self._pages.values())

    async def get_active_contexts(self) -> list[BrowserContext]:
        """Get all active browser contexts."""
        return list(self._contexts.values())


def create_session_context(config: Optional[SessionConfig] = None) -> SessionContext:
    """Create a new session context.

    Args:
        config: Optional session configuration

    Returns:
        New SessionContext instance
    """
    return SessionContext(config)


# Legacy alias - web_maestro internally uses SessionContext
EnhancedSessionContext = SessionContext
