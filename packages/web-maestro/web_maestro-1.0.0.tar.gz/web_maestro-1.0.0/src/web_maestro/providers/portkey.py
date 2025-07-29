"""Portkey provider implementation."""

import asyncio
import base64
from collections.abc import AsyncIterator
import json
import logging
import time
from typing import Any, Optional, Union

from portkey_ai import Portkey

from .base import BaseLLMProvider, LLMConfig, LLMResponse, ModelCapability

logger = logging.getLogger(__name__)


class PortkeyProvider(BaseLLMProvider):
    """Portkey provider for unified LLM API access."""

    def __init__(self, config: LLMConfig):
        """Initialize Portkey provider.

        Args:
            config: LLM configuration with Portkey-specific settings
        """
        # Set default capabilities for Portkey
        if not config.supported_capabilities:
            config.supported_capabilities = [
                ModelCapability.TEXT_COMPLETION,
                ModelCapability.CHAT_COMPLETION,
                ModelCapability.VISION,
                ModelCapability.FUNCTION_CALLING,
                ModelCapability.STREAMING,
                ModelCapability.JSON_MODE,
            ]

        super().__init__(config)

        # Initialize Portkey client
        self._client = self._create_client()

        logger.info(f"Initialized Portkey provider with model: {config.model}")

    def _create_client(self) -> Portkey:
        """Create Portkey client instance."""
        try:
            client_params = {
                "api_key": self.config.api_key,
            }

            # Add optional parameters
            if self.config.base_url:
                client_params["base_url"] = self.config.base_url

            # Portkey-specific parameters from extra_params
            if "virtual_key" in self.config.extra_params:
                client_params["virtual_key"] = self.config.extra_params["virtual_key"]

            return Portkey(**client_params)

        except Exception as e:
            logger.error(f"Failed to create Portkey client: {e}")
            raise ValueError(f"Invalid Portkey configuration: {e}") from e

    async def complete(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate text completion using Portkey.

        Args:
            prompt: Input prompt text
            **kwargs: Additional generation parameters

        Returns:
            LLM response with generated content
        """
        start_time = time.time()
        prompt_length = len(prompt)

        logger.info(
            f"🤖 Starting LLM completion - model: {self.config.model}, prompt_length: {prompt_length}"
        )
        logger.debug(
            f"📝 Prompt preview: {prompt[:200]}{'...' if len(prompt) > 200 else ''}"
        )

        # Prepare generation parameters
        params = self._prepare_generation_params(**kwargs)
        logger.debug(f"⚙️ Generation params: {params}")

        try:
            # Use asyncio.to_thread for sync Portkey client
            response = await asyncio.to_thread(
                self._client.chat.completions.create,
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
            content_length = len(content)

            # Extract usage information
            usage = response.usage if hasattr(response, "usage") else None

            logger.info(
                f"✅ LLM completion successful - response_time: {response_time:.2f}s, content_length: {content_length}"
            )
            if usage:
                logger.debug(
                    f"📊 Token usage - prompt: {usage.prompt_tokens}, completion: {usage.completion_tokens}, total: {usage.total_tokens}"
                )
            logger.debug(f"🏁 Finish reason: {response.choices[0].finish_reason}")
            logger.debug(
                f"📄 Response preview: {content[:200]}{'...' if len(content) > 200 else ''}"
            )

            return LLMResponse(
                content=content,
                provider=self.config.provider,
                model=self.config.model,
                prompt_tokens=usage.prompt_tokens if usage else None,
                completion_tokens=usage.completion_tokens if usage else None,
                total_tokens=usage.total_tokens if usage else None,
                finish_reason=response.choices[0].finish_reason,
                response_time=response_time,
                raw_response=response,
            )

        except Exception as e:
            logger.error(f"❌ Portkey completion failed: {type(e).__name__}: {e}")
            logger.debug(
                f"🔍 Error details for prompt length {prompt_length}:", exc_info=True
            )
            return self._create_error_response(
                f"Portkey completion failed: {e}", "COMPLETION_FAILED"
            )

    async def complete_chat(
        self, messages: list[dict[str, str]], **kwargs
    ) -> LLMResponse:
        """Generate chat completion using Portkey.

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
            # Use asyncio.to_thread for sync Portkey client
            response = await asyncio.to_thread(
                self._client.chat.completions.create,
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

            # Extract usage information
            usage = response.usage if hasattr(response, "usage") else None

            return LLMResponse(
                content=content,
                provider=self.config.provider,
                model=self.config.model,
                prompt_tokens=usage.prompt_tokens if usage else None,
                completion_tokens=usage.completion_tokens if usage else None,
                total_tokens=usage.total_tokens if usage else None,
                finish_reason=response.choices[0].finish_reason,
                response_time=response_time,
                raw_response=response,
            )

        except Exception as e:
            logger.error(f"Portkey chat completion failed: {e}")
            return self._create_error_response(
                f"Portkey chat completion failed: {e}", "CHAT_COMPLETION_FAILED"
            )

    async def complete_stream(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        """Generate streaming text completion using Portkey.

        Args:
            prompt: Input prompt text
            **kwargs: Additional generation parameters

        Yields:
            Chunks of generated text
        """
        # Prepare generation parameters
        params = self._prepare_generation_params(**kwargs)

        try:
            # Create streaming response in a thread
            def create_stream():
                return self._client.chat.completions.create(
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
                    stream=True,  # Enable streaming
                )

            # Get the stream object
            stream = await asyncio.to_thread(create_stream)

            # Stream the response chunks
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    await asyncio.sleep(0)  # Allow other tasks to run

        except Exception as e:
            logger.error(f"Portkey streaming completion failed: {e}")
            yield f"[Error: {e}]"

    async def complete_chat_stream(
        self, messages: list[dict[str, str]], **kwargs
    ) -> AsyncIterator[str]:
        """Generate streaming chat completion using Portkey.

        Args:
            messages: List of chat messages
            **kwargs: Additional generation parameters

        Yields:
            Chunks of generated text
        """
        # Prepare generation parameters
        params = self._prepare_generation_params(**kwargs)

        try:
            # Use asyncio.to_thread for sync Portkey client with streaming
            response = await asyncio.to_thread(
                self._client.chat.completions.create,
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
                stream=True,  # Enable streaming
            )

            # Stream the response chunks
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            logger.error(f"Portkey streaming chat completion failed: {e}")
            yield f"[Error: {e}]"

    async def complete_vision(
        self, prompt: str, images: list[Union[str, bytes]], **kwargs
    ) -> LLMResponse:
        """Generate completion with vision capabilities using Portkey.

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
            for image in images[:5]:  # Limit to 5 images
                if isinstance(image, str):
                    # URL
                    content.append({"type": "image_url", "image_url": {"url": image}})
                elif isinstance(image, bytes):
                    # Binary data - convert to base64
                    image_b64 = base64.b64encode(image).decode()
                    content.append(
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
                        }
                    )

            # Prepare generation parameters
            params = self._prepare_generation_params(**kwargs)

            # Create messages with vision content
            messages = [{"role": "user", "content": content}]

            # Use asyncio.to_thread for sync Portkey client
            response = await asyncio.to_thread(
                self._client.chat.completions.create,
                model=self.config.model,
                messages=messages,
                max_tokens=params.get("max_tokens", self.config.max_tokens),
                temperature=params.get("temperature", self.config.temperature),
                stream=False,
            )

            response_time = time.time() - start_time

            # Extract content
            content = response.choices[0].message.content or ""

            # Extract usage information
            usage = response.usage if hasattr(response, "usage") else None

            return LLMResponse(
                content=content,
                provider=self.config.provider,
                model=self.config.model,
                prompt_tokens=usage.prompt_tokens if usage else None,
                completion_tokens=usage.completion_tokens if usage else None,
                total_tokens=usage.total_tokens if usage else None,
                finish_reason=response.choices[0].finish_reason,
                response_time=response_time,
                raw_response=response,
            )

        except Exception as e:
            logger.error(f"Portkey vision completion failed: {e}")
            return self._create_error_response(
                f"Portkey vision completion failed: {e}", "VISION_COMPLETION_FAILED"
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
        """Get list of available models for Portkey.

        Returns:
            List of model names (depends on Portkey configuration)
        """
        # Portkey supports many models depending on configuration
        # Return common ones, but actual availability depends on virtual key setup
        return [
            "gpt-4-turbo-preview",
            "gpt-4",
            "gpt-3.5-turbo",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
        ]

    @classmethod
    def create_from_legacy_config(cls, config_path: str) -> "PortkeyProvider":
        """Create PortkeyProvider from legacy Maestro config file.

        Args:
            config_path: Path to legacy config.json file

        Returns:
            Configured PortkeyProvider instance
        """
        try:
            with open(config_path) as f:
                legacy_config = json.load(f)

            # Map legacy config to new format
            llm_config = LLMConfig(
                provider="portkey",
                model=legacy_config.get("model_id", "gpt-4"),
                api_key=legacy_config.get("api_key"),
                base_url=legacy_config.get("base_url"),
                extra_params={"virtual_key": legacy_config.get("virtual_key")},
            )

            return cls(llm_config)

        except Exception as e:
            logger.error(f"Failed to load legacy config from {config_path}: {e}")
            raise ValueError(f"Invalid legacy config file: {e}") from e

    def analyze_menu_image(
        self, image_data: bytes, extraction_prompt: Optional[str] = None
    ) -> dict[str, Any]:
        """Analyze menu image and extract structured data.

        This method maintains compatibility with the legacy PortkeyToolClient.

        Args:
            image_data: Binary image data
            extraction_prompt: Custom extraction prompt

        Returns:
            Dictionary with extracted menu data
        """
        if extraction_prompt is None:
            extraction_prompt = """
            Analyze this menu image and extract the following information in JSON format:
            {
                "restaurant_name": "Restaurant name if visible",
                "menu_sections": [
                    {
                        "section_name": "Section name (e.g., Appetizers, Main Courses)",
                        "items": [
                            {
                                "name": "Item name",
                                "price": "Price as string",
                                "description": "Item description if available"
                            }
                        ]
                    }
                ],
                "additional_info": "Any other relevant information"
            }
            """

        try:
            # Use synchronous call for backward compatibility
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            response = loop.run_until_complete(
                self.complete_vision(extraction_prompt, [image_data])
            )

            if response.success:
                # Try to parse JSON from response
                try:
                    import re

                    # Extract JSON from response content
                    json_match = re.search(r"\{.*\}", response.content, re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                    else:
                        return {"extracted_text": response.content}
                except json.JSONDecodeError:
                    return {"extracted_text": response.content}
            else:
                return {"error": response.error}

        except Exception as e:
            logger.error(f"Menu image analysis failed: {e}")
            return {"error": str(e)}

        finally:
            loop.close()
