"""Interfaces for web_maestro to allow pluggable implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class LLMResponse:
    """Response from an LLM client."""

    content: str
    raw_response: Any | None = None
    error: str | None = None


class LLMClient(ABC):
    """Abstract interface for LLM clients."""

    @abstractmethod
    def create_completion(self, prompt: str, max_tokens: int = 100) -> LLMResponse:
        """Create a completion from a prompt."""
        pass

    def is_available(self) -> bool:
        """Check if the client is available."""
        return True


__all__ = ["LLMClient", "LLMResponse"]
