"""Centralized Configuration for Menu Extraction and Playwright-Based Web Interaction.

This module defines tunable parameters and default selectors used across the LLM-powered
menu extraction pipeline and dynamic browser automation. It includes:

1. ExtractionConfig:
    A dataclass representing crawl-time configuration for structured menu extraction.
    Used by the `extract_async()` pipeline to control depth, link filtering, timeouts,
    and LLM chunking behavior.

2. FAST_CONFIG:
    Default settings for dynamic page interaction using Playwright — governs scrolling,
    DOM stabilization, click exploration, and tab interaction behavior.

3. DOM_STABILITY:
    Profiles for determining when the DOM is "stable" enough to extract content.
    These profiles control timing thresholds and detection intervals for reactive pages.

4. UNIVERSAL_CLICKABLE_SELECTOR:
    A comprehensive CSS selector that targets most interactive page elements
    (buttons, nav items, tabs, expandable menus, filters, etc.) for exploration and expansion.

5. TAB_SELECTOR:
    A focused selector used to identify tab-style category toggles — typically found in
    menu carousels, segmented panels, or restaurant menu UIs.

"""

FAST_CONFIG = {
    "max_tabs": 10,  # Maximum tab-like elements to click during tab exploration
    "tab_timeout": 5000,  # Timeout (in ms) per tab click operation
    "max_scrolls": 15,  # Maximum number of downward scroll attempts
    "stability_threshold": 4,  # Number of stable DOM checks required for confirmation
    "explore_elements": 25,  # Max number of exploratory elements to interact with
    "expand_buttons": 12,  # Max number of expandable triggers (e.g., hamburgers, drawers)
    "dom_timeout_ms": 8000,  # Timeout for full DOM load during navigation
    "scroll": True,  # Whether to perform scrolling during interaction
}

STANDARD_CONFIG = {
    "max_tabs": 15,  # More thorough tab exploration
    "tab_timeout": 10000,  # Longer timeout per tab
    "max_scrolls": 25,  # More scrolling attempts
    "stability_threshold": 6,  # More stable DOM checks
    "explore_elements": 40,  # More exploratory elements
    "expand_buttons": 20,  # More expandable triggers
    "dom_timeout_ms": 15000,  # Longer DOM load timeout
    "scroll": True,
}

THOROUGH_CONFIG = {
    "max_tabs": 25,  # Maximum tab exploration
    "tab_timeout": 15000,  # Longest timeout per tab
    "max_scrolls": 50,  # Maximum scrolling attempts
    "stability_threshold": 8,  # Most stable DOM checks
    "explore_elements": 75,  # Maximum exploratory elements
    "expand_buttons": 30,  # Maximum expandable triggers
    "dom_timeout_ms": 30000,  # Longest DOM load timeout
    "scroll": True,
}

DOM_STABILITY = {
    "DEFAULT": {
        "timeout_ms": 2000,  # Total time to wait for DOM stabilization
        "stability_threshold": 4,  # Required stable cycles before accepting DOM as stable
        "check_interval": 1000,  # Time between DOM state comparisons (in ms)
        "min_stability_time": 1000,  # Minimum time the DOM must remain unchanged
    },
    "QUICK": {
        "timeout_ms": 6000,
        "stability_threshold": 4,
        "check_interval": 1000,
        "min_stability_time": 1000,
    },
    "THOROUGH": {
        "timeout_ms": 3000,
        "stability_threshold": 2,
        "check_interval": 200,
        "min_stability_time": 200,
    },
    "VALIDATION": {  # Ultra-fast for validation only
        "timeout_ms": 1000,  # Only wait 1 second max
        "stability_threshold": 1,  # Accept after 1 stable check
        "check_interval": 500,  # Check every 500ms
        "min_stability_time": 500,  # Only 500ms of stability needed
    },
}

UNIVERSAL_CLICKABLE_SELECTOR = (
    "button, a, [role='button'], [role='tab'], [role='menuitem'], "
    "[data-post-type], [data-taxonomy], [data-taxonomy-terms], [data-category], "
    "[data-filter], [data-sort], [data-orderby], [data-menu], "
    "[onclick], [data-toggle], [data-tab], [data-target], "
    "li, li > *, ul > li, ol > li, "
    "span[class*='tab'], div[class*='tab'], div[class*='button'], "
    "span[class*='button'], div[class*='menu'], span[class*='menu'], "
    "nav *, header *, .nav *, .menu *, .tab *, .category *, "
    ".filter *, .sort *, .toggle *, "
    "[class*='click'], [class*='select'], [id*='tab'], [id*='menu'], "
    "[id*='button'], [class*='item'], "
    "*[class*='link'], *[class*='nav'], *[href], "
    "*[tabindex], *[role], [aria-expanded], [aria-controls], "
    # Additional modern patterns (just append these)
    "[data-action], [data-click], [role='option'], [role='link'], "
    "*[class*='btn'], *[class*='card'], input[type='button'], "
    "select, *[ng-click]"
)

# Alternative: Keep yours exactly, add these as supplementary
ADDITIONAL_CLICKABLE_PATTERNS = (
    "[data-action], [data-click], [role='option'], [role='link'], "
    "*[class*='btn'], *[class*='card'], input[type='button'], "
    "select, *[ng-click]"
)


# Or create a more focused version for better performance
FOCUSED_CLICKABLE_SELECTOR = (
    "button, a[href], [role='button'], [role='tab'], [role='menuitem'], "
    "[data-menu], [data-category], [data-filter], [data-toggle], "
    "[onclick], [data-tab], [data-target], [data-action], "
    "li[class*='menu'], li[class*='nav'], li[class*='tab'], "
    "*[class*='btn'], *[class*='button'], *[class*='menu'], "
    "*[class*='tab'], *[class*='nav'], nav *, header *, "
    "[tabindex]:not([tabindex='-1']), [aria-expanded]"
)

# Enhanced version of your selector
TAB_SELECTOR = (
    # ARIA and semantic tabs
    "[role='tab'], [role='tablist'] *, "
    "[data-tab], [data-tab-id], [data-tabname], [data-tab-target], "
    "[aria-controls], [aria-selected], [aria-expanded], "
    # Class-based tab patterns (your existing ones improved)
    ".tab, .tabs *, .tab-button, .tabs button, .tablinks, "
    ".menu-tabs button, .tab-menu *, .tab-item, .tab-control, "
    ".tab-toggle, .tab-selector, .nav-tabs li, .nav-tabs a, "
    # Additional common tab patterns
    ".tab-nav *, .tabbed *, .tab-container *, .tab-wrapper *, "
    ".tab-header *, .tab-title, .tab-label, .switcher *, "
    "*[class*='tab-'], *[class*='-tab'], *[id*='tab'], "
    # Modern framework patterns
    "*[data-toggle='tab'], *[data-bs-toggle='tab'], "
    # List items that are likely tabs (more specific than "ul li")
    "ul[class*='tab'] li, ul[class*='nav'] li, ol[class*='tab'] li, "
    "li[class*='tab'], li[data-tab], li[role='tab']"
)

# More focused version for better performance
FOCUSED_TAB_SELECTOR = (
    "[role='tab'], [data-tab], [data-tab-id], [aria-controls], "
    ".tab, .tab-button, .tablinks, .tab-item, .nav-tabs a, "
    "*[class*='tab-'], *[data-toggle='tab'], "
    "li[class*='tab'], ul[class*='tab'] li"
)

# Generic tab selector for common tab patterns
GENERIC_TAB_SELECTOR = (
    "[role='tab'], [data-tab], [aria-selected], [data-toggle='tab'], "
    ".tab, .nav-tab, .tab-item, .tab-link, "
    "[class*='tab']:not(table), [id*='tab']:not(table), "
    "ul.tabs > li, .tab-list > *, .tab-panel-selector, "
    "[role='tablist'] > *, nav[role='tablist'] > *"
)

# Deprecated: Use DomainConfig.navigation_selectors instead
MENU_TAB_SELECTOR = GENERIC_TAB_SELECTOR


def create_default_config(profile: str = "standard") -> dict:
    """Create a default configuration for web_maestro.

    Args:
        profile: Configuration profile ('fast', 'standard', 'thorough')

    Returns:
        Configuration dictionary
    """
    import copy

    if profile.lower() == "fast":
        return copy.deepcopy(FAST_CONFIG)
    elif profile.lower() == "thorough":
        return copy.deepcopy(THOROUGH_CONFIG)
    else:
        return copy.deepcopy(STANDARD_CONFIG)
