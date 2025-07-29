"""Base classes and interfaces for LLM providers."""

from abc import ABC, abstractmethod
import asyncio
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from enum import Enum
import logging
from typing import Any, Optional, Union

logger = logging.getLogger(__name__)


class ModelCapability(Enum):
    """Capabilities that models can support."""

    TEXT_COMPLETION = "text_completion"
    CHAT_COMPLETION = "chat_completion"
    VISION = "vision"
    FUNCTION_CALLING = "function_calling"
    STREAMING = "streaming"
    JSON_MODE = "json_mode"


@dataclass
class LLMConfig:
    """Configuration for LLM providers."""

    # Core settings
    provider: str
    model: str
    api_key: Optional[str] = None

    # Connection settings
    base_url: Optional[str] = None
    timeout: int = 30
    max_retries: int = 3

    # Generation settings
    temperature: float = 0.7
    max_tokens: int = 1000
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0

    # Provider-specific settings
    extra_params: dict[str, Any] = field(default_factory=dict)

    # Capabilities
    supported_capabilities: list[ModelCapability] = field(default_factory=list)


@dataclass
class LLMResponse:
    """Response from an LLM provider."""

    # Content
    content: str

    # Metadata
    provider: Optional[str] = None
    model: Optional[str] = None

    # Usage information
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None

    # Response details
    finish_reason: Optional[str] = None
    response_time: Optional[float] = None

    # Error handling
    error: Optional[str] = None
    error_code: Optional[str] = None

    # Raw response (for debugging)
    raw_response: Optional[Any] = None

    @property
    def success(self) -> bool:
        """Check if the response was successful."""
        return self.error is None and bool(self.content.strip())

    @property
    def usage_cost(self) -> Optional[float]:
        """Calculate approximate cost (if token counts available)."""
        # This would need provider-specific pricing
        return None


class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers."""

    def __init__(self, config: LLMConfig):
        """Initialize the provider with configuration.

        Args:
            config: LLM configuration object
        """
        self.config = config
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self._client = None

        # Validate configuration
        self._validate_config()

    def _validate_config(self):
        """Validate the provider configuration."""
        if not self.config.provider:
            raise ValueError("Provider name is required")
        if not self.config.model:
            raise ValueError("Model name is required")

    @abstractmethod
    async def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate a text completion.

        Args:
            prompt: Input prompt text
            **kwargs: Additional generation parameters

        Returns:
            LLM response with generated content
        """
        pass

    @abstractmethod
    async def complete_chat(
        self, messages: list[dict[str, str]], **kwargs
    ) -> LLMResponse:
        """Generate a chat completion.

        Args:
            messages: List of chat messages with 'role' and 'content'
            **kwargs: Additional generation parameters

        Returns:
            LLM response with generated content
        """
        pass

    async def complete_stream(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        """Generate a streaming text completion.

        Args:
            prompt: Input prompt text
            **kwargs: Additional generation parameters

        Yields:
            Chunks of generated text as they become available
        """
        # Default implementation falls back to non-streaming
        response = await self.complete(prompt, **kwargs)
        if response.success:
            yield response.content

    async def complete_chat_stream(
        self, messages: list[dict[str, str]], **kwargs
    ) -> AsyncIterator[str]:
        """Generate a streaming chat completion.

        Args:
            messages: List of chat messages with 'role' and 'content'
            **kwargs: Additional generation parameters

        Yields:
            Chunks of generated text as they become available
        """
        # Default implementation falls back to non-streaming
        response = await self.complete_chat(messages, **kwargs)
        if response.success:
            yield response.content

    async def complete_vision(
        self, prompt: str, images: list[Union[str, bytes]], **kwargs
    ) -> LLMResponse:
        """Generate completion with vision capabilities.

        Args:
            prompt: Text prompt
            images: List of image URLs or binary data
            **kwargs: Additional parameters

        Returns:
            LLM response with analysis of images and text
        """
        if ModelCapability.VISION not in self.config.supported_capabilities:
            return LLMResponse(
                content="",
                error="Vision capabilities not supported by this model",
                error_code="CAPABILITY_NOT_SUPPORTED",
                provider=self.config.provider,
                model=self.config.model,
            )

        # Default implementation - subclasses should override
        return await self.complete(prompt, **kwargs)

    @abstractmethod
    def supports_capability(self, capability: ModelCapability) -> bool:
        """Check if the provider supports a specific capability.

        Args:
            capability: Capability to check

        Returns:
            True if supported, False otherwise
        """
        pass

    @abstractmethod
    def get_available_models(self) -> list[str]:
        """Get list of available models for this provider.

        Returns:
            List of model names
        """
        pass

    async def validate_connection(self) -> bool:
        """Validate that the provider connection works.

        Returns:
            True if connection is valid, False otherwise
        """
        try:
            response = await self.complete("Test", max_tokens=5)
            return response.success
        except Exception as e:
            self.logger.error(f"Connection validation failed: {e}")
            return False

    def _prepare_generation_params(self, **kwargs) -> dict[str, Any]:
        """Prepare generation parameters, merging config and kwargs.

        Args:
            **kwargs: Override parameters

        Returns:
            Merged parameters dictionary
        """
        params = {
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "top_p": self.config.top_p,
            "frequency_penalty": self.config.frequency_penalty,
            "presence_penalty": self.config.presence_penalty,
        }

        # Override with provided kwargs
        params.update(kwargs)

        # Add provider-specific params
        params.update(self.config.extra_params)

        return params

    async def _handle_rate_limit(self, retry_count: int = 0) -> bool:
        """Handle rate limiting with exponential backoff.

        Args:
            retry_count: Current retry attempt

        Returns:
            True if should retry, False if max retries exceeded
        """
        if retry_count >= self.config.max_retries:
            return False

        # Exponential backoff: 2^retry_count seconds
        wait_time = 2**retry_count
        self.logger.warning(
            f"Rate limited, waiting {wait_time}s before retry {retry_count + 1}"
        )

        await asyncio.sleep(wait_time)
        return True

    def _create_error_response(
        self, error_message: str, error_code: Optional[str] = None
    ) -> LLMResponse:
        """Create a standardized error response.

        Args:
            error_message: Error description
            error_code: Optional error code

        Returns:
            LLMResponse with error information
        """
        return LLMResponse(
            content="",
            error=error_message,
            error_code=error_code,
            provider=self.config.provider,
            model=self.config.model,
        )

    def __repr__(self) -> str:
        """String representation of the provider."""
        return f"{self.__class__.__name__}(provider={self.config.provider}, model={self.config.model})"
