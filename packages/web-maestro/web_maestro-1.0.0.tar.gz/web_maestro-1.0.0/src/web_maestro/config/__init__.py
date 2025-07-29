"""Configuration management for playwright utilities."""

from .base import FAST_CONFIG, STANDARD_CONFIG, THOROUGH_CONFIG


def get_preset_config(preset_name: str) -> dict:
    """Get a preset configuration by name.

    Args:
        preset_name: Name of the preset ('fast', 'standard', 'thorough')

    Returns:
        Configuration dictionary
    """
    presets = {
        "fast": FAST_CONFIG,
        "standard": STANDARD_CONFIG,
        "thorough": THOROUGH_CONFIG,
    }

    if preset_name.lower() not in presets:
        raise ValueError(
            f"Unknown preset: {preset_name}. Available: {list(presets.keys())}"
        )

    return presets[preset_name.lower()]


def list_presets() -> list[str]:
    """List available preset names.

    Returns:
        List of available preset names
    """
    return ["fast", "standard", "thorough"]


__all__ = [
    # Base configurations
    "FAST_CONFIG",
    "STANDARD_CONFIG",
    "THOROUGH_CONFIG",
    # Presets
    "get_preset_config",
    "list_presets",
]
