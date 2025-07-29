"""Provider factory and registry for LLM providers."""

import logging
from typing import Any, Optional

from .base import BaseLLMProvider, LLMConfig

logger = logging.getLogger(__name__)


class ProviderRegistry:
    """Registry for LLM provider implementations."""

    _providers: dict[str, type[BaseLLMProvider]] = {}

    @classmethod
    def register(cls, name: str, provider_class: type[BaseLLMProvider]):
        """Register a provider implementation.

        Args:
            name: Provider name (e.g., 'openai', 'anthropic')
            provider_class: Provider implementation class
        """
        if not issubclass(provider_class, BaseLLMProvider):
            raise ValueError("Provider class must inherit from BaseLLMProvider")

        cls._providers[name.lower()] = provider_class
        logger.info(f"Registered provider: {name}")

    @classmethod
    def get_provider_class(cls, name: str) -> type[BaseLLMProvider]:
        """Get provider class by name.

        Args:
            name: Provider name

        Returns:
            Provider class

        Raises:
            ValueError: If provider is not registered
        """
        provider_class = cls._providers.get(name.lower())
        if not provider_class:
            available = ", ".join(cls._providers.keys())
            raise ValueError(f"Unknown provider '{name}'. Available: {available}")

        return provider_class

    @classmethod
    def list_providers(cls) -> list[str]:
        """List all registered provider names.

        Returns:
            List of provider names
        """
        return list(cls._providers.keys())

    @classmethod
    def is_registered(cls, name: str) -> bool:
        """Check if a provider is registered.

        Args:
            name: Provider name

        Returns:
            True if registered, False otherwise
        """
        return name.lower() in cls._providers


class ProviderFactory:
    """Factory for creating LLM provider instances."""

    @staticmethod
    def create_provider(
        provider: str,
        model: str,
        api_key: Optional[str] = None,
        config: Optional[LLMConfig] = None,
        **kwargs,
    ) -> BaseLLMProvider:
        """Create a provider instance.

        Args:
            provider: Provider name (e.g., 'openai', 'anthropic')
            model: Model name
            api_key: API key for the provider
            config: Complete LLM configuration (overrides other params)
            **kwargs: Additional configuration parameters

        Returns:
            Configured provider instance

        Raises:
            ValueError: If provider is not registered or configuration is invalid
        """
        # Use provided config or create new one
        if config is None:
            config = LLMConfig(
                provider=provider, model=model, api_key=api_key, **kwargs
            )

        # Get provider class and create instance
        provider_class = ProviderRegistry.get_provider_class(provider)

        try:
            instance = provider_class(config)
            logger.info(f"Created {provider} provider with model {model}")
            return instance
        except Exception as e:
            logger.error(f"Failed to create {provider} provider: {e}")
            raise ValueError(f"Failed to create provider '{provider}': {e}") from e

    @staticmethod
    def create_from_config(config: LLMConfig) -> BaseLLMProvider:
        """Create provider from configuration object.

        Args:
            config: LLM configuration

        Returns:
            Configured provider instance
        """
        return ProviderFactory.create_provider(
            config.provider, config.model, config=config
        )

    @staticmethod
    def create_multi_provider(
        providers_config: dict[str, dict[str, Any]],
    ) -> dict[str, BaseLLMProvider]:
        """Create multiple providers from configuration.

        Args:
            providers_config: Dictionary mapping provider names to their configs

        Returns:
            Dictionary of provider instances

        Example:
            config = {
                "primary": {"provider": "openai", "model": "gpt-4", "api_key": "..."},
                "fallback": {"provider": "anthropic", "model": "claude-3", "api_key": "..."}
            }
            providers = ProviderFactory.create_multi_provider(config)
        """
        providers = {}

        for name, config_dict in providers_config.items():
            try:
                provider = ProviderFactory.create_provider(**config_dict)
                providers[name] = provider
                logger.info(f"Created provider '{name}': {config_dict['provider']}")
            except Exception as e:
                logger.error(f"Failed to create provider '{name}': {e}")
                # Continue with other providers rather than failing completely

        if not providers:
            raise ValueError("No providers could be created from configuration")

        return providers


# Auto-register providers when they're imported
def _auto_register_providers():
    """Automatically register available provider implementations."""
    try:
        from .openai import OpenAIProvider

        if hasattr(OpenAIProvider, "__mro__") and issubclass(
            OpenAIProvider, BaseLLMProvider
        ):
            ProviderRegistry.register("openai", OpenAIProvider)
    except (ImportError, TypeError):
        logger.debug("OpenAI provider not available")

    try:
        from .anthropic import AnthropicProvider

        if hasattr(AnthropicProvider, "__mro__") and issubclass(
            AnthropicProvider, BaseLLMProvider
        ):
            ProviderRegistry.register("anthropic", AnthropicProvider)
    except (ImportError, TypeError):
        logger.debug("Anthropic provider not available")

    try:
        from .portkey import PortkeyProvider

        if hasattr(PortkeyProvider, "__mro__") and issubclass(
            PortkeyProvider, BaseLLMProvider
        ):
            ProviderRegistry.register("portkey", PortkeyProvider)
    except (ImportError, TypeError):
        logger.debug("Portkey provider not available")

    try:
        from .ollama import OllamaProvider

        if hasattr(OllamaProvider, "__mro__") and issubclass(
            OllamaProvider, BaseLLMProvider
        ):
            ProviderRegistry.register("ollama", OllamaProvider)
    except (ImportError, TypeError):
        logger.debug("Ollama provider not available")


# Register providers on module import
_auto_register_providers()


# Convenience function at module level
def create_provider(
    provider: str,
    model: str,
    api_key: Optional[str] = None,
    config: Optional[LLMConfig] = None,
    **kwargs,
) -> BaseLLMProvider:
    """Convenience function to create a provider instance.

    Args:
        provider: Provider name (e.g., 'openai', 'anthropic')
        model: Model name
        api_key: API key for the provider
        config: Complete LLM configuration (overrides other params)
        **kwargs: Additional configuration parameters

    Returns:
        Configured provider instance
    """
    return ProviderFactory.create_provider(
        provider=provider, model=model, api_key=api_key, config=config, **kwargs
    )
