"""Data models for playwright utilities."""

from .base import (
    CapturePhaseStrategy,
    ContentFilter,
    ContentProcessor,
    ErrorHandler,
    ExtractionStrategy,
    InteractionStrategy,
    MetricsCollector,
    NavigationStrategy,
    ResourceBlocker,
    ScrollStrategy,
    SessionManager,
    StabilityDetector,
)
from .content import ContentItem, ContentSection, ExtractedContent, StructuredContent
from .types import (
    CapturedBlock,
    CaptureResult,
    DOMElement,
    InteractionResult,
    PageMetrics,
    ScrollPosition,
)

__all__ = [
    # Base interfaces
    "CapturePhaseStrategy",
    "CaptureResult",
    "CapturedBlock",
    "ContentFilter",
    "ContentItem",
    "ContentProcessor",
    "ContentSection",
    "DOMElement",
    "ErrorHandler",
    "ExtractedContent",
    "ExtractionStrategy",
    "InteractionResult",
    "InteractionStrategy",
    "MetricsCollector",
    "NavigationStrategy",
    "PageMetrics",
    "ResourceBlocker",
    "ScrollPosition",
    "ScrollStrategy",
    "SessionManager",
    "StabilityDetector",
    "StructuredContent",
]
