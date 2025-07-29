"""Domain-specific configurations for content extraction.

This module provides the base structure for domain configurations.
Specific domain implementations should be created in the consuming application.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ExtractionMode(Enum):
    """Extraction modes."""

    FAST = "fast"
    THOROUGH = "thorough"
    BALANCED = "balanced"
    CUSTOM = "custom"


@dataclass
class DomainConfig:
    """Configuration for a specific content domain.

    This is a generic structure that can be used for any domain
    (e-commerce, news, documentation, restaurant menus, etc.)
    """

    # Domain identification
    domain_name: str
    description: str = ""

    # Target content configuration
    target_selectors: list[str] = field(default_factory=list)
    target_keywords: list[str] = field(default_factory=list)
    exclude_keywords: list[str] = field(default_factory=list)

    # Navigation configuration
    navigation_selectors: list[str] = field(default_factory=list)
    interaction_keywords: list[str] = field(default_factory=list)

    # Extraction configuration
    content_fields: list[str] = field(default_factory=list)
    required_fields: list[str] = field(default_factory=list)
    field_patterns: dict[str, str] = field(default_factory=dict)

    # Quality control
    min_items: int = 1
    max_items: int = 1000
    min_confidence: float = 0.5

    # AI scout
    ai_scout_config: dict[str, Any] = field(default_factory=dict)

    # Custom prompts for LLM navigation
    navigation_prompts: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "domain_name": self.domain_name,
            "description": self.description,
            "target_selectors": self.target_selectors,
            "target_keywords": self.target_keywords,
            "exclude_keywords": self.exclude_keywords,
            "navigation_selectors": self.navigation_selectors,
            "interaction_keywords": self.interaction_keywords,
            "content_fields": self.content_fields,
            "required_fields": self.required_fields,
            "field_patterns": self.field_patterns,
            "min_items": self.min_items,
            "max_items": self.max_items,
            "min_confidence": self.min_confidence,
            "ai_scout_config": self.ai_scout_config,
            "navigation_prompts": self.navigation_prompts,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DomainConfig":
        """Create from dictionary."""
        return cls(**data)


def create_generic_config(**kwargs) -> DomainConfig:
    """Create a generic domain configuration with custom settings."""
    defaults = {
        "domain_name": "generic",
        "description": "Generic content extraction",
        "target_selectors": [
            ".content",
            ".item",
            ".entry",
            ".card",
            "article",
            "section",
            "[data-item]",
        ],
        "navigation_selectors": [
            "[role='tab']",
            ".tab",
            ".nav-item",
            "[data-tab]",
            "nav a",
        ],
    }
    defaults.update(kwargs)
    return DomainConfig(**defaults)


# Factory function and aliases for backward compatibility
def domain_config_factory(domain_type: str = "generic", **kwargs) -> DomainConfig:
    """Factory function to create domain-specific configurations."""
    if domain_type == "restaurant":
        return create_generic_config(domain_name="restaurant", **kwargs)
    elif domain_type == "ecommerce":
        return create_generic_config(domain_name="ecommerce", **kwargs)
    elif domain_type == "news":
        return create_generic_config(domain_name="news", **kwargs)
    else:
        return create_generic_config(**kwargs)


# Convenience aliases
def RestaurantConfig(**kwargs):  # noqa: N802
    """Create a restaurant domain configuration."""
    return domain_config_factory("restaurant", **kwargs)


def EcommerceConfig(**kwargs):  # noqa: N802
    """Create an ecommerce domain configuration."""
    return domain_config_factory("ecommerce", **kwargs)


def NewsConfig(**kwargs):  # noqa: N802
    """Create a news domain configuration."""
    return domain_config_factory("news", **kwargs)


def GenericConfig(**kwargs):  # noqa: N802
    """Create a generic domain configuration."""
    return domain_config_factory("generic", **kwargs)
