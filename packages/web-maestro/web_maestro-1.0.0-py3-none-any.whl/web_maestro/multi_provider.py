"""Multi-provider WebMaestro implementation.

This module provides a simple interface for web content extraction
using multiple LLM providers with intelligent fallback strategies.
"""

from collections.abc import AsyncIterator
import logging
from typing import Any, Optional

from .providers import BaseLLMProvider, LLMConfig, ModelCapability, ProviderFactory

logger = logging.getLogger(__name__)


class WebMaestro:
    """Multi-provider web content extraction orchestrator.

    WebMaestro provides a high-level interface for web content extraction
    using multiple LLM providers with automatic failover and streaming support.

    Features:
        - Multi-provider LLM support with automatic fallback
        - Streaming content extraction for real-time responses
        - Provider health monitoring and testing
        - Configurable retry and timeout strategies

    Examples:
        # Single provider setup
        config = LLMConfig(provider="portkey", api_key="pk-...", model="gpt-4")
        maestro = WebMaestro(config=config)
        result = await maestro.extract_content("https://example.com")

        # Multi-provider with fallback
        maestro = WebMaestro(providers={
            "primary": {"provider": "portkey", "api_key": "pk-...", "model": "gpt-4"},
            "fallback": {"provider": "openai", "api_key": "sk-...", "model": "gpt-3.5-turbo"}
        })

        # Streaming extraction
        async for chunk in maestro.extract_content_stream(
            url="https://news-site.com",
            goal="Summarize latest articles"
        ):
            print(chunk, end="", flush=True)

    Note:
        This is a high-level orchestrator. For direct browser automation,
        use fetch_rendered_html() function directly.
    """

    def __init__(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        providers: Optional[dict[str, dict[str, Any]]] = None,
        config: Optional[LLMConfig] = None,
        **kwargs,
    ):
        """Initialize WebMaestro with LLM provider(s).

        Args:
            provider: Single provider name (openai, anthropic, portkey, ollama)
            model: Model name to use
            api_key: API key for the provider
            providers: Multi-provider configuration dict
            config: Complete LLM configuration object
            **kwargs: Additional provider-specific parameters
        """
        self.providers: dict[str, BaseLLMProvider] = {}
        self.primary_provider: Optional[BaseLLMProvider] = None

        if providers:
            # Multi-provider setup
            self._setup_multi_provider(providers)
        elif config:
            # Single provider from config
            self.primary_provider = ProviderFactory.create_from_config(config)
            self.providers["primary"] = self.primary_provider
        elif provider:
            # Single provider from parameters
            self.primary_provider = ProviderFactory.create_provider(
                provider=provider,
                model=model or self._get_default_model(provider),
                api_key=api_key,
                **kwargs,
            )
            self.providers["primary"] = self.primary_provider
        else:
            raise ValueError("Must provide either provider, providers dict, or config")

        logger.info(f"WebMaestro initialized with {len(self.providers)} provider(s)")

    def _setup_multi_provider(self, providers_config: dict[str, dict[str, Any]]):
        """Setup multiple providers from configuration.

        Args:
            providers_config: Dictionary mapping provider names to configs
        """
        self.providers = ProviderFactory.create_multi_provider(providers_config)

        # Set primary provider (first one or one marked as primary)
        if "primary" in self.providers:
            self.primary_provider = self.providers["primary"]
        else:
            self.primary_provider = next(iter(self.providers.values()))

    def _get_default_model(self, provider: str) -> str:
        """Get default model for provider.

        Args:
            provider: Provider name

        Returns:
            Default model name
        """
        defaults = {
            "openai": "gpt-4-turbo-preview",
            "anthropic": "claude-3-sonnet-20240229",
            "portkey": "gpt-4",
            "ollama": "llama2",
        }
        return defaults.get(provider, "gpt-4")

    @classmethod
    def from_portkey_config(cls, config_path: str) -> "WebMaestro":
        """Create WebMaestro from legacy Portkey config file.

        Args:
            config_path: Path to legacy config.json file

        Returns:
            Configured WebMaestro instance
        """
        from .providers.portkey import PortkeyProvider

        provider = PortkeyProvider.create_from_legacy_config(config_path)

        instance = cls.__new__(cls)
        instance.providers = {"primary": provider}
        instance.primary_provider = provider

        logger.info(f"WebMaestro created from legacy Portkey config: {config_path}")
        return instance

    async def extract_content(
        self,
        url: str,
        goal: str = "Extract all relevant content from this webpage",
        try_all_providers: bool = False,
        **kwargs,
    ) -> dict[str, Any]:
        """Extract content from a webpage.

        Args:
            url: Target URL to extract content from
            goal: Description of what to extract
            try_all_providers: Whether to try fallback providers on failure
            **kwargs: Additional extraction parameters

        Returns:
            Dictionary with extracted content and metadata
        """
        logger.info(f"Extracting content from: {url}")

        # For now, this is a simple implementation that uses the LLM
        # to generate extraction instructions. In the next phase, we'll
        # add the actual web fetching and processing logic.

        extraction_prompt = f"""
        Goal: {goal}
        URL: {url}

        Please provide instructions for extracting content from this webpage.
        Consider what type of content this URL likely contains and the best
        approach for extraction.

        Return your response in JSON format with:
        {{
            "url": "{url}",
            "extraction_strategy": "Description of recommended approach",
            "content_type": "Predicted content type (e.g., menu, article, product)",
            "instructions": "Step-by-step extraction instructions"
        }}
        """

        # Try primary provider first
        result = await self._try_provider(self.primary_provider, extraction_prompt)

        if result.success:
            return {
                "url": url,
                "content": result.content,
                "provider": result.provider,
                "model": result.model,
                "tokens_used": result.total_tokens,
                "response_time": result.response_time,
                "success": True,
            }

        # Try fallback providers if enabled
        if try_all_providers and len(self.providers) > 1:
            for name, provider in self.providers.items():
                if provider == self.primary_provider:
                    continue  # Already tried

                logger.info(f"Trying fallback provider: {name}")
                result = await self._try_provider(provider, extraction_prompt)

                if result.success:
                    return {
                        "url": url,
                        "content": result.content,
                        "provider": result.provider,
                        "model": result.model,
                        "tokens_used": result.total_tokens,
                        "response_time": result.response_time,
                        "success": True,
                        "fallback_used": name,
                    }

        # All providers failed
        return {
            "url": url,
            "content": "",
            "success": False,
            "error": result.error if result else "All providers failed",
            "providers_tried": list(self.providers.keys()),
        }

    async def _try_provider(self, provider: BaseLLMProvider, prompt: str):
        """Try extraction with a specific provider.

        Args:
            provider: LLM provider to use
            prompt: Extraction prompt

        Returns:
            LLM response
        """
        try:
            return await provider.complete(prompt, max_tokens=2000)
        except Exception as e:
            logger.error(f"Provider {provider.config.provider} failed: {e}")
            return provider._create_error_response(str(e))

    async def extract_content_stream(
        self,
        url: str,
        goal: str = "Extract all relevant content from this webpage",
        use_streaming: bool = True,
        **kwargs,
    ) -> AsyncIterator[str]:
        """Extract content from a webpage with streaming response.

        Args:
            url: Target URL to extract content from
            goal: Description of what to extract
            use_streaming: Whether to use streaming (default: True)
            **kwargs: Additional extraction parameters

        Yields:
            Chunks of extracted content as they become available
        """
        logger.info(f"Extracting content from {url} with streaming")

        extraction_prompt = f"""
        Goal: {goal}
        URL: {url}

        Analyze this webpage and extract the requested content.
        Provide a detailed response with all relevant information.
        """

        if use_streaming and self.primary_provider.supports_capability(
            ModelCapability.STREAMING
        ):
            # Use streaming completion
            async for chunk in self.primary_provider.complete_stream(
                extraction_prompt, **kwargs
            ):
                yield chunk
        else:
            # Fall back to non-streaming
            result = await self._try_provider(self.primary_provider, extraction_prompt)
            if result.success:
                yield result.content
            else:
                yield f"Error: {result.error}"

    async def test_providers(self) -> dict[str, dict[str, Any]]:
        """Test all configured providers.

        Returns:
            Dictionary with test results for each provider
        """
        results = {}

        test_prompt = (
            "Respond with 'Hello from [provider name]' to confirm you're working."
        )

        for name, provider in self.providers.items():
            logger.info(f"Testing provider: {name}")

            try:
                response = await provider.complete(test_prompt, max_tokens=50)

                results[name] = {
                    "success": response.success,
                    "provider": response.provider,
                    "model": response.model,
                    "response": response.content[:100],  # First 100 chars
                    "response_time": response.response_time,
                    "error": response.error,
                }

            except Exception as e:
                results[name] = {"success": False, "error": str(e)}

        return results

    def list_providers(self) -> list[str]:
        """List all configured providers.

        Returns:
            List of provider names
        """
        return list(self.providers.keys())

    def get_provider(self, name: str) -> Optional[BaseLLMProvider]:
        """Get a specific provider by name.

        Args:
            name: Provider name

        Returns:
            Provider instance or None if not found
        """
        return self.providers.get(name)

    def set_primary_provider(self, name: str) -> bool:
        """Set the primary provider.

        Args:
            name: Provider name to set as primary

        Returns:
            True if successful, False if provider not found
        """
        if name in self.providers:
            self.primary_provider = self.providers[name]
            logger.info(f"Primary provider set to: {name}")
            return True
        else:
            logger.error(f"Provider not found: {name}")
            return False
