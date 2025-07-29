"""DOM capture functionality for web_maestro."""

from ..dom_capture.ai_scout import classify_element
from ..dom_capture.capture import (
    capture_dom_stages_universal,
    capture_from_data_attributes,
    capture_from_visible_dom_and_scripts,
    capture_scripts_json_blobs,
    capture_structured_blobs,
    capture_tab_linked_sections,
    capture_visible_links,
    deduplicate_and_capture_blocks,
)
from ..dom_capture.click_strategies import (
    ClickStrategyExecutor,
    safe_click,
    safe_click_if_menu_relevant,  # Deprecated
    safe_click_if_relevant,
    universal_click_element,
)
from ..dom_capture.expansion import expand_hidden_menus
from ..dom_capture.exploration import explore_hover_and_click
from ..dom_capture.scroll import scroll_until_stable
from ..dom_capture.stability import wait_until_dom_stable
from ..dom_capture.tab_expansion import expand_tabs_and_capture
from ..dom_capture.universal_capture import universal_click_everything_and_capture

__all__ = [
    "ClickStrategyExecutor",
    # Main capture functions
    "capture_dom_stages_universal",
    "capture_from_data_attributes",
    "capture_from_visible_dom_and_scripts",
    "capture_scripts_json_blobs",
    "capture_structured_blobs",
    "capture_tab_linked_sections",
    "capture_visible_links",
    # AI Scout
    "classify_element",
    "deduplicate_and_capture_blocks",
    "expand_hidden_menus",
    "expand_tabs_and_capture",
    "explore_hover_and_click",
    # Interactions
    "safe_click",
    "safe_click_if_menu_relevant",  # Deprecated
    "safe_click_if_relevant",
    # DOM utilities
    "scroll_until_stable",
    "universal_click_element",
    "universal_click_everything_and_capture",
    "wait_until_dom_stable",
]
