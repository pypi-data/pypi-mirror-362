"""Enhanced utility functions and helper classes for web_maestro.

This module provides both legacy web-related utilities and new enhanced utilities
with production-ready features for content extraction and processing.
"""

# Legacy tracing utilities
# Enhanced utilities
from .enhanced_fetch import ContentBlock, EnhancedFetcher, HTMLProcessor, HTTPClient
from .json_processor import JSONProcessor, extract_json_from_text, safe_json_parse
from .rate_limiter import RateLimitedBatchManager, RateLimiter, RateLimitStrategy
from .text_processor import (
    TextProcessor,
    chunk_with_overlap,
    clean_text,
    semantic_deduplicate,
)
from .trace_utils import log_trace_events, save_trace, setup_tracing, stop_tracing
from .url_processor import URLProcessor, normalize_url, validate_url_format

__all__ = [
    # Legacy tracing utilities
    "log_trace_events",
    "save_trace",
    "setup_tracing",
    "stop_tracing",
    # Enhanced HTTP and fetching
    "EnhancedFetcher",
    "HTTPClient",
    "HTMLProcessor",
    "ContentBlock",
    # JSON processing
    "JSONProcessor",
    "safe_json_parse",
    "extract_json_from_text",
    # Text processing
    "TextProcessor",
    "chunk_with_overlap",
    "semantic_deduplicate",
    "clean_text",
    # URL processing
    "URLProcessor",
    "normalize_url",
    "validate_url_format",
    # Rate limiting
    "RateLimiter",
    "RateLimitedBatchManager",
    "RateLimitStrategy",
]
