"""OpenAI provider implementation."""

import base64
import logging
import time
from typing import Union

try:
    import openai
    from openai import AsyncOpenAI

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

    # Create dummy class for type hints when OpenAI is not available
    class AsyncOpenAI:
        pass


from .base import BaseLLMProvider, LLMConfig, LLMResponse, ModelCapability

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseLLMProvider):
    """OpenAI provider for GPT models."""

    def __init__(self, config: LLMConfig):
        """Initialize OpenAI provider.

        Args:
            config: LLM configuration with OpenAI-specific settings
        """
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "OpenAI package not installed. Install with: pip install openai"
            )

        # Set default capabilities for OpenAI models
        if not config.supported_capabilities:
            config.supported_capabilities = self._get_model_capabilities(config.model)

        super().__init__(config)

        # Initialize OpenAI client
        self._client = self._create_client()

        logger.info(f"Initialized OpenAI provider with model: {config.model}")

    def _get_model_capabilities(self, model: str) -> list[ModelCapability]:
        """Get capabilities for specific OpenAI model.

        Args:
            model: Model name

        Returns:
            List of supported capabilities
        """
        # GPT-4 Vision models
        if "gpt-4" in model and ("vision" in model or "turbo" in model):
            return [
                ModelCapability.TEXT_COMPLETION,
                ModelCapability.CHAT_COMPLETION,
                ModelCapability.VISION,
                ModelCapability.FUNCTION_CALLING,
                ModelCapability.STREAMING,
                ModelCapability.JSON_MODE,
            ]

        # GPT-4 models (non-vision)
        elif "gpt-4" in model:
            return [
                ModelCapability.TEXT_COMPLETION,
                ModelCapability.CHAT_COMPLETION,
                ModelCapability.FUNCTION_CALLING,
                ModelCapability.STREAMING,
                ModelCapability.JSON_MODE,
            ]

        # GPT-3.5 models
        elif "gpt-3.5" in model:
            return [
                ModelCapability.TEXT_COMPLETION,
                ModelCapability.CHAT_COMPLETION,
                ModelCapability.FUNCTION_CALLING,
                ModelCapability.STREAMING,
            ]

        # Default capabilities
        else:
            return [
                ModelCapability.TEXT_COMPLETION,
                ModelCapability.CHAT_COMPLETION,
            ]

    def _create_client(self) -> AsyncOpenAI:
        """Create OpenAI async client instance."""
        try:
            client_params = {
                "api_key": self.config.api_key,
                "timeout": self.config.timeout,
            }

            # Add optional parameters
            if self.config.base_url:
                client_params["base_url"] = self.config.base_url

            return AsyncOpenAI(**client_params)

        except Exception as e:
            logger.error(f"Failed to create OpenAI client: {e}")
            raise ValueError(f"Invalid OpenAI configuration: {e}") from e

    async def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate text completion using OpenAI.

        Args:
            prompt: Input prompt text
            **kwargs: Additional generation parameters

        Returns:
            LLM response with generated content
        """
        start_time = time.time()

        # Prepare generation parameters
        params = self._prepare_generation_params(**kwargs)

        retry_count = 0
        while retry_count <= self.config.max_retries:
            try:
                response = await self._client.chat.completions.create(
                    model=self.config.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=params.get("max_tokens", self.config.max_tokens),
                    temperature=params.get("temperature", self.config.temperature),
                    top_p=params.get("top_p", self.config.top_p),
                    frequency_penalty=params.get(
                        "frequency_penalty", self.config.frequency_penalty
                    ),
                    presence_penalty=params.get(
                        "presence_penalty", self.config.presence_penalty
                    ),
                    stream=False,
                )

                response_time = time.time() - start_time

                # Extract content
                content = response.choices[0].message.content or ""

                return LLMResponse(
                    content=content,
                    provider=self.config.provider,
                    model=self.config.model,
                    prompt_tokens=response.usage.prompt_tokens,
                    completion_tokens=response.usage.completion_tokens,
                    total_tokens=response.usage.total_tokens,
                    finish_reason=response.choices[0].finish_reason,
                    response_time=response_time,
                    raw_response=response,
                )

            except openai.RateLimitError as e:
                logger.warning(f"OpenAI rate limit hit: {e}")
                if not await self._handle_rate_limit(retry_count):
                    return self._create_error_response(
                        f"Rate limit exceeded after {self.config.max_retries} retries",
                        "RATE_LIMIT_EXCEEDED",
                    )
                retry_count += 1
                continue

            except openai.APIError as e:
                logger.error(f"OpenAI API error: {e}")
                return self._create_error_response(
                    f"OpenAI API error: {e}", "API_ERROR"
                )

            except Exception as e:
                logger.error(f"OpenAI completion failed: {e}")
                return self._create_error_response(
                    f"OpenAI completion failed: {e}", "COMPLETION_FAILED"
                )

    async def complete_chat(
        self, messages: list[dict[str, str]], **kwargs
    ) -> LLMResponse:
        """Generate chat completion using OpenAI.

        Args:
            messages: List of chat messages
            **kwargs: Additional generation parameters

        Returns:
            LLM response with generated content
        """
        start_time = time.time()

        # Prepare generation parameters
        params = self._prepare_generation_params(**kwargs)

        retry_count = 0
        while retry_count <= self.config.max_retries:
            try:
                response = await self._client.chat.completions.create(
                    model=self.config.model,
                    messages=messages,
                    max_tokens=params.get("max_tokens", self.config.max_tokens),
                    temperature=params.get("temperature", self.config.temperature),
                    top_p=params.get("top_p", self.config.top_p),
                    frequency_penalty=params.get(
                        "frequency_penalty", self.config.frequency_penalty
                    ),
                    presence_penalty=params.get(
                        "presence_penalty", self.config.presence_penalty
                    ),
                    stream=False,
                )

                response_time = time.time() - start_time

                # Extract content
                content = response.choices[0].message.content or ""

                return LLMResponse(
                    content=content,
                    provider=self.config.provider,
                    model=self.config.model,
                    prompt_tokens=response.usage.prompt_tokens,
                    completion_tokens=response.usage.completion_tokens,
                    total_tokens=response.usage.total_tokens,
                    finish_reason=response.choices[0].finish_reason,
                    response_time=response_time,
                    raw_response=response,
                )

            except openai.RateLimitError as e:
                logger.warning(f"OpenAI rate limit hit: {e}")
                if not await self._handle_rate_limit(retry_count):
                    return self._create_error_response(
                        f"Rate limit exceeded after {self.config.max_retries} retries",
                        "RATE_LIMIT_EXCEEDED",
                    )
                retry_count += 1
                continue

            except openai.APIError as e:
                logger.error(f"OpenAI API error: {e}")
                return self._create_error_response(
                    f"OpenAI API error: {e}", "API_ERROR"
                )

            except Exception as e:
                logger.error(f"OpenAI chat completion failed: {e}")
                return self._create_error_response(
                    f"OpenAI chat completion failed: {e}", "CHAT_COMPLETION_FAILED"
                )

    async def complete_vision(
        self, prompt: str, images: list[Union[str, bytes]], **kwargs
    ) -> LLMResponse:
        """Generate completion with vision capabilities using OpenAI.

        Args:
            prompt: Text prompt
            images: List of image URLs or binary data
            **kwargs: Additional parameters

        Returns:
            LLM response with image analysis
        """
        if not self.supports_capability(ModelCapability.VISION):
            return self._create_error_response(
                "Vision capabilities not supported by this model",
                "CAPABILITY_NOT_SUPPORTED",
            )

        start_time = time.time()

        try:
            # Prepare content with images
            content = [{"type": "text", "text": prompt}]

            # Add images to content
            for image in images[:10]:  # OpenAI supports up to 10 images
                if isinstance(image, str):
                    # URL
                    content.append(
                        {
                            "type": "image_url",
                            "image_url": {"url": image, "detail": "auto"},
                        }
                    )
                elif isinstance(image, bytes):
                    # Binary data - convert to base64
                    image_b64 = base64.b64encode(image).decode()
                    content.append(
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_b64}",
                                "detail": "auto",
                            },
                        }
                    )

            # Prepare generation parameters
            params = self._prepare_generation_params(**kwargs)

            # Create messages with vision content
            messages = [{"role": "user", "content": content}]

            response = await self._client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                max_tokens=params.get("max_tokens", self.config.max_tokens),
                temperature=params.get("temperature", self.config.temperature),
                stream=False,
            )

            response_time = time.time() - start_time

            # Extract content
            content = response.choices[0].message.content or ""

            return LLMResponse(
                content=content,
                provider=self.config.provider,
                model=self.config.model,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
                finish_reason=response.choices[0].finish_reason,
                response_time=response_time,
                raw_response=response,
            )

        except Exception as e:
            logger.error(f"OpenAI vision completion failed: {e}")
            return self._create_error_response(
                f"OpenAI vision completion failed: {e}", "VISION_COMPLETION_FAILED"
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
        """Get list of available OpenAI models.

        Returns:
            List of model names
        """
        return [
            "gpt-4-turbo-preview",
            "gpt-4-vision-preview",
            "gpt-4",
            "gpt-4-32k",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
        ]
