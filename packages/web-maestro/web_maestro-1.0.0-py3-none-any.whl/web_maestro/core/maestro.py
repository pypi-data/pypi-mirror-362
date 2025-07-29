"""Main WebMaestro class for intelligent web content extraction.

This module provides the primary interface for web content extraction with
multi-provider LLM support, smart navigation, and fallback strategies.
"""

import asyncio
import logging
from typing import Any, Optional

# Processor imports
from ..dom_capture.capture import CapturedBlock

# from ..extractors.html_extractor import HTMLExtractor  # Module doesn't exist
# from ..extractors.image_extractor import ImageExtractor  # Module doesn't exist
# from ..extractors.pdf_extractor import PDFExtractor  # Module doesn't exist
# from ..auth.manager import APIKeyManager  # Module doesn't exist
# from ..config.settings import WebMaestroSettings  # Module doesn't exist
# from ..detectors.base import ContentLinkDetector  # Module doesn't exist
from ..exceptions import WebMaestroError  # Using existing exception
from ..fetch import fetch_rendered_html
from ..models.content import StructuredContent
from ..processors import (
    ChainProcessor,
    HTMLCleanerProcessor,
    JSONExtractorProcessor,
    MultimodalProcessor,
)
from ..providers.base import LLMConfig
from ..providers.factory import ProviderFactory
from ..utils.enhanced_fetch import EnhancedFetcher  # Corrected import path
from ..utils.url_processor import (  # Corrected import path
    normalize_url,
    validate_url_format,
)

# PDF processor may not be available if dependencies are missing
try:
    from ..processors import PDFProcessor

    PDF_PROCESSOR_AVAILABLE = True
except ImportError:
    PDFProcessor = None
    PDF_PROCESSOR_AVAILABLE = False

logger = logging.getLogger(__name__)


# Placeholder classes for missing models
class ExtractionConfig:
    """Configuration for content extraction with processor support."""

    def __init__(
        self,
        try_static_first: bool = True,
        enable_ai_navigation: bool = False,
        max_navigation_steps: int = 3,
        # DOM capture configuration
        tab_timeout: int = 2000,
        max_tabs: int = 10,
        explore_elements: int = 25,
        expand_buttons: int = 10,
        dom_timeout_ms: int = 8000,
        # Processor configuration
        enable_processors: bool = True,
        processor_chain: list[str] | None = None,
        processor_config: dict[str, Any] | None = None,
        enable_multimodal: bool = False,
        pdf_extraction_method: str = "vision",  # "vision" or "text"
        clean_html: bool = True,
        extract_json: bool = True,
        **kwargs,
    ):
        self.try_static_first = try_static_first
        self.enable_ai_navigation = enable_ai_navigation
        self.max_navigation_steps = max_navigation_steps
        # DOM capture settings
        self.tab_timeout = tab_timeout
        self.max_tabs = max_tabs
        self.explore_elements = explore_elements
        self.expand_buttons = expand_buttons
        self.dom_timeout_ms = dom_timeout_ms
        # Processor settings
        self.enable_processors = enable_processors
        self.processor_chain = processor_chain or []
        self.processor_config = processor_config or {}
        self.enable_multimodal = enable_multimodal
        self.pdf_extraction_method = pdf_extraction_method
        self.clean_html = clean_html
        self.extract_json = extract_json
        for key, value in kwargs.items():
            setattr(self, key, value)


class WebMaestroResponse:
    """Placeholder response class for extraction results."""

    def __init__(
        self,
        url: str,
        success: bool,
        content: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
        extraction_method: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        error: Optional[str] = None,
    ):
        self.url = url
        self.success = success
        self.content = content
        self.metadata = metadata or {}
        self.extraction_method = extraction_method
        self.provider = provider
        self.model = model
        self.error = error


class APIKeyManager:
    """Placeholder API key manager."""

    def get_api_key(self, provider: str) -> Optional[str]:
        """Get API key from environment variables."""
        import os

        env_keys = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "portkey": "PORTKEY_API_KEY",
            "ollama": "OLLAMA_API_KEY",
        }
        return os.getenv(env_keys.get(provider.lower(), f"{provider.upper()}_API_KEY"))


class WebMaestroSettings:
    """Placeholder settings class."""

    def __init__(self):
        self.default_provider = "openai"
        self.default_timeout = 30
        self.max_retries = 3


class WebMaestro:
    """Main class for intelligent web content extraction.

    Examples:
        # Simple usage with environment variables
        maestro = WebMaestro()
        result = await maestro.extract("https://example.com")

        # With specific provider
        maestro = WebMaestro(provider="openai", api_key="sk-...")
        result = await maestro.extract("https://example.com", goal="Extract menu items")

        # With custom configuration
        config = ExtractionConfig(
            try_static_first=True,
            enable_ai_navigation=True,
            max_navigation_steps=3
        )
        result = await maestro.extract("https://example.com", config=config)
    """

    def __init__(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        config: Optional[LLMConfig] = None,
        settings: Optional[WebMaestroSettings] = None,
        key_manager: Optional[APIKeyManager] = None,
        # link_detectors: Optional[list[ContentLinkDetector]] = None,  # Module doesn't exist
        **kwargs,
    ):
        """Initialize WebMaestro with LLM provider and configuration.

        Args:
            provider: LLM provider name (openai, anthropic, portkey, ollama)
            model: Model name to use
            api_key: API key for the provider
            base_url: Custom base URL for the provider
            config: Complete LLM configuration object
            settings: Global settings object
            key_manager: Custom API key manager
            # link_detectors: List of content link detectors  # Module doesn't exist
            **kwargs: Additional provider-specific parameters
        """
        self.settings = settings or WebMaestroSettings()
        self.key_manager = key_manager or APIKeyManager()

        # Set up LLM provider
        if config:
            self.llm_config = config
        else:
            self.llm_config = self._create_llm_config(
                provider, model, api_key, base_url, **kwargs
            )

        self.provider = ProviderFactory.create_from_config(self.llm_config)

        # Set up components
        self.fetcher = EnhancedFetcher(
            timeout=self.settings.default_timeout, max_retries=self.settings.max_retries
        )

        # self.link_detectors = link_detectors or []  # Module doesn't exist

        # TODO: Set up extractors when modules are available
        # self.html_extractor = HTMLExtractor(self.provider)
        # self.pdf_extractor = PDFExtractor(self.provider)
        # self.image_extractor = ImageExtractor(self.provider)

        logger.info(f"WebMaestro initialized with provider: {self.llm_config.provider}")

    def _create_llm_config(
        self,
        provider: Optional[str],
        model: Optional[str],
        api_key: Optional[str],
        base_url: Optional[str],
        **kwargs,
    ) -> LLMConfig:
        """Create LLM configuration from parameters."""
        # Use provided values or fall back to settings/environment
        provider = provider or self.settings.default_provider

        # Get API key from multiple sources
        if not api_key:
            api_key = self.key_manager.get_api_key(provider)

        if not api_key:
            raise WebMaestroError(f"No API key found for provider: {provider}")

        return LLMConfig(
            provider=provider,
            model=model or self._get_default_model(provider),
            api_key=api_key,
            base_url=base_url,
            timeout=self.settings.default_timeout,
            **kwargs,
        )

    def _create_processor_chain(self, config: ExtractionConfig) -> ChainProcessor:
        """Create a chain of processors based on configuration.

        Args:
            config: Extraction configuration

        Returns:
            ChainProcessor with configured processors
        """
        processors = []

        # Add processors based on config or defaults
        if config.processor_chain:
            # Use explicitly configured processors
            for processor_name in config.processor_chain:
                if processor_name == "html_cleaner" and config.clean_html:
                    processors.append(HTMLCleanerProcessor())
                elif processor_name == "json_extractor" and config.extract_json:
                    processors.append(JSONExtractorProcessor())
                elif (
                    processor_name == "pdf"
                    and self.provider
                    and PDF_PROCESSOR_AVAILABLE
                ):
                    pdf_config = config.processor_config.get("pdf", {})
                    # Use processor-specific method if provided, otherwise fall back to global config
                    method = pdf_config.get("method", config.pdf_extraction_method)
                    processors.append(
                        PDFProcessor(
                            provider=self.provider,
                            method=method,
                            **{k: v for k, v in pdf_config.items() if k != "method"},
                        )
                    )
                elif processor_name == "pdf" and not PDF_PROCESSOR_AVAILABLE:
                    logger.warning(
                        "PDF processor requested but dependencies not available. Install with: pip install pdf2image pillow"
                    )
                elif (
                    processor_name == "multimodal"
                    and config.enable_multimodal
                    and self.provider
                ):
                    processors.append(
                        MultimodalProcessor(
                            provider=self.provider,
                            **config.processor_config.get("multimodal", {}),
                        )
                    )
        else:
            # Default processor chain
            if config.clean_html:
                processors.append(HTMLCleanerProcessor())
            if config.extract_json:
                processors.append(JSONExtractorProcessor())
            if config.enable_multimodal and self.provider:
                processors.append(
                    MultimodalProcessor(provider=self.provider, content_type="auto")
                )

        return ChainProcessor(processors) if processors else None

    def _get_default_model(self, provider: str) -> str:
        """Get default model for provider."""
        defaults = {
            "openai": "gpt-4-turbo-preview",
            "anthropic": "claude-3-sonnet-20240229",
            "portkey": "gpt-4",
            "ollama": "llama2",
        }
        return defaults.get(provider, "gpt-4")

    async def extract(
        self,
        url: str,
        goal: str = "Extract all relevant content from this webpage",
        config: Optional[ExtractionConfig] = None,
        **kwargs,
    ) -> WebMaestroResponse:
        """Extract content from a single URL.

        Args:
            url: Target URL to extract content from
            goal: Description of what to extract
            config: Extraction configuration options
            **kwargs: Additional extraction parameters

        Returns:
            WebMaestroResponse with extracted content and metadata

        Raises:
            WebMaestroError: If URL is invalid or extraction fails
        """
        # Validate URL
        if not validate_url_format(url):
            raise WebMaestroError(f"Invalid URL format: {url}")

        # Normalize URL
        normalized_url = normalize_url(url)

        # Use default config if none provided
        if config is None:
            config = ExtractionConfig(**kwargs)

        logger.info(f"Starting extraction for: {normalized_url}")

        try:
            # Fetch content with browser and DOM capture
            # Create config dict with required DOM capture settings
            fetch_config = {
                "tab_timeout": getattr(config, "tab_timeout", 2000),
                "max_tabs": getattr(config, "max_tabs", 10),
                "explore_elements": getattr(config, "explore_elements", 25),
                "expand_buttons": getattr(config, "expand_buttons", 10),
                "dom_timeout_ms": getattr(config, "dom_timeout_ms", 8000),
                "scroll": True,  # Default to enable scrolling
            }
            raw_blocks = await fetch_rendered_html(normalized_url, config=fetch_config)

            if not raw_blocks:
                raise WebMaestroError(f"Failed to fetch content from {normalized_url}")

            # Convert to CapturedBlock objects if needed
            captured_blocks = []
            for block in raw_blocks:
                if isinstance(block, dict):
                    captured_blocks.append(
                        CapturedBlock(
                            content=block.get("content", ""),
                            source_id=block.get("source_id", ""),
                            capture_type=block.get("capture_type", "unknown"),
                        )
                    )
                elif hasattr(block, "content"):
                    captured_blocks.append(block)

            # Process blocks with configured processors
            if config.enable_processors:
                processor_chain = self._create_processor_chain(config)
                if processor_chain:
                    structured_content = await processor_chain.process(captured_blocks)
                else:
                    # No processors configured, return raw blocks
                    structured_content = StructuredContent(
                        source_name="RawCapture",
                        source_url=normalized_url,
                        domain="raw_capture",
                        sections=[],
                        extraction_metadata={"raw_blocks": len(captured_blocks)},
                    )
            else:
                # Processors disabled
                structured_content = StructuredContent(
                    source_name="DisabledProcessors",
                    source_url=normalized_url,
                    domain="disabled",
                    sections=[],
                    extraction_metadata={"processors_disabled": True},
                )

            # Convert structured content to response format
            content_items = []
            for section in structured_content.sections:
                for item in section.items:
                    content_items.append(
                        {
                            "name": item.name,
                            "description": item.description,
                            "metadata": item.metadata,
                        }
                    )

            return WebMaestroResponse(
                url=normalized_url,
                success=True,
                content=(
                    content_items
                    if content_items
                    else "No structured content extracted"
                ),
                metadata={
                    "goal": goal,
                    "total_blocks": len(captured_blocks),
                    "total_sections": len(structured_content.sections),
                    "processors_used": config.enable_processors,
                    **structured_content.extraction_metadata,
                },
                extraction_method="dom_capture_with_processors",
                provider=self.llm_config.provider,
                model=self.llm_config.model,
            )

        except Exception as e:
            logger.error(f"Extraction failed for {normalized_url}: {e}")
            return WebMaestroResponse(
                url=normalized_url,
                success=False,
                error=str(e),
                provider=self.llm_config.provider,
                model=self.llm_config.model,
            )

    async def extract_batch(
        self,
        urls: list[str],
        goal: str = "Extract all relevant content from these webpages",
        config: Optional[ExtractionConfig] = None,
        max_concurrent: int = 5,
        **kwargs,
    ) -> list[WebMaestroResponse]:
        """Extract content from multiple URLs concurrently.

        Args:
            urls: List of URLs to extract from
            goal: Description of what to extract
            config: Extraction configuration
            max_concurrent: Maximum concurrent extractions
            **kwargs: Additional extraction parameters

        Returns:
            List of WebMaestroResponse objects
        """
        logger.info(f"Starting batch extraction for {len(urls)} URLs")

        semaphore = asyncio.Semaphore(max_concurrent)

        async def extract_single(url: str) -> WebMaestroResponse:
            async with semaphore:
                return await self.extract(url, goal, config, **kwargs)

        tasks = [extract_single(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Convert exceptions to error responses
        responses = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                responses.append(
                    WebMaestroResponse(
                        url=urls[i],
                        success=False,
                        error=str(result),
                        provider=self.llm_config.provider,
                        model=self.llm_config.model,
                    )
                )
            else:
                responses.append(result)

        return responses

    async def discover_links(
        self,
        url: str,
        content_types: Optional[list[str]] = None,
        max_links: int = 20,
        confidence_threshold: float = 0.6,
    ) -> list[dict[str, Any]]:
        """Discover relevant content links from a webpage.

        Args:
            url: URL to analyze for links
            content_types: Types of content to look for
            max_links: Maximum number of links to return
            confidence_threshold: Minimum confidence score

        Returns:
            List of link analysis results
        """
        # TODO: Implement link discovery when detector modules are available
        logger.warning("Link detectors not implemented yet")
        return []

        # Placeholder implementation would go here
        # try:
        #     html_content = await self.fetcher.fetch_html(url)
        #     if not html_content:
        #         return []
        #
        #     # Simple link extraction as placeholder
        #     # Could use BeautifulSoup to find links
        #     return []
        # except Exception as e:
        #     logger.error(f"Link discovery failed for {url}: {e}")
        #     return []

    async def _detect_content_type(self, url: str) -> str:
        """Detect content type of URL."""
        try:
            return await self.fetcher.get_content_type(url)
        except Exception:
            return "text/html"  # Default fallback

    def add_link_detector(self, detector):
        """Add a content link detector (placeholder)."""
        # TODO: Implement when ContentLinkDetector module is available
        logger.warning("Link detector functionality not implemented yet")

    def set_provider(self, provider: str, **kwargs):
        """Switch to a different LLM provider."""
        # Extract known parameters
        model = kwargs.pop("model", None)
        api_key = kwargs.pop("api_key", None)
        base_url = kwargs.pop("base_url", None)

        self.llm_config = self._create_llm_config(
            provider, model=model, api_key=api_key, base_url=base_url, **kwargs
        )
        self.provider = ProviderFactory.create_from_config(self.llm_config)

        # TODO: Update extractors with new provider when modules are available
        # self.html_extractor.provider = self.provider
        # self.pdf_extractor.provider = self.provider
        # self.image_extractor.provider = self.provider

        logger.info(f"Switched to provider: {provider}")

    async def health_check(self) -> dict[str, Any]:
        """Check the health of the WebMaestro instance."""
        health = {
            "status": "healthy",
            "provider": self.llm_config.provider,
            "model": self.llm_config.model,
            "components": {},
        }

        try:
            # Test LLM provider
            test_response = await self.provider.complete("Test", max_tokens=5)
            health["components"]["llm_provider"] = {
                "status": "healthy" if not test_response.error else "unhealthy",
                "error": test_response.error,
            }
        except Exception as e:
            health["components"]["llm_provider"] = {
                "status": "unhealthy",
                "error": str(e),
            }
            health["status"] = "degraded"

        # Test fetch capabilities
        try:
            test_url = "https://httpbin.org/status/200"
            await self.fetcher.check_url_accessible(test_url)
            health["components"]["fetcher"] = {"status": "healthy"}
        except Exception as e:
            health["components"]["fetcher"] = {"status": "unhealthy", "error": str(e)}
            health["status"] = "degraded"

        return health
