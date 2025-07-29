"""Session Context for Playwright-Based Crawling Sessions.

This module defines the `SessionContext` dataclass, which is used to manage
shared state across asynchronous crawling operations. It ensures that long-lived
tasks can be gracefully shut down and tracked during teardown.

The context is passed explicitly to most Playwright interactions in order to:
- Track whether cleanup has been triggered (e.g., for cancellation).
- Accumulate references to background tasks that need termination.
- Coordinate teardown across navigation, interaction, and DOM capture phases.

"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field


@dataclass
class SessionContext:
    """Tracks session-level state for a single HTML extraction or crawling run.

    Attributes:
        cleanup_started (bool):
            Flag indicating whether cleanup has been initiated. Used to prevent
            scheduling new async tasks or actions once shutdown has begun.

        background_tasks (List[asyncio.Task]):
            A list of all asyncio tasks that were started in fire-and-forget
            mode during the session. These tasks are explicitly cancelled during
            final teardown to prevent dangling work or memory leaks.

    """

    cleanup_started: bool = False
    background_tasks: list[asyncio.Task] = field(default_factory=list)
    last_logged_dom_hash: str | None = None


def create_session_context() -> SessionContext:
    """Create a new session context.

    Returns:
        New SessionContext instance with default values.
    """
    return SessionContext()
