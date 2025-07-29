"""Ollama provider implementation for local LLM models."""

import logging
import time

try:
    import httpx

    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False

    # Create dummy module for when httpx is not available
    class HTTPX:
        class AsyncClient:
            pass

        class HTTPStatusError(Exception):
            pass

    httpx = HTTPX()


from .base import BaseLLMProvider, LLMConfig, LLMResponse, ModelCapability

logger = logging.getLogger(__name__)


class OllamaProvider(BaseLLMProvider):
    """Ollama provider for local LLM models."""

    def __init__(self, config: LLMConfig):
        """Initialize Ollama provider.

        Args:
            config: LLM configuration with Ollama-specific settings
        """
        if not HTTPX_AVAILABLE:
            raise ImportError(
                "httpx package not installed. Install with: pip install httpx"
            )

        # Set default base URL for Ollama
        if not config.base_url:
            config.base_url = "http://localhost:11434"

        # Set default capabilities for Ollama models
        if not config.supported_capabilities:
            config.supported_capabilities = [
                ModelCapability.TEXT_COMPLETION,
                ModelCapability.CHAT_COMPLETION,
            ]

        super().__init__(config)

        # Initialize HTTP client
        self._client = httpx.AsyncClient(
            base_url=self.config.base_url, timeout=self.config.timeout
        )

        logger.info(f"Initialized Ollama provider with model: {config.model}")

    async def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate text completion using Ollama.

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
            payload = {
                "model": self.config.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": params.get("temperature", self.config.temperature),
                    "top_p": params.get("top_p", self.config.top_p),
                    "num_predict": params.get("max_tokens", self.config.max_tokens),
                },
            }

            response = await self._client.post("/api/generate", json=payload)
            response.raise_for_status()

            response_time = time.time() - start_time

            result = response.json()
            content = result.get("response", "")

            return LLMResponse(
                content=content,
                provider=self.config.provider,
                model=self.config.model,
                response_time=response_time,
                raw_response=result,
            )

        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama HTTP error: {e}")
            return self._create_error_response(f"Ollama HTTP error: {e}", "HTTP_ERROR")
        except Exception as e:
            logger.error(f"Ollama completion failed: {e}")
            return self._create_error_response(
                f"Ollama completion failed: {e}", "COMPLETION_FAILED"
            )

    async def complete_chat(
        self, messages: list[dict[str, str]], **kwargs
    ) -> LLMResponse:
        """Generate chat completion using Ollama.

        Args:
            messages: List of chat messages
            **kwargs: Additional generation parameters

        Returns:
            LLM response with generated content
        """
        start_time = time.time()

        # Prepare generation parameters
        params = self._prepare_generation_params(**kwargs)

        try:
            payload = {
                "model": self.config.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": params.get("temperature", self.config.temperature),
                    "top_p": params.get("top_p", self.config.top_p),
                    "num_predict": params.get("max_tokens", self.config.max_tokens),
                },
            }

            response = await self._client.post("/api/chat", json=payload)
            response.raise_for_status()

            response_time = time.time() - start_time

            result = response.json()
            content = result.get("message", {}).get("content", "")

            return LLMResponse(
                content=content,
                provider=self.config.provider,
                model=self.config.model,
                response_time=response_time,
                raw_response=result,
            )

        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama HTTP error: {e}")
            return self._create_error_response(f"Ollama HTTP error: {e}", "HTTP_ERROR")
        except Exception as e:
            logger.error(f"Ollama chat completion failed: {e}")
            return self._create_error_response(
                f"Ollama chat completion failed: {e}", "CHAT_COMPLETION_FAILED"
            )

    async def get_models(self) -> list[str]:
        """Get list of available models from Ollama instance.

        Returns:
            List of model names
        """
        try:
            response = await self._client.get("/api/tags")
            response.raise_for_status()

            result = response.json()
            models = [model["name"] for model in result.get("models", [])]
            return models

        except Exception as e:
            logger.error(f"Failed to get Ollama models: {e}")
            return []

    def supports_capability(self, capability: ModelCapability) -> bool:
        """Check if the provider supports a specific capability.

        Args:
            capability: Capability to check

        Returns:
            True if supported, False otherwise
        """
        return capability in self.config.supported_capabilities

    def get_available_models(self) -> list[str]:
        """Get list of common Ollama models.

        Returns:
            List of model names
        """
        # Common Ollama models - actual availability depends on what's pulled
        return [
            "llama2",
            "llama2:13b",
            "llama2:70b",
            "mistral",
            "mixtral",
            "codellama",
            "phi",
            "gemma",
        ]

    async def pull_model(self, model_name: str) -> bool:
        """Pull a model to the Ollama instance.

        Args:
            model_name: Name of the model to pull

        Returns:
            True if successful, False otherwise
        """
        try:
            payload = {"name": model_name}
            response = await self._client.post("/api/pull", json=payload)
            response.raise_for_status()

            logger.info(f"Successfully pulled model: {model_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to pull model {model_name}: {e}")
            return False

    async def validate_connection(self) -> bool:
        """Validate that Ollama is running and accessible.

        Returns:
            True if connection is valid, False otherwise
        """
        try:
            response = await self._client.get("/api/tags")
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Ollama connection validation failed: {e}")
            return False

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self._client.aclose()
