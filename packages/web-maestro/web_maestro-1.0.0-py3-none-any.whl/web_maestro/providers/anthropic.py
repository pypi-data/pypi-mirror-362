"""Anthropic provider implementation."""

import logging
import time

try:
    from anthropic import AsyncAnthropic

    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

    # Create dummy class for type hints when Anthropic is not available
    class AsyncAnthropic:
        pass


from .base import BaseLLMProvider, LLMConfig, LLMResponse, ModelCapability

logger = logging.getLogger(__name__)


class AnthropicProvider(BaseLLMProvider):
    """Anthropic provider for Claude models."""

    def __init__(self, config: LLMConfig):
        """Initialize Anthropic provider.

        Args:
            config: LLM configuration with Anthropic-specific settings
        """
        if not ANTHROPIC_AVAILABLE:
            raise ImportError(
                "Anthropic package not installed. Install with: pip install anthropic"
            )

        # Set default capabilities for Anthropic models
        if not config.supported_capabilities:
            config.supported_capabilities = [
                ModelCapability.TEXT_COMPLETION,
                ModelCapability.CHAT_COMPLETION,
                ModelCapability.VISION,  # Claude 3 supports vision
            ]

        super().__init__(config)

        # Initialize Anthropic client
        self._client = self._create_client()

        logger.info(f"Initialized Anthropic provider with model: {config.model}")

    def _create_client(self) -> AsyncAnthropic:
        """Create Anthropic async client instance."""
        try:
            client_params = {
                "api_key": self.config.api_key,
                "timeout": self.config.timeout,
            }

            # Add optional parameters
            if self.config.base_url:
                client_params["base_url"] = self.config.base_url

            return AsyncAnthropic(**client_params)

        except Exception as e:
            logger.error(f"Failed to create Anthropic client: {e}")
            raise ValueError(f"Invalid Anthropic configuration: {e}") from e

    async def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate text completion using Anthropic.

        Args:
            prompt: Input prompt text
            **kwargs: Additional generation parameters

        Returns:
            LLM response with generated content
        """
        start_time = time.time()

        # Prepare generation parameters
        params = self._prepare_generation_params(**kwargs)

        try:
            response = await self._client.messages.create(
                model=self.config.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=params.get("max_tokens", self.config.max_tokens),
                temperature=params.get("temperature", self.config.temperature),
                top_p=params.get("top_p", self.config.top_p),
            )

            response_time = time.time() - start_time

            # Extract content from response
            content = ""
            if response.content:
                content = "".join(
                    [block.text for block in response.content if hasattr(block, "text")]
                )

            return LLMResponse(
                content=content,
                provider=self.config.provider,
                model=self.config.model,
                prompt_tokens=(
                    response.usage.input_tokens if hasattr(response, "usage") else None
                ),
                completion_tokens=(
                    response.usage.output_tokens if hasattr(response, "usage") else None
                ),
                total_tokens=(
                    (response.usage.input_tokens + response.usage.output_tokens)
                    if hasattr(response, "usage")
                    else None
                ),
                finish_reason=(
                    response.stop_reason if hasattr(response, "stop_reason") else None
                ),
                response_time=response_time,
                raw_response=response,
            )

        except Exception as e:
            logger.error(f"Anthropic completion failed: {e}")
            return self._create_error_response(
                f"Anthropic completion failed: {e}", "COMPLETION_FAILED"
            )

    async def complete_chat(
        self, messages: list[dict[str, str]], **kwargs
    ) -> LLMResponse:
        """Generate chat completion using Anthropic.

        Args:
            messages: List of chat messages
            **kwargs: Additional generation parameters

        Returns:
            LLM response with generated content
        """
        # Anthropic uses the same messages API for chat
        # Convert messages to Anthropic format if needed
        return await self.complete_messages(messages, **kwargs)

    async def complete_messages(
        self, messages: list[dict[str, str]], **kwargs
    ) -> LLMResponse:
        """Generate completion using Anthropic messages API.

        Args:
            messages: List of messages
            **kwargs: Additional parameters

        Returns:
            LLM response
        """
        start_time = time.time()

        # Prepare generation parameters
        params = self._prepare_generation_params(**kwargs)

        try:
            response = await self._client.messages.create(
                model=self.config.model,
                messages=messages,
                max_tokens=params.get("max_tokens", self.config.max_tokens),
                temperature=params.get("temperature", self.config.temperature),
                top_p=params.get("top_p", self.config.top_p),
            )

            response_time = time.time() - start_time

            # Extract content from response
            content = ""
            if response.content:
                content = "".join(
                    [block.text for block in response.content if hasattr(block, "text")]
                )

            return LLMResponse(
                content=content,
                provider=self.config.provider,
                model=self.config.model,
                prompt_tokens=(
                    response.usage.input_tokens if hasattr(response, "usage") else None
                ),
                completion_tokens=(
                    response.usage.output_tokens if hasattr(response, "usage") else None
                ),
                total_tokens=(
                    (response.usage.input_tokens + response.usage.output_tokens)
                    if hasattr(response, "usage")
                    else None
                ),
                finish_reason=(
                    response.stop_reason if hasattr(response, "stop_reason") else None
                ),
                response_time=response_time,
                raw_response=response,
            )

        except Exception as e:
            logger.error(f"Anthropic messages completion failed: {e}")
            return self._create_error_response(
                f"Anthropic messages completion failed: {e}",
                "MESSAGES_COMPLETION_FAILED",
            )

    def supports_capability(self, capability: ModelCapability) -> bool:
        """Check if the provider supports a specific capability.

        Args:
            capability: Capability to check

        Returns:
            True if supported, False otherwise
        """
        return capability in self.config.supported_capabilities

    def get_available_models(self) -> list[str]:
        """Get list of available Anthropic models.

        Returns:
            List of model names
        """
        return [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-2.1",
            "claude-2.0",
        ]
