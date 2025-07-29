"""Compatibility bridge for maestro to use enhanced web_maestro utilities.

This module provides backward-compatible access to enhanced utilities
while maintaining the existing maestro API. It allows maestro to optionally
use new enhanced utilities without breaking existing code.
"""

import asyncio
from functools import wraps
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Flag to enable enhanced utilities
_USE_ENHANCED_UTILS = False
_enhanced_fetcher = None
_url_processor = None
_text_processor = None


def enable_enhanced_utilities():
    """Enable enhanced utilities for better performance and features."""
    global _USE_ENHANCED_UTILS, _enhanced_fetcher, _url_processor, _text_processor

    try:
        from .utils import EnhancedFetcher, TextProcessor, URLProcessor

        _enhanced_fetcher = EnhancedFetcher()
        _url_processor = URLProcessor()
        _text_processor = TextProcessor()
        _USE_ENHANCED_UTILS = True

        logger.info("Enhanced web_maestro utilities enabled")
        return True

    except ImportError as e:
        logger.warning(f"Could not enable enhanced utilities: {e}")
        return False


def disable_enhanced_utilities():
    """Disable enhanced utilities and use legacy functions."""
    global _USE_ENHANCED_UTILS, _enhanced_fetcher, _url_processor, _text_processor

    _USE_ENHANCED_UTILS = False
    _enhanced_fetcher = None
    _url_processor = None
    _text_processor = None

    logger.info("Enhanced web_maestro utilities disabled")


def is_enhanced_enabled() -> bool:
    """Check if enhanced utilities are enabled."""
    return _USE_ENHANCED_UTILS


# Enhanced URL utilities with backward compatibility
async def try_static_first(url: str, **kwargs) -> Optional[list[Any]]:
    """Try static content extraction first, with enhanced utilities if available.

    This provides the try_static_html functionality that was requested to be
    moved from maestro utils to web_maestro.

    Args:
        url: URL to fetch
        **kwargs: Additional arguments for fetching

    Returns:
        List of content blocks if successful, None otherwise
    """
    if _USE_ENHANCED_UTILS and _enhanced_fetcher:
        try:
            # Use enhanced fetcher with static-first strategy
            blocks = await _enhanced_fetcher.try_static_first(url, **kwargs)
            return blocks
        except Exception as e:
            logger.warning(f"Enhanced fetch failed, falling back to legacy: {e}")

    # Fallback to existing maestro utilities
    try:
        from maestro.src.utils.fetch import try_static_request_first

        return await try_static_request_first(url, **kwargs)
    except Exception as e:
        logger.error(f"Static fetch failed: {e}")
        return None


def normalize_url_enhanced(url: str, **kwargs) -> str:
    """Normalize URL with enhanced processing if available."""
    if _USE_ENHANCED_UTILS and _url_processor:
        try:
            return _url_processor.normalize_cached(url, **kwargs)
        except Exception as e:
            logger.warning(f"Enhanced URL normalization failed: {e}")

    # Fallback to existing maestro utilities
    try:
        from maestro.src.utils.url_utils import normalize_url

        return normalize_url(url)
    except Exception as e:
        logger.warning(f"URL normalization failed: {e}")
        return url


def validate_url_enhanced(url: str) -> bool:
    """Validate URL with enhanced processing if available."""
    if _USE_ENHANCED_UTILS and _url_processor:
        try:
            return _url_processor.validate_cached(url)
        except Exception as e:
            logger.warning(f"Enhanced URL validation failed: {e}")

    # Fallback to basic validation
    try:
        from urllib.parse import urlparse

        parsed = urlparse(url)
        return bool(parsed.scheme and parsed.netloc)
    except Exception:
        return False


def chunk_text_enhanced(
    text: str, max_tokens: int = 1000, overlap_tokens: int = 100, **kwargs
) -> list[dict[str, Any]]:
    """Chunk text with enhanced processing if available."""
    if _USE_ENHANCED_UTILS and _text_processor:
        try:
            return _text_processor.chunk_text_cached(
                text, max_tokens, overlap_tokens, **kwargs
            )
        except Exception as e:
            logger.warning(f"Enhanced text chunking failed: {e}")

    # Fallback to existing maestro utilities
    try:
        from maestro.src.utils.text_processing import chunk_by_tokens_with_overlap

        chunks = chunk_by_tokens_with_overlap(text, max_tokens, overlap_tokens)

        # Convert to enhanced format for consistency
        enhanced_chunks = []
        for i, chunk in enumerate(chunks):
            enhanced_chunks.append(
                {
                    "text": chunk,
                    "chunk_index": i,
                    "token_count": len(chunk.split()) * 1.3,  # Rough estimate
                    "word_count": len(chunk.split()),
                    "char_count": len(chunk),
                    "preview": chunk[:100] + "..." if len(chunk) > 100 else chunk,
                }
            )
        return enhanced_chunks

    except Exception as e:
        logger.warning(f"Text chunking failed: {e}")
        return [
            {
                "text": text,
                "chunk_index": 0,
                "token_count": len(text.split()) * 1.3,
                "word_count": len(text.split()),
                "char_count": len(text),
                "preview": text[:100],
            }
        ]


def process_json_enhanced(text: str, **kwargs) -> dict[str, Any]:
    """Process JSON from LLM response with enhanced utilities if available."""
    if _USE_ENHANCED_UTILS:
        try:
            from .utils import JSONProcessor

            processor = JSONProcessor()
            return processor.process_llm_response(text)
        except Exception as e:
            logger.warning(f"Enhanced JSON processing failed: {e}")

    # Fallback to basic JSON parsing
    import json

    try:
        return {"success": True, "data": json.loads(text), "parsing_method": "direct"}
    except json.JSONDecodeError:
        # Try to extract JSON from text
        import re

        json_pattern = r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}"
        matches = re.findall(json_pattern, text)

        for match in matches:
            try:
                data = json.loads(match)
                return {"success": True, "data": data, "parsing_method": "extraction"}
            except json.JSONDecodeError:
                continue

        return {
            "success": False,
            "error": "No valid JSON found",
            "parsing_method": "none",
        }


# Decorator for optional enhancement
def with_enhanced_fallback(fallback_func):
    """Decorator to provide enhanced functionality with fallback."""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if _USE_ENHANCED_UTILS:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    logger.warning(
                        f"Enhanced function {func.__name__} failed, using fallback: {e}"
                    )

            # Use fallback function
            if asyncio.iscoroutinefunction(fallback_func):
                return await fallback_func(*args, **kwargs)
            else:
                return fallback_func(*args, **kwargs)

        return wrapper

    return decorator


# Cleanup function
async def cleanup_enhanced_resources():
    """Clean up enhanced utility resources."""
    global _enhanced_fetcher

    if _enhanced_fetcher:
        try:
            await _enhanced_fetcher.close()
        except Exception as e:
            logger.warning(f"Error cleaning up enhanced fetcher: {e}")


# Auto-initialization attempt
def auto_enable_enhanced():
    """Automatically enable enhanced utilities if available."""
    try:
        return enable_enhanced_utilities()
    except Exception as e:
        logger.info(f"Enhanced utilities not available: {e}")
        return False


# Export compatibility functions
__all__ = [
    "enable_enhanced_utilities",
    "disable_enhanced_utilities",
    "is_enhanced_enabled",
    "try_static_first",
    "normalize_url_enhanced",
    "validate_url_enhanced",
    "chunk_text_enhanced",
    "process_json_enhanced",
    "with_enhanced_fallback",
    "cleanup_enhanced_resources",
    "auto_enable_enhanced",
]
