"""Core playwright utilities - browser setup, sessions, and context management."""

from ..models.types import BrowserConfig
from .browser_setup import create_browser_context, setup_browser
from .context import SessionContext
from .exceptions import (
    BrowserError,
    BrowserSetupError,
    NavigationError,
    PageError,
    PlaywrightUtilsError,
    TimeoutError,
)

__all__ = [
    "BrowserConfig",
    "BrowserError",
    "BrowserSetupError",
    "NavigationError",
    "PageError",
    # Exceptions
    "PlaywrightUtilsError",
    # Session management
    "SessionContext",
    "TimeoutError",
    # Browser setup
    "create_browser_context",
    "setup_browser",
]
