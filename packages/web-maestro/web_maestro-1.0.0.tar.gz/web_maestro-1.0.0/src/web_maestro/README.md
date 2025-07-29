# Web Maestro

AI-powered web automation and content extraction engine with intelligent navigation, progressive content discovery, and production-ready reliability.

## Overview

Web Maestro is a sophisticated web automation framework that combines traditional browser automation with AI-powered decision making. It provides intelligent navigation, comprehensive content extraction, and robust handling of dynamic web applications.

### Key Features

- **AI-Powered Navigation**: LLM-guided decision making for intelligent interaction
- **Universal Content Extraction**: Comprehensive DOM capture with progressive discovery
- **Production-Ready**: Robust error handling, resource management, and monitoring
- **Configurable Profiles**: Multiple extraction strategies for different use cases
- **Domain-Specific Optimization**: Specialized configurations for different content types

## Architecture

```
web_maestro/
├── agents/              # AI scout system
│   └── scout_bridge.py # AI-powered navigation decisions
├── browser.py          # Core browser management
├── capture/            # Content capture coordination
├── config/             # Configuration system
│   ├── base.py        # Core configuration profiles
│   ├── config_classes.py # Configuration data structures
│   └── llm_config.py  # LLM integration configuration
├── context.py          # Session context management
├── core/               # Core browser functionality
│   ├── browser_setup.py # Browser initialization
│   ├── context.py     # Context management
│   └── exceptions.py  # Custom exceptions
├── dom_capture/        # Advanced DOM interaction
│   ├── ai_scout.py    # AI-powered element classification
│   ├── capture.py     # Main capture orchestration
│   ├── click_strategies.py # Click interaction strategies
│   ├── expansion.py   # Content expansion strategies
│   ├── exploration.py # Hover-based discovery
│   ├── scroll.py      # Scrolling and stability
│   ├── stability.py   # DOM stability detection
│   ├── tab_expansion.py # Tab-based interface handling
│   └── universal_capture.py # Universal content extraction
├── domains/            # Domain-specific configurations
│   └── domain_config.py # Domain configuration factory
├── fetch.py           # Main entry point for content extraction
├── interfaces/        # Abstract interfaces
│   └── base.py       # Base interfaces for extensibility
├── models/            # Data models and types
│   ├── base.py       # Base model classes
│   ├── content.py    # Content representation models
│   └── types.py      # Type definitions
└── utils/             # Utilities and helpers
    ├── logging.py    # Logging configuration
    └── trace_utils.py # Distributed tracing support
```

## Core Components

### Browser Management

#### `browser.py` - Core Browser Management

Central browser session management with Playwright integration:

```python
from maestro.src.web_maestro.browser import create_browser_session

async with create_browser_session() as session:
    page = session.page
    result = await page.goto("https://example.com")
```

**Features:**
- Automatic browser lifecycle management
- Context isolation for parallel sessions
- Resource cleanup and error recovery
- Tracing support for debugging

#### `core/browser_setup.py` - Browser Initialization

Production-optimized browser configuration:

- **Chromium Setup**: Headless mode with extensive Chrome flags
- **Resource Blocking**: Images, fonts, analytics disabled for speed
- **Security Bypass**: CSP and web security disabled for scraping access
- **Navigation Protection**: JavaScript injection prevents unwanted redirects

### Content Extraction

#### `fetch.py` - Main Entry Point

Primary interface for web content extraction:

```python
from maestro.src.web_maestro.fetch import fetch_with_ai_scout

# Basic extraction
result = await fetch_with_ai_scout(
    url="https://example.com",
    extraction_goal="Extract menu information"
)

# With custom configuration
result = await fetch_with_ai_scout(
    url="https://example.com",
    extraction_goal="Extract product catalog",
    config=THOROUGH_CONFIG,
    domain_config=ecommerce_domain
)
```

#### `dom_capture/capture.py` - Capture Orchestration

Multi-phase content extraction process:

1. **Tab Expansion**: Discover and activate tab-based content
2. **Menu Expansion**: Open hidden navigation and dropdown menus
3. **Universal Clicking**: Systematic interaction with relevant elements
4. **Hover Exploration**: Discover hover-activated content
5. **Content Extraction**: Structured data extraction from all states

### AI-Powered Navigation

#### `agents/scout_bridge.py` - AI Scout System

Intelligent navigation decisions powered by large language models:

```python
from maestro.src.web_maestro.agents.scout_bridge import LLMScoutBridge

# Initialize AI scout
scout = LLMScoutBridge(client=your_llm_client)

# Get navigation decision
decision = await scout.should_interact_with_element(
    element=dom_element,
    context=navigation_context,
    extraction_goal="Find menu information"
)
```

**Capabilities:**
- **Element Classification**: AI-based relevance filtering
- **Context-Aware Decisions**: Uses page context and extraction goals
- **Smart Navigation**: Decides which elements to click, scroll, or ignore
- **Fallback Strategies**: Rule-based alternatives when LLM unavailable

#### `dom_capture/ai_scout.py` - Element Classification

Advanced element analysis with AI assistance:

- **Relevance Detection**: Identifies elements relevant to extraction goals
- **Content Prediction**: Predicts what content interactions will reveal
- **Risk Assessment**: Evaluates potential negative impacts of interactions
- **Priority Scoring**: Ranks elements by interaction value

### Universal Content Extraction

#### `dom_capture/universal_capture.py` - Comprehensive Extraction

Systematic approach to discovering all content on a page:

```python
from maestro.src.web_maestro.dom_capture.universal_capture import capture_all_content

result = await capture_all_content(
    page=playwright_page,
    extraction_goal="Extract all menu items",
    config=STANDARD_CONFIG
)
```

**Features:**
- **Element Detection**: Sophisticated CSS selectors for interactive elements
- **Visual Ordering**: Processes elements in natural reading order
- **Deduplication**: Hash-based duplicate detection across DOM states
- **Progressive Expansion**: Systematic expansion of collapsible content

#### Content Discovery Strategies

**Tab Expansion** (`dom_capture/tab_expansion.py`):
- Detects tab-based interfaces
- Activates all tabs to reveal hidden content
- Handles complex tab hierarchies

**Menu Expansion** (`dom_capture/expansion.py`):
- Opens hamburger menus and navigation
- Expands dropdown menus and mega-menus
- Reveals accordion and collapsible content

**Click Strategies** (`dom_capture/click_strategies.py`):
- Multiple click approaches with fallbacks
- JavaScript click alternatives
- Coordinate-based clicking for difficult elements

**Hover Exploration** (`dom_capture/exploration.py`):
- Discovers hover-activated content
- Handles tooltip and popup content
- Progressive hover pattern exploration

### Stability and Reliability

#### `dom_capture/stability.py` - DOM Stability Detection

Intelligent waiting for dynamic content:

```python
from maestro.src.web_maestro.dom_capture.stability import wait_until_dom_stable

# Wait for content to stabilize
await wait_until_dom_stable(
    page=playwright_page,
    profile="DEFAULT",  # DEFAULT, QUICK, THOROUGH, VALIDATION
    timeout=10
)
```

**Stability Profiles:**
- **QUICK**: Fast detection for simple pages (1-3 seconds)
- **DEFAULT**: Balanced approach for most content (3-5 seconds)
- **THOROUGH**: Comprehensive detection for complex sites (5-10 seconds)
- **VALIDATION**: Optimized for menu validation tasks

#### `dom_capture/scroll.py` - Scrolling and Loading

Progressive content loading through scrolling:

- **Incremental Scrolling**: Scroll in steps to trigger lazy loading
- **Stability Monitoring**: Wait for content to load after each scroll
- **Infinite Scroll Handling**: Detect and handle infinite scroll patterns
- **Performance Optimization**: Avoid unnecessary scrolling

### Configuration System

#### `config/base.py` - Configuration Profiles

Pre-defined extraction profiles for different use cases:

```python
# Fast extraction - minimal interactions
FAST_CONFIG = CaptureConfig(
    max_interactions=10,
    stability_profile="QUICK",
    enable_hover_exploration=False,
    timeout_seconds=60
)

# Standard extraction - balanced approach
STANDARD_CONFIG = CaptureConfig(
    max_interactions=50,
    stability_profile="DEFAULT",
    enable_hover_exploration=True,
    timeout_seconds=180
)

# Thorough extraction - maximum coverage
THOROUGH_CONFIG = CaptureConfig(
    max_interactions=200,
    stability_profile="THOROUGH",
    enable_hover_exploration=True,
    timeout_seconds=300
)
```

#### `config/config_classes.py` - Configuration Data Models

Structured configuration with validation:

```python
@dataclass
class CaptureConfig:
    max_interactions: int = 50
    stability_profile: str = "DEFAULT"
    enable_ai_scout: bool = True
    enable_hover_exploration: bool = True
    timeout_seconds: int = 180
    max_scroll_attempts: int = 3
    wait_for_load: bool = True
```

#### `domains/domain_config.py` - Domain-Specific Configuration

Specialized configurations for different content types:

```python
# Restaurant domain configuration
restaurant_domain = DomainConfig(
    domain_name="restaurant",
    target_keywords=["menu", "food", "drink", "price"],
    navigation_patterns=["menu", "order", "food"],
    quality_threshold=0.7,
    ai_scout_prompt="restaurant_menu_extraction"
)

# E-commerce domain configuration
ecommerce_domain = DomainConfig(
    domain_name="ecommerce",
    target_keywords=["product", "price", "cart", "buy"],
    navigation_patterns=["shop", "products", "catalog"],
    quality_threshold=0.8,
    ai_scout_prompt="product_catalog_extraction"
)
```

### Data Models

#### `models/content.py` - Content Representation

Structured representation of extracted content:

```python
@dataclass
class CapturedBlock:
    content: str
    element_type: str
    source_info: dict
    confidence: float
    extraction_metadata: dict

@dataclass
class CaptureResult:
    blocks: List[CapturedBlock]
    metadata: dict
    extraction_time: float
    success: bool
    errors: List[str]
```

#### `models/types.py` - Type Definitions

Comprehensive type system for strong typing:

```python
# Navigation decisions
class NavigationDecision(Enum):
    CLICK = "click"
    HOVER = "hover"
    SCROLL = "scroll"
    SKIP = "skip"

# Interaction results
@dataclass
class InteractionResult:
    success: bool
    new_content_detected: bool
    error_message: Optional[str]
    metadata: dict
```

## Usage Examples

### Basic Content Extraction

```python
from maestro.src.web_maestro.fetch import fetch_with_ai_scout

# Simple extraction
result = await fetch_with_ai_scout(
    url="https://restaurant.com",
    extraction_goal="Extract menu items with prices"
)

# Access extracted content
for block in result.blocks:
    print(f"Content: {block.content}")
    print(f"Type: {block.element_type}")
    print(f"Confidence: {block.confidence}")
```

### Advanced Configuration

```python
from maestro.src.web_maestro.config.base import THOROUGH_CONFIG
from maestro.src.web_maestro.domains.domain_config import create_domain_config

# Create custom domain configuration
custom_domain = create_domain_config(
    domain_type="restaurant",
    custom_keywords=["special", "daily", "seasonal"],
    quality_threshold=0.9
)

# Extract with custom configuration
result = await fetch_with_ai_scout(
    url="https://fine-dining.com",
    extraction_goal="Extract seasonal menu items",
    config=THOROUGH_CONFIG,
    domain_config=custom_domain,
    timeout=300
)
```

### AI Scout Integration

```python
from maestro.src.web_maestro.agents.scout_bridge import LLMScoutBridge
from maestro.src.clients.portkey_tool_client import PortkeyToolClient

# Initialize with custom LLM client
client = PortkeyToolClient()
scout = LLMScoutBridge(client=client)

# Custom navigation context
context = NavigationContext(
    extraction_goal="Find wine list",
    current_page_url="https://restaurant.com/beverages",
    previous_actions=["clicked_menu_link"],
    discovered_content=["appetizers", "mains"]
)

# Get AI decision
decision = await scout.should_interact_with_element(
    element=wine_menu_element,
    context=context
)
```

### Session Management

```python
from maestro.src.web_maestro.context import SessionContext
from maestro.src.web_maestro.browser import create_browser_session

# Managed session with cleanup
async with SessionContext() as session_ctx:
    async with create_browser_session() as browser_session:
        page = browser_session.page

        # Perform extraction
        result = await fetch_with_ai_scout(
            url="https://example.com",
            extraction_goal="Extract content",
            session_context=session_ctx
        )

        # Session automatically cleaned up
```

## Performance Optimization

### Concurrency Management

```python
# Configure concurrency limits
PRODUCTION_CONFIG = CaptureConfig(
    max_concurrent_interactions=3,
    interaction_delay_ms=100,
    stability_timeout=5,
    enable_resource_monitoring=True
)
```

### Resource Optimization

```python
# Browser resource configuration
BROWSER_CONFIG = BrowserConfig(
    viewport_width=1920,
    viewport_height=1080,
    user_agent="custom-agent",
    enable_javascript=True,
    block_images=True,  # Faster loading
    block_fonts=True,   # Reduce bandwidth
    block_media=True    # Skip video/audio
)
```

### Caching and Persistence

```python
# Enable result caching
result = await fetch_with_ai_scout(
    url="https://example.com",
    extraction_goal="Extract menu",
    enable_caching=True,
    cache_ttl=3600  # 1 hour
)
```

## Error Handling and Monitoring

### Exception Handling

```python
from maestro.src.web_maestro.core.exceptions import (
    BrowserTimeoutError,
    ContentExtractionError,
    NavigationError
)

try:
    result = await fetch_with_ai_scout(url, goal)
except BrowserTimeoutError:
    # Handle timeout gracefully
    logger.warning("Extraction timed out, using partial results")
except ContentExtractionError as e:
    # Handle extraction failures
    logger.error(f"Extraction failed: {e}")
except NavigationError:
    # Handle navigation issues
    logger.error("Could not navigate to content")
```

### Logging and Tracing

```python
from maestro.src.web_maestro.utils.logging import configure_web_maestro_logging
from maestro.src.web_maestro.trace_utils import trace_extraction

# Configure detailed logging
configure_web_maestro_logging(level="DEBUG")

# Enable tracing for debugging
with trace_extraction("menu_extraction") as tracer:
    result = await fetch_with_ai_scout(url, goal)
    tracer.add_metadata({"items_found": len(result.blocks)})
```

### Health Monitoring

```python
from maestro.src.web_maestro.utils.monitoring import monitor_extraction

# Monitor extraction performance
@monitor_extraction("restaurant_menu")
async def extract_restaurant_menu(url: str):
    return await fetch_with_ai_scout(url, "Extract menu")

# Metrics automatically collected:
# - Extraction time
# - Success rate
# - Content quality
# - Resource usage
```

## Best Practices

### Configuration Selection

1. **Fast Config**: Use for quick validation or lightweight extraction
2. **Standard Config**: Default choice for most extraction tasks
3. **Thorough Config**: Use for comprehensive extraction of complex sites

### Domain Optimization

1. **Match Domain**: Use appropriate domain configuration for content type
2. **Custom Keywords**: Add domain-specific keywords for better targeting
3. **Quality Thresholds**: Adjust based on accuracy requirements

### Error Recovery

1. **Timeout Handling**: Set appropriate timeouts for site complexity
2. **Partial Results**: Accept partial results when full extraction fails
3. **Retry Logic**: Implement exponential backoff for transient failures

### Performance Monitoring

1. **Resource Tracking**: Monitor memory and CPU usage
2. **Success Metrics**: Track extraction success rates
3. **Quality Assessment**: Monitor content quality over time
4. **Error Analysis**: Analyze failure patterns for improvement

## Troubleshooting

### Common Issues

#### Slow Extraction
- Reduce `max_interactions` in configuration
- Use `FAST_CONFIG` profile
- Disable hover exploration for simple sites

#### Missing Content
- Increase `stability_timeout` for dynamic content
- Enable AI scout for better navigation
- Use `THOROUGH_CONFIG` for comprehensive extraction

#### Browser Issues
- Check browser setup and Chrome flags
- Verify Playwright installation
- Review browser resource allocation

#### AI Scout Problems
- Verify LLM client configuration
- Check API key and connection
- Enable fallback strategies

### Debug Mode

```python
# Enable comprehensive debugging
import os
os.environ['DEBUG'] = 'true'
os.environ['WEB_MAESTRO_LOG_LEVEL'] = 'DEBUG'

# Enable browser debugging
result = await fetch_with_ai_scout(
    url=url,
    extraction_goal=goal,
    enable_tracing=True,
    debug_screenshots=True
)
```

### Performance Profiling

```python
# Profile extraction performance
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

result = await fetch_with_ai_scout(url, goal)

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

Web Maestro provides a powerful, production-ready foundation for intelligent web automation and content extraction, with the flexibility to handle diverse content types and extraction requirements.
