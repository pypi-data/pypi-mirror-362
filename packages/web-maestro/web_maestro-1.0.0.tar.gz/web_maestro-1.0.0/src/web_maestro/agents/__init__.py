"""Agent integration interfaces for playwright utilities."""

from .scout_bridge import NavigationAction, NavigationContext, NavigationDecision

__all__ = [
    "NavigationAction",
    "NavigationContext",
    "NavigationDecision",
]
