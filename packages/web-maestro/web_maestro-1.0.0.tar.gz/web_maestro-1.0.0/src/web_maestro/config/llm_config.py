"""LLM configuration for web_maestro."""

from __future__ import annotations

import logging

from ..interfaces import LLMClient, LLMResponse

logger = logging.getLogger(__name__)

# Global LLM client instance
_llm_client: LLMClient | None = None


def set_llm_client(client: LLMClient | None):
    """Set the global LLM client for web_maestro.

    Args:
            client: The LLM client instance to set.
    """
    global _llm_client
    _llm_client = client
    if client:
        logger.info("LLM client configured for web_maestro")
    else:
        logger.info("LLM features disabled in web_maestro")


def get_llm_client() -> LLMClient | None:
    """Get the configured LLM client.

    Returns:
        The configured LLM client or None if not set
    """
    return _llm_client


def create_portkey_adapter():
    """Create an adapter for the Portkey client if available.

    This is an optional integration that will only work if maestro
    is available in the environment.

    Returns:
        PortkeyAdapter instance or None if maestro is not available
    """
    try:
        from maestro.src.clients.portkey_tool_client import PortkeyToolClient

        class PortkeyAdapter(LLMClient):
            """Adapter to use Portkey client with web_maestro interface."""

            def __init__(self):
                self.client = PortkeyToolClient()

            def create_completion(
                self, prompt: str, max_tokens: int = 100
            ) -> LLMResponse:
                try:
                    result = self.client.create_completion(
                        prompt, max_tokens=max_tokens
                    )

                    if isinstance(result, dict):
                        return LLMResponse(
                            content="", raw_response=result, error=str(result)
                        )

                    content = result.choices[0].message.content.strip()
                    return LLMResponse(content=content, raw_response=result)

                except Exception as e:
                    logger.error(f"Portkey completion failed: {e}")
                    return LLMResponse(content="", error=str(e))

            def is_available(self) -> bool:
                return True

        return PortkeyAdapter()

    except ImportError:
        logger.debug("Maestro Portkey client not available")
        return None
