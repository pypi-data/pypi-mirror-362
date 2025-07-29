"""Data types and structures for the web_maestro package."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import TypeAlias

# Type aliases for commonly used types
ElementSelector: TypeAlias = str
ElementText: TypeAlias = str
ElementAttributes: TypeAlias = dict[str, str]
Milliseconds: TypeAlias = int
Pixels: TypeAlias = int


class CaptureType(Enum):
    """Types of content capture."""

    TEXT = "text"
    JSON = "json"
    LINK = "link"
    IMAGE = "image"
    TABLE = "table"
    FORM = "form"
    TAB_CONTENT = "tab_content"
    MENU_CONTENT = "menu_content"
    EXPANDED_CONTENT = "expanded_content"
    HOVER_CONTENT = "hover_content"


class InteractionType(Enum):
    """Types of DOM interactions."""

    CLICK = "click"
    HOVER = "hover"
    SCROLL = "scroll"
    TYPE = "type"
    SELECT = "select"
    EXPAND = "expand"
    COLLAPSE = "collapse"


class ResourceType(Enum):
    """Types of web resources that can be blocked."""

    DOCUMENT = "document"
    STYLESHEET = "stylesheet"
    IMAGE = "image"
    MEDIA = "media"
    FONT = "font"
    SCRIPT = "script"
    TEXTTRACK = "texttrack"
    XHR = "xhr"
    FETCH = "fetch"
    EVENTSOURCE = "eventsource"
    WEBSOCKET = "websocket"
    MANIFEST = "manifest"
    OTHER = "other"


@dataclass
class CapturedBlock:
    """Class representing a block of captured content.

    Attributes:
        content: The content that was captured.
        source_id: The ID of the source from which the content was captured.
        capture_type: Optional type of the capture.
    """

    content: str
    source_id: str
    capture_type: str | None = None


@dataclass
class DOMElement:
    """Represents a DOM element with its properties."""

    selector: str
    text: str
    attributes: dict[str, str] = field(default_factory=dict)
    is_visible: bool = True
    bounding_box: dict[str, float] | None = None
    parent_selector: str | None = None
    children_count: int = 0


@dataclass
class InteractionResult:
    """Result of a DOM interaction."""

    success: bool
    interaction_type: InteractionType
    element: DOMElement | None = None
    error: str | None = None
    new_content: list[CapturedBlock] = field(default_factory=list)
    duration_ms: float = 0


@dataclass
class ScrollPosition:
    """Represents scroll position in a page."""

    x: int
    y: int
    width: int
    height: int
    scroll_width: int
    scroll_height: int

    @property
    def is_at_bottom(self) -> bool:
        """Check if scrolled to bottom."""
        return self.y + self.height >= self.scroll_height - 10

    @property
    def is_at_top(self) -> bool:
        """Check if scrolled to top."""
        return self.y <= 10


@dataclass
class PageMetrics:
    """Metrics about a web page."""

    url: str
    title: str
    load_time_ms: float
    dom_content_loaded_ms: float
    total_elements: int
    interactive_elements: int
    images_count: int
    scripts_count: int
    stylesheets_count: int
    viewport: dict[str, int]


@dataclass
class CaptureConfig:
    """Configuration for content capture."""

    # Timing
    timeout_ms: Milliseconds = 30000
    stability_timeout_ms: Milliseconds = 2000
    interaction_delay_ms: Milliseconds = 500

    # Scrolling
    scroll_enabled: bool = True
    max_scrolls: int = 15
    scroll_increment: Pixels = 500

    # Element interaction
    max_elements_to_click: int = 25
    max_hover_elements: int = 20
    click_timeout_ms: Milliseconds = 5000

    # Content filtering
    min_text_length: int = 10
    exclude_selectors: list[str] = field(
        default_factory=lambda: ["script", "style", "noscript", "iframe"]
    )

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

    # Debug
    debug: bool = False
    screenshot_on_error: bool = True
    trace_enabled: bool = True


@dataclass
class CapturePhase:
    """Represents a phase in the capture process."""

    name: str
    description: str
    max_duration_ms: Milliseconds
    required: bool = True
    depends_on: list[str] = field(default_factory=list)


@dataclass
class CaptureResult:
    """Complete result of a page capture."""

    url: str
    success: bool
    blocks: list[CapturedBlock]
    metrics: PageMetrics | None = None
    interactions: list[InteractionResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    duration_ms: float = 0
    phases_completed: list[str] = field(default_factory=list)


@dataclass
class ElementFilter:
    """Filter for selecting DOM elements."""

    include_selectors: list[str] = field(default_factory=list)
    exclude_selectors: list[str] = field(default_factory=list)
    text_patterns: list[str] = field(default_factory=list)
    attribute_filters: dict[str, str] = field(default_factory=dict)
    custom_filter: Callable[[DOMElement], bool] | None = None


@dataclass
class NavigationOptions:
    """Options for page navigation."""

    wait_until: str = "domcontentloaded"
    timeout_ms: Milliseconds = 30000
    referer: str | None = None
    extra_headers: dict[str, str] = field(default_factory=dict)


@dataclass
class BrowserConfig:
    """Configuration for browser setup."""

    headless: bool = True
    viewport: dict[str, int] = field(
        default_factory=lambda: {"width": 1920, "height": 3000}
    )
    user_agent: str | None = None
    locale: str = "en-US"
    timezone: str | None = None
    permissions: list[str] = field(default_factory=list)
    extra_args: list[str] = field(default_factory=list)
    ignore_https_errors: bool = True
    bypass_csp: bool = True
