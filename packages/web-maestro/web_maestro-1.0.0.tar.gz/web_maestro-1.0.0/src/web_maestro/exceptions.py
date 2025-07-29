"""Custom exceptions for the web_maestro package."""

from __future__ import annotations


# New standard exception hierarchy
class WebMaestroError(Exception):
    """Base exception for all web-maestro errors."""

    pass


class FetchError(WebMaestroError):
    """Exception raised when content fetching fails."""

    pass


class LLMError(WebMaestroError):
    """Exception raised when LLM operations fail."""

    pass


# Legacy exception hierarchy (for backward compatibility)
class PlaywrightUtilsError(WebMaestroError):
    """Base exception for all web_maestro errors."""

    pass


class BrowserSetupError(PlaywrightUtilsError):
    """Raised when browser setup fails."""

    pass


class BrowserError(PlaywrightUtilsError):
    """Raised when browser operations fail."""

    pass


class PageError(PlaywrightUtilsError):
    """Raised when page operations fail."""

    pass


class NavigationError(PlaywrightUtilsError):
    """Raised when page navigation fails."""

    def __init__(self, url: str, message: str, original_error: Exception | None = None):
        """Initialize NavigationError.

        Args:
            url: The URL that failed to navigate to
            message: Error message describing the failure
            original_error: The original error that was caught.
        """
        self.url = url
        self.original_error = original_error
        super().__init__(f"Navigation to {url} failed: {message}")


class DOMInteractionError(PlaywrightUtilsError):
    """Raised when DOM interaction fails."""

    def __init__(
        self,
        interaction_type: str,
        selector: str | None = None,
        message: str = "",
        original_error: Exception | None = None,
    ):
        """Initialize DOMInteractionError.

        Args:
            interaction_type: Type of DOM interaction that failed
            selector: CSS selector where interaction failed
            message: Additional error message
            original_error: The original error that was caught.
        """
        self.interaction_type = interaction_type
        self.selector = selector
        self.original_error = original_error
        error_msg = f"{interaction_type} interaction failed"
        if selector:
            error_msg += f" on selector '{selector}'"
        if message:
            error_msg += f": {message}"
        super().__init__(error_msg)


class ContentExtractionError(PlaywrightUtilsError):
    """Raised when content extraction fails."""

    pass


class TimeoutError(PlaywrightUtilsError):
    """Raised when an operation times out."""

    def __init__(self, operation: str, timeout_ms: int):
        """Initialize TimeoutError.

        Args:
            operation: The operation that timed out
            timeout_ms: Timeout duration in milliseconds.
        """
        self.operation = operation
        self.timeout_ms = timeout_ms
        super().__init__(f"{operation} timed out after {timeout_ms}ms")


class StabilityError(PlaywrightUtilsError):
    """Raised when DOM stability cannot be achieved."""

    def __init__(self, message: str = "DOM did not stabilize within timeout"):
        """Initialize StabilityError.

        Args:
                message (str): The error message.
        """
        super().__init__(message)


class ResourceCleanupError(PlaywrightUtilsError):
    """Raised when resource cleanup fails."""

    def __init__(self, resources: list[str], errors: list[Exception]):
        """Initialize ResourceCleanupError.

        Args:
            resources: List of resources that failed to cleanup
            errors: List of validation errors.
        """
        self.resources = resources
        self.errors = errors
        super().__init__(
            f"Failed to cleanup {len(resources)} resources: {', '.join(resources)}"
        )


class ConfigurationError(WebMaestroError):
    """Raised when configuration is invalid."""

    def __init__(
        self, field: str = "", value: any = None, message: str = "Invalid configuration"
    ):
        """Initialize ConfigurationError.

        Args:
            field: Configuration field name that is invalid
            value: The invalid value
            message (str): The error message.
        """
        self.field = field
        self.value = value
        if field:
            super().__init__(f"Invalid configuration for '{field}': {message}")
        else:
            super().__init__(message)


class SessionError(PlaywrightUtilsError):
    """Raised when session management fails."""

    pass


class AIScoutError(PlaywrightUtilsError):
    """Raised when AI scout decision fails."""

    def __init__(self, message: str, llm_error: Exception | None = None):
        """Initialize AIScoutError.

        Args:
            message: Error message describing the scout failure
            llm_error: The LLM-related error that occurred.
        """
        self.llm_error = llm_error
        super().__init__(f"AI scout failed: {message}")


class InvalidSelectorError(PlaywrightUtilsError):
    """Raised when a CSS selector is invalid."""

    def __init__(self, selector: str, message: str = ""):
        """Initialize InvalidSelectorError.

        Args:
            selector: The invalid CSS selector
            message (str): The error message.
        """
        self.selector = selector
        error_msg = f"Invalid selector: '{selector}'"
        if message:
            error_msg += f" - {message}"
        super().__init__(error_msg)


class NetworkError(PlaywrightUtilsError):
    """Raised when network-related operations fail."""

    def __init__(self, url: str, status_code: int | None = None, message: str = ""):
        """Initialize NetworkError.

        Args:
            url: The URL that encountered a network error
            status_code: HTTP status code if available
            message (str): The error message.
        """
        self.url = url
        self.status_code = status_code
        error_msg = f"Network error for {url}"
        if status_code:
            error_msg += f" (status: {status_code})"
        if message:
            error_msg += f": {message}"
        super().__init__(error_msg)


class ContentDeduplicationError(PlaywrightUtilsError):
    """Raised when content deduplication fails."""

    pass


class ScreenshotError(PlaywrightUtilsError):
    """Raised when screenshot capture fails."""

    def __init__(self, path: str, message: str = ""):
        """Initialize ScreenshotError.

        Args:
            path: The path where the screenshot was supposed to be saved
            message (str): The error message.
        """
        self.path = path
        error_msg = f"Failed to capture screenshot at {path}"
        if message:
            error_msg += f": {message}"
        super().__init__(error_msg)


class TraceError(PlaywrightUtilsError):
    """Raised when trace operations fail."""

    pass


def wrap_playwright_error(func):
    """Decorator to wrap Playwright errors in custom exceptions."""
    import functools

    from playwright.async_api import Error as PlaywrightError

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except PlaywrightError as e:
            # Convert specific Playwright errors to custom exceptions
            error_str = str(e)
            if "Cannot navigate to invalid URL" in error_str:
                raise NavigationError(
                    url=kwargs.get("url", "unknown"),
                    message="Invalid URL format",
                    original_error=e,
                ) from e
            elif "Timeout" in error_str:
                raise TimeoutError(
                    operation=func.__name__, timeout_ms=kwargs.get("timeout", 30000)
                ) from e
            elif "net::" in error_str:
                raise NetworkError(
                    url=kwargs.get("url", "unknown"), message=error_str
                ) from e
            else:
                # Re-raise as generic PlaywrightUtilsError
                raise PlaywrightUtilsError(
                    f"Playwright error in {func.__name__}: {e}"
                ) from e

    return wrapper
