"""Domain-specific configurations and logic."""

from .domain_config import (
    DomainConfig,
    EcommerceConfig,
    ExtractionMode,
    GenericConfig,
    NewsConfig,
    RestaurantConfig,
    create_generic_config,
    domain_config_factory,
)

__all__ = [
    "DomainConfig",
    "ExtractionMode",
    "create_generic_config",
    "domain_config_factory",
    "EcommerceConfig",
    "GenericConfig",
    "NewsConfig",
    "RestaurantConfig",
]
