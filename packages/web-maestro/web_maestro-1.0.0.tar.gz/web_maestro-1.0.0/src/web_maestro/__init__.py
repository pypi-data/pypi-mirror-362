"""Web Maestro - Production-ready web content extraction with multi-provider LLM support.

Web Maestro combines advanced web scraping capabilities with AI-powered content analysis.
It provides browser automation using Playwright and integrates with multiple LLM providers
for intelligent content extraction and structuring.

## Key Features

- **Browser Automation**: Playwright-powered dynamic content extraction
- **Multi-Provider LLM**: OpenAI, Anthropic, Portkey, and Ollama support
- **Streaming Support**: Real-time content delivery
- **Type Safety**: Comprehensive type hints and Pydantic models
- **Production Ready**: Error handling, rate limiting, and caching

## Quick Start

### Basic Content Extraction
```python
import asyncio
from web_maestro import fetch_rendered_html, SessionContext
from web_maestro.providers.portkey import PortkeyProvider
from web_maestro import LLMConfig


async def extract_content():
    # Configure LLM provider
    config = LLMConfig(
        provider="portkey",
        api_key="your-api-key",
        model="gpt-4",
        base_url="your-endpoint",
        extra_params={"virtual_key": "your-virtual-key"},
    )

    provider = PortkeyProvider(config)

    # Extract content with browser automation
    ctx = SessionContext()
    blocks = await fetch_rendered_html("https://example.com", ctx)

    if blocks:
        content = "\\n".join([block.content for block in blocks[:20]])
        response = await provider.complete(f"Analyze: {content[:3000]}")

        if response.success:
            print("Analysis:", response.content)


asyncio.run(extract_content())
```

### Streaming Analysis
```python
async def stream_analysis():
    config = LLMConfig(provider="portkey", api_key="key", model="gpt-4")
    provider = PortkeyProvider(config)

    async for chunk in provider.complete_stream("Analyze web scraping trends"):
        print(chunk, end="", flush=True)
```

### Enhanced Fetching
```python
from web_maestro.utils import EnhancedFetcher


async def smart_fetch():
    fetcher = EnhancedFetcher(cache_ttl=300)
    blocks = await fetcher.try_static_first("https://example.com")

    for block in blocks:
        print(f"[{block.content_type}] {block.content[:100]}...")
```
"""

from __future__ import annotations

from typing import Optional

from .__about__ import __version__

# Configuration helpers
from .config.base import create_default_config
from .context import SessionContext

# Crawling functionality
from .crawl import crawl_with_depth, flatten_crawl_results

# Content detectors
from .detectors import (
    ContentElementDetector,
    ContentLinkDetector,
    GenericContentElementDetector,
    GenericContentLinkDetector,
    analyze_elements_for_content,
    analyze_links_for_content,
    create_element_detector,
    create_link_detector,
    extract_images_from_static_blocks,
    find_all_images_comprehensive,
    is_likely_content_image,
    is_valid_image_url,
)

# Exceptions
from .exceptions import ConfigurationError, FetchError, LLMError, WebMaestroError
from .fetch import fetch_rendered_html

# Legacy compatibility (for existing code migration)
from .models import CapturedBlock

# Core multi-provider functionality
from .multi_provider import WebMaestro

# Content processors
from .processors import (
    BaseProcessor,
    ChainProcessor,
    HTMLCleanerProcessor,
    JSONExtractorProcessor,
    MultimodalProcessor,
)
from .providers import LLMConfig, LLMResponse, ModelCapability
from .providers.factory import ProviderRegistry, create_provider

# Enhanced utilities (main new features)
from .utils import (  # Utility functions
    EnhancedFetcher,
    JSONProcessor,
    RateLimiter,
    TextProcessor,
    URLProcessor,
    chunk_with_overlap,
    normalize_url,
    safe_json_parse,
    validate_url_format,
)

# PDF processor may not be available if dependencies are missing
try:
    from .processors import PDFProcessor

    PDF_PROCESSOR_AVAILABLE = True
except ImportError:
    PDFProcessor = None
    PDF_PROCESSOR_AVAILABLE = False

# Main exports for public API
__all__ = [
    # Version
    "__version__",
    # Core classes
    "WebMaestro",
    "LLMConfig",
    "LLMResponse",
    "ModelCapability",
    "ProviderRegistry",
    # Utility classes
    "EnhancedFetcher",
    "URLProcessor",
    "TextProcessor",
    "JSONProcessor",
    "RateLimiter",
    # Legacy compatibility
    "CapturedBlock",
    "SessionContext",
    "fetch_rendered_html",
    # Utility functions
    "normalize_url",
    "validate_url_format",
    "chunk_with_overlap",
    "safe_json_parse",
    "create_provider",
    "create_default_config",
    # Exceptions
    "WebMaestroError",
    "FetchError",
    "LLMError",
    "ConfigurationError",
    # Convenience functions
    "get_version",
    "list_providers",
    "create_maestro",
    # Crawling functionality
    "crawl_with_depth",
    "flatten_crawl_results",
    # Content processors
    "BaseProcessor",
    "ChainProcessor",
    "HTMLCleanerProcessor",
    "JSONExtractorProcessor",
    "MultimodalProcessor",
    # Content detectors
    "ContentElementDetector",
    "ContentLinkDetector",
    "GenericContentElementDetector",
    "GenericContentLinkDetector",
    "analyze_elements_for_content",
    "analyze_links_for_content",
    "create_element_detector",
    "create_link_detector",
    "extract_images_from_static_blocks",
    "find_all_images_comprehensive",
    "is_likely_content_image",
    "is_valid_image_url",
]

# Add PDFProcessor to __all__ only if it's available
if PDF_PROCESSOR_AVAILABLE:
    __all__.append("PDFProcessor")


def get_version() -> str:
    """Get the current version of web-maestro."""
    return __version__


def list_providers() -> list[str]:
    """List available LLM providers."""
    return list(ProviderRegistry.list_providers())


def create_maestro(
    provider: str, api_key: str | None = None, model: str | None = None, **kwargs
) -> WebMaestro:
    """Convenience function to create a WebMaestro instance.

    Args:
        provider: LLM provider name ("openai", "anthropic", "portkey", "ollama")
        api_key: API key for the provider (if required)
        model: Model name to use
        **kwargs: Additional configuration options

    Returns:
        Configured WebMaestro instance

    Example:
        >>> maestro = create_maestro("openai", api_key="sk-...", model="gpt-4")
        >>> result = await maestro.extract_content("https://example.com")
    """
    config = LLMConfig(provider=provider, api_key=api_key, model=model, **kwargs)
    return WebMaestro(config=config)
