"""Configuration classes for web_maestro package.

This module provides dataclass-based configuration that complements the existing
dictionary-based FAST_CONFIG, offering type safety and better IDE support.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from ..models.types import (
    BrowserConfig,
    Milliseconds,
    NavigationOptions,
    Pixels,
    ResourceType,
)


@dataclass
class StabilityConfig:
    """Configuration for DOM stability detection."""

    timeout_ms: Milliseconds = 2000
    stability_threshold: int = 4
    check_interval: Milliseconds = 1000
    min_stability_time: Milliseconds = 1000

    @classmethod
    def from_profile(cls, profile: str = "DEFAULT") -> StabilityConfig:
        """Create config from predefined profiles in config.py."""
        from .base import DOM_STABILITY

        if profile not in DOM_STABILITY:
            raise ValueError(f"Unknown stability profile: {profile}")

        profile_dict = DOM_STABILITY[profile]
        return cls(**profile_dict)


@dataclass
class InteractionConfig:
    """Configuration for DOM interactions and element clicking."""

    # Tab interaction
    max_tabs: int = 10
    tab_timeout_ms: Milliseconds = 5000
    tab_selector: str | None = None

    # Element exploration
    explore_elements: int = 25
    expand_buttons: int = 12
    clickable_selector: str | None = None

    # Timing
    interaction_delay_ms: Milliseconds = 500
    click_timeout_ms: Milliseconds = 5000

    # Hover interaction
    max_hover_elements: int = 20
    hover_delay_ms: Milliseconds = 300


@dataclass
class ScrollConfig:
    """Configuration for page scrolling behavior."""

    enabled: bool = True
    max_scrolls: int = 15
    scroll_increment: Pixels = 500
    scroll_delay_ms: Milliseconds = 500
    wait_after_scroll_ms: Milliseconds = 1000

    # Smart scrolling
    detect_infinite_scroll: bool = True
    stop_at_repeated_content: bool = True


@dataclass
class ContentFilterConfig:
    """Configuration for content filtering and deduplication."""

    min_text_length: int = 10
    exclude_selectors: list[str] = field(
        default_factory=lambda: [
            "script",
            "style",
            "noscript",
            "iframe",
            "svg",
            "canvas",
        ]
    )

    # Text cleaning
    remove_empty_lines: bool = True
    normalize_whitespace: bool = True

    # Deduplication
    deduplicate_content: bool = True
    similarity_threshold: float = 0.95


@dataclass
class ScraperConfig:
    """Complete configuration for web scraping."""

    # Core settings
    url_timeout_ms: Milliseconds = 30000
    dom_timeout_ms: Milliseconds = 8000

    # Sub-configurations
    browser: BrowserConfig = field(default_factory=BrowserConfig)
    navigation: NavigationOptions = field(default_factory=NavigationOptions)
    stability: StabilityConfig = field(default_factory=StabilityConfig)
    interaction: InteractionConfig = field(default_factory=InteractionConfig)
    scroll: ScrollConfig = field(default_factory=ScrollConfig)
    content_filter: ContentFilterConfig = field(default_factory=ContentFilterConfig)

    # Resource blocking
    block_resources: bool = True
    blocked_resource_types: list[ResourceType] = field(
        default_factory=lambda: [
            ResourceType.IMAGE,
            ResourceType.FONT,
            ResourceType.STYLESHEET,
            ResourceType.MEDIA,
        ]
    )

    # Debug settings
    debug: bool = False
    screenshot_on_error: bool = True
    trace_enabled: bool = True
    verbose_logging: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary format compatible with existing code."""
        result = {}

        # Map to FAST_CONFIG keys
        result["max_tabs"] = self.interaction.max_tabs
        result["tab_timeout"] = self.interaction.tab_timeout_ms
        result["max_scrolls"] = self.scroll.max_scrolls
        result["stability_threshold"] = self.stability.stability_threshold
        result["explore_elements"] = self.interaction.explore_elements
        result["expand_buttons"] = self.interaction.expand_buttons
        result["dom_timeout_ms"] = self.dom_timeout_ms
        result["scroll"] = self.scroll.enabled

        # Add additional fields
        result["interaction_config"] = asdict(self.interaction)
        result["scroll_config"] = asdict(self.scroll)
        result["stability_config"] = asdict(self.stability)
        result["content_filter_config"] = asdict(self.content_filter)

        return result

    @classmethod
    def from_fast_config(
        cls, fast_config: dict[str, Any] | None = None
    ) -> ScraperConfig:
        """Create ScraperConfig from FAST_CONFIG dictionary."""
        if fast_config is None:
            from .base import FAST_CONFIG

            fast_config = FAST_CONFIG

        interaction = InteractionConfig(
            max_tabs=fast_config.get("max_tabs", 10),
            tab_timeout_ms=fast_config.get("tab_timeout", 5000),
            explore_elements=fast_config.get("explore_elements", 25),
            expand_buttons=fast_config.get("expand_buttons", 12),
        )

        scroll = ScrollConfig(
            enabled=fast_config.get("scroll", True),
            max_scrolls=fast_config.get("max_scrolls", 15),
        )

        stability = StabilityConfig(
            stability_threshold=fast_config.get("stability_threshold", 4),
        )

        return cls(
            dom_timeout_ms=fast_config.get("dom_timeout_ms", 8000),
            interaction=interaction,
            scroll=scroll,
            stability=stability,
        )

    def merge_with_dict(self, config_dict: dict[str, Any]) -> ScraperConfig:
        """Merge with a dictionary config, with dict values taking precedence."""
        # Create a copy
        import copy

        merged = copy.deepcopy(self)

        # Update with dictionary values
        if "max_tabs" in config_dict:
            merged.interaction.max_tabs = config_dict["max_tabs"]
        if "tab_timeout" in config_dict:
            merged.interaction.tab_timeout_ms = config_dict["tab_timeout"]
        if "max_scrolls" in config_dict:
            merged.scroll.max_scrolls = config_dict["max_scrolls"]
        if "scroll" in config_dict:
            merged.scroll.enabled = config_dict["scroll"]
        if "dom_timeout_ms" in config_dict:
            merged.dom_timeout_ms = config_dict["dom_timeout_ms"]
        if "stability_threshold" in config_dict:
            merged.stability.stability_threshold = config_dict["stability_threshold"]
        if "explore_elements" in config_dict:
            merged.interaction.explore_elements = config_dict["explore_elements"]
        if "expand_buttons" in config_dict:
            merged.interaction.expand_buttons = config_dict["expand_buttons"]

        return merged


@dataclass
class ValidationConfig(ScraperConfig):
    """Optimized configuration for quick validation runs."""

    def __post_init__(self):
        """Initialize validation-optimized settings after dataclass init."""
        # Override with validation-optimized settings
        self.dom_timeout_ms = 2000
        self.stability = StabilityConfig.from_profile("VALIDATION")
        self.interaction.max_tabs = 1
        self.interaction.explore_elements = 5
        self.interaction.expand_buttons = 3
        self.scroll.max_scrolls = 3
        self.browser.headless = True
        self.trace_enabled = False


@dataclass
class DomainOptimizedConfig(ScraperConfig):
    """Configuration optimized for specific domain extraction."""

    # Domain-specific settings
    domain_name: str = "generic"
    custom_tab_selector: str | None = None
    priority_keywords: list[str] | None = None
    element_classification_prompt: str | None = None

    def __post_init__(self):
        """Initialize domain-optimized settings after dataclass init."""
        # Use custom or generic selectors
        from .base import GENERIC_TAB_SELECTOR, UNIVERSAL_CLICKABLE_SELECTOR

        if self.custom_tab_selector:
            self.interaction.tab_selector = self.custom_tab_selector
        else:
            self.interaction.tab_selector = GENERIC_TAB_SELECTOR

        self.interaction.clickable_selector = UNIVERSAL_CLICKABLE_SELECTOR


@dataclass
class MenuExtractionConfig(DomainOptimizedConfig):
    """DEPRECATED: Use DomainOptimizedConfig with appropriate settings.

    Configuration optimized for restaurant menu extraction.
    Kept for backward compatibility.
    """

    def __post_init__(self):
        """Initialize menu extraction-optimized settings."""
        # Set domain-specific values
        self.domain_name = "restaurant_menu"
        self.priority_keywords = ["menu", "order", "delivery", "food"]
        self.element_classification_prompt = (
            "Does the following label refer to a food-related tab in a restaurant website?\n"
            "Label: '{label}'\n\n"
            "Respond only with 'Yes' or 'No'."
        )

        # Call parent post_init by calling the parent class method directly
        DomainOptimizedConfig.__post_init__(self)

        # Menu-specific optimizations
        self.interaction.max_tabs = 15  # More tabs for menu categories
        self.interaction.explore_elements = 30  # More exploration for menu items
        self.scroll.max_scrolls = 20  # Longer scrolling for full menus
        self.content_filter.min_text_length = 5  # Shorter for menu items
        self.content_filter.exclude_selectors.extend(
            [".social-media", ".footer", ".header", ".advertisement"]
        )


# Preset configurations
PRESETS = {
    "default": ScraperConfig(),
    "validation": ValidationConfig(),
    "menu": MenuExtractionConfig(),  # Deprecated - use DomainOptimizedConfig
    "fast": ScraperConfig(
        dom_timeout_ms=5000,
        interaction=InteractionConfig(max_tabs=5, explore_elements=10),
        scroll=ScrollConfig(max_scrolls=5),
    ),
    "thorough": ScraperConfig(
        dom_timeout_ms=15000,
        stability=StabilityConfig.from_profile("THOROUGH"),
        interaction=InteractionConfig(max_tabs=20, explore_elements=50),
        scroll=ScrollConfig(max_scrolls=30),
    ),
}
