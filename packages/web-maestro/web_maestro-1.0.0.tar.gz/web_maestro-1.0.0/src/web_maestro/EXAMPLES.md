# 🌐 Web Maestro - Comprehensive Examples & Recipes

Web Maestro is the AI-powered web automation engine that drives intelligent content extraction. This guide provides extensive examples of its capabilities and advanced usage patterns. 🚀

## 📋 Table of Contents

- [🎯 Basic Web Extraction](#basic-web-extraction)
- [🕵️ AI Scout Integration](#ai-scout-integration)
- [🎭 DOM Capture Strategies](#dom-capture-strategies)
- [⚙️ Configuration & Profiles](#configuration--profiles)
- [🎨 Domain-Specific Extraction](#domain-specific-extraction)
- [📈 Progressive Content Discovery](#progressive-content-discovery)
- [🏭 Production Patterns](#production-patterns)
- [🧪 Advanced Techniques](#advanced-techniques)
- [🛠️ Custom Extensions](#custom-extensions)

## 🎯 Basic Web Extraction

### 🌐 Simple Content Extraction

```python
from maestro.src.web_maestro.fetch import fetch_with_ai_scout
import asyncio

async def basic_extraction():
    """🎯 Basic web content extraction example."""

    result = await fetch_with_ai_scout(
        url="https://restaurant-example.com",
        extraction_goal="Extract menu items with prices"
    )

    print(f"🎯 Extraction completed!")
    print(f"📊 Found {len(result.blocks)} content blocks")
    print(f"⏱️ Extraction time: {result.extraction_time:.2f}s")
    print(f"✅ Success: {result.success}")

    # 📝 Display content blocks
    for i, block in enumerate(result.blocks[:5], 1):
        print(f"\n📦 Block {i}:")
        print(f"  🏷️ Type: {block.element_type}")
        print(f"  📊 Confidence: {block.confidence:.2f}")
        print(f"  📝 Content: {block.content[:100]}...")
        print(f"  🎯 Source: {block.source_info.get('selector', 'unknown')}")

    return result

# 🚀 Run basic extraction
result = asyncio.run(basic_extraction())
```

### 🔍 Multiple URL Extraction

```python
async def multi_url_extraction():
    """📦 Extract content from multiple URLs."""

    urls = [
        "https://restaurant1.com/menu",
        "https://restaurant2.com/food",
        "https://cafe.com/beverages"
    ]

    results = []

    for url in urls:
        print(f"🌐 Processing: {url}")

        try:
            result = await fetch_with_ai_scout(
                url=url,
                extraction_goal="Extract menu items and prices",
                timeout=120
            )

            results.append({
                "url": url,
                "status": "success",
                "blocks_found": len(result.blocks),
                "extraction_time": result.extraction_time,
                "result": result
            })

            print(f"✅ Success: {len(result.blocks)} blocks found")

        except Exception as e:
            print(f"❌ Failed: {str(e)}")
            results.append({
                "url": url,
                "status": "failed",
                "error": str(e)
            })

    # 📊 Summary
    successful = len([r for r in results if r["status"] == "success"])
    print(f"\n📊 Summary: {successful}/{len(urls)} successful extractions")

    return results

# 🚀 Run multi-URL extraction
results = asyncio.run(multi_url_extraction())
```

## 🕵️ AI Scout Integration

### 🧠 AI-Guided Navigation

```python
from maestro.src.web_maestro.agents.scout_bridge import LLMScoutBridge
from maestro.src.clients.portkey_tool_client import PortkeyToolClient

async def ai_scout_navigation():
    """🕵️ Example of AI Scout for intelligent navigation."""

    # 🧠 Initialize AI Scout
    client = PortkeyToolClient()
    scout = LLMScoutBridge(client=client)

    # 🎯 Navigation context
    context = {
        "extraction_goal": "Find detailed wine menu with prices",
        "current_page_url": "https://restaurant.com/beverages",
        "page_title": "Beverage Menu",
        "discovered_content": ["beer list", "cocktails", "soft drinks"],
        "previous_actions": ["clicked_beverages_link"]
    }

    # 🔍 Elements to evaluate
    elements = [
        {
            "text": "Wine Selection",
            "tag": "a",
            "href": "/wines",
            "class": "menu-link",
            "position": {"x": 200, "y": 150}
        },
        {
            "text": "Wine Cellar",
            "tag": "button",
            "data_action": "expand-wine-section",
            "class": "expandable-section",
            "position": {"x": 300, "y": 200}
        },
        {
            "text": "Download Wine List PDF",
            "tag": "a",
            "href": "/wine-list.pdf",
            "class": "download-link",
            "position": {"x": 400, "y": 100}
        }
    ]

    # 🤔 Get AI decisions for each element
    for element in elements:
        decision = await scout.should_interact_with_element(
            element=element,
            context=context
        )

        print(f"🎯 Element: {element['text']}")
        print(f"🤖 Decision: {decision.action}")
        print(f"🧠 Reasoning: {decision.reasoning}")
        print(f"📊 Confidence: {decision.confidence:.2f}")
        print(f"🎯 Priority: {decision.priority}")
        print("---")

    return True

# 🚀 Run AI scout navigation
result = asyncio.run(ai_scout_navigation())
```

### 🎯 Custom AI Scout Prompts

```python
async def custom_ai_scout():
    """🎨 Custom AI Scout with domain-specific prompts."""

    # 🎯 Custom prompt for wine menu extraction
    wine_menu_prompt = """
    You are an expert sommelier and web navigation specialist.

    Your goal: Find comprehensive wine information including:
    - Wine names and vintages
    - Prices (bottle/glass)
    - Descriptions and tasting notes
    - Wine regions and varietals

    Prioritize:
    1. Links to dedicated wine sections
    2. Expandable wine menus
    3. PDF wine lists (often most comprehensive)
    4. Wine category tabs

    Avoid:
    - General beverage links
    - Non-alcoholic drinks
    - Restaurant info pages
    """

    client = PortkeyToolClient()
    scout = LLMScoutBridge(
        client=client,
        custom_prompt=wine_menu_prompt
    )

    # 🍷 Wine-specific extraction
    result = await fetch_with_ai_scout(
        url="https://fine-dining.com/beverages",
        extraction_goal="Extract comprehensive wine menu with prices and descriptions",
        ai_scout=scout,
        domain_keywords=["wine", "vintage", "bottle", "glass", "sommelier"]
    )

    # 🍷 Filter wine-related content
    wine_blocks = [
        block for block in result.blocks
        if any(keyword in block.content.lower()
               for keyword in ["wine", "vintage", "bottle", "cabernet", "chardonnay"])
    ]

    print(f"🍷 Found {len(wine_blocks)} wine-related content blocks")

    return wine_blocks

# 🚀 Run custom AI scout
wine_content = asyncio.run(custom_ai_scout())
```

## 🎭 DOM Capture Strategies

### 📑 Tab Expansion Example

```python
from maestro.src.web_maestro.dom_capture.tab_expansion import expand_all_tabs

async def tab_expansion_example():
    """📑 Example of tab-based content discovery."""

    from maestro.src.web_maestro.browser import create_browser_session

    async with create_browser_session() as session:
        page = session.page

        # 🌐 Navigate to page with tabs
        await page.goto("https://restaurant.com/menu")

        # 📑 Discover and expand all tabs
        tab_results = await expand_all_tabs(
            page=page,
            max_tabs=10,
            wait_after_click=2
        )

        print(f"📑 Found {len(tab_results)} tab sections:")

        for tab_info in tab_results:
            print(f"  🏷️ Tab: {tab_info['tab_text']}")
            print(f"  📊 Content blocks: {len(tab_info['content_blocks'])}")
            print(f"  ⏱️ Load time: {tab_info['load_time']:.2f}s")

            # 📝 Show sample content
            if tab_info['content_blocks']:
                sample = tab_info['content_blocks'][0]
                print(f"  📄 Sample: {sample.content[:80]}...")
            print("---")

    return tab_results

# 🚀 Run tab expansion
results = asyncio.run(tab_expansion_example())
```

### 🍔 Menu & Navigation Expansion

```python
from maestro.src.web_maestro.dom_capture.expansion import expand_navigation_menus

async def menu_expansion_example():
    """🍔 Example of menu and navigation expansion."""

    from maestro.src.web_maestro.browser import create_browser_session

    async with create_browser_session() as session:
        page = session.page
        await page.goto("https://restaurant.com")

        # 🍔 Expand all navigation menus
        expansion_results = await expand_navigation_menus(
            page=page,
            include_hamburger=True,
            include_dropdowns=True,
            include_mega_menus=True
        )

        print(f"🍔 Expanded {len(expansion_results)} menu systems:")

        for menu_info in expansion_results:
            print(f"  🏷️ Menu Type: {menu_info['menu_type']}")
            print(f"  🎯 Trigger: {menu_info['trigger_element']}")
            print(f"  📊 Items Found: {len(menu_info['menu_items'])}")

            # 📝 Show menu items
            for item in menu_info['menu_items'][:3]:
                print(f"    - {item['text']} -> {item.get('href', 'no link')}")

            if len(menu_info['menu_items']) > 3:
                print(f"    ... and {len(menu_info['menu_items']) - 3} more items")
            print("---")

    return expansion_results

# 🚀 Run menu expansion
results = asyncio.run(menu_expansion_example())
```

### 👆 Hover Exploration

```python
from maestro.src.web_maestro.dom_capture.exploration import explore_hover_content

async def hover_exploration_example():
    """👆 Example of hover-based content discovery."""

    from maestro.src.web_maestro.browser import create_browser_session

    async with create_browser_session() as session:
        page = session.page
        await page.goto("https://restaurant.com/menu")

        # 👆 Explore hover interactions
        hover_results = await explore_hover_content(
            page=page,
            max_elements=20,
            hover_duration=1.5,
            wait_for_content=2.0
        )

        print(f"👆 Explored {len(hover_results)} hover interactions:")

        for hover_info in hover_results:
            if hover_info['new_content_found']:
                print(f"  🎯 Element: {hover_info['element_text']}")
                print(f"  📝 Content Type: {hover_info['content_type']}")
                print(f"  📊 Content Length: {len(hover_info['revealed_content'])}")
                print(f"  🔍 Content: {hover_info['revealed_content'][:100]}...")
                print("---")

    return hover_results

# 🚀 Run hover exploration
results = asyncio.run(hover_exploration_example())
```

### 🖱️ Universal Clicking Strategy

```python
from maestro.src.web_maestro.dom_capture.universal_capture import capture_all_content

async def universal_clicking_example():
    """🖱️ Example of systematic universal clicking."""

    from maestro.src.web_maestro.config.base import STANDARD_CONFIG

    # 🎛️ Configure universal capture
    capture_config = STANDARD_CONFIG.copy()
    capture_config.update({
        "max_interactions": 30,
        "click_delay_ms": 500,
        "stability_timeout": 3,
        "enable_hover_exploration": True,
        "enable_tab_expansion": True
    })

    result = await fetch_with_ai_scout(
        url="https://complex-restaurant.com/menu",
        extraction_goal="Extract all menu content from complex interface",
        config=capture_config
    )

    # 📊 Analyze interaction results
    interaction_summary = result.metadata.get("interaction_summary", {})

    print(f"🖱️ Universal Clicking Results:")
    print(f"  📊 Total Interactions: {interaction_summary.get('total_clicks', 0)}")
    print(f"  ✅ Successful Clicks: {interaction_summary.get('successful_clicks', 0)}")
    print(f"  📑 Tabs Expanded: {interaction_summary.get('tabs_expanded', 0)}")
    print(f"  🍔 Menus Opened: {interaction_summary.get('menus_opened', 0)}")
    print(f"  👆 Hover Discoveries: {interaction_summary.get('hover_discoveries', 0)}")
    print(f"  📊 Content Blocks Found: {len(result.blocks)}")

    return result

# 🚀 Run universal clicking
result = asyncio.run(universal_clicking_example())
```

## ⚙️ Configuration & Profiles

### ⚡ Fast Configuration

```python
from maestro.src.web_maestro.config.base import FAST_CONFIG

async def fast_extraction_example():
    """⚡ Quick extraction with minimal interactions."""

    # 🎯 Fast configuration for rapid extraction
    fast_config = FAST_CONFIG.copy()
    fast_config.update({
        "max_interactions": 5,
        "stability_timeout": 1,
        "enable_hover_exploration": False,
        "enable_ai_scout": False,  # Use rule-based decisions
        "timeout_seconds": 30
    })

    start_time = time.time()

    result = await fetch_with_ai_scout(
        url="https://simple-restaurant.com/menu",
        extraction_goal="Quick menu extraction",
        config=fast_config
    )

    end_time = time.time()

    print(f"⚡ Fast Extraction Results:")
    print(f"  ⏱️ Total Time: {end_time - start_time:.2f}s")
    print(f"  📊 Blocks Found: {len(result.blocks)}")
    print(f"  🎯 Extraction Speed: {len(result.blocks)/(end_time - start_time):.1f} blocks/sec")
    print(f"  💾 Memory Efficient: {fast_config.get('memory_optimized', True)}")

    return result

# 🚀 Run fast extraction
result = asyncio.run(fast_extraction_example())
```

### 🔍 Thorough Configuration

```python
from maestro.src.web_maestro.config.base import THOROUGH_CONFIG

async def thorough_extraction_example():
    """🔍 Comprehensive extraction with maximum coverage."""

    # 🎯 Thorough configuration for complete extraction
    thorough_config = THOROUGH_CONFIG.copy()
    thorough_config.update({
        "max_interactions": 100,
        "stability_timeout": 8,
        "enable_hover_exploration": True,
        "enable_ai_scout": True,
        "enable_tab_expansion": True,
        "enable_menu_expansion": True,
        "max_scroll_attempts": 5,
        "wait_for_load": True,
        "timeout_seconds": 600
    })

    result = await fetch_with_ai_scout(
        url="https://complex-restaurant.com/menu",
        extraction_goal="Extract absolutely everything - menus, specials, wine lists, all content",
        config=thorough_config
    )

    print(f"🔍 Thorough Extraction Results:")
    print(f"  📊 Total Blocks: {len(result.blocks)}")
    print(f"  ⏱️ Extraction Time: {result.extraction_time:.2f}s")
    print(f"  🎯 High Confidence Blocks: {len([b for b in result.blocks if b.confidence > 0.8])}")
    print(f"  📑 Content Types Found: {len(set(b.element_type for b in result.blocks))}")

    # 📊 Content analysis
    content_types = {}
    for block in result.blocks:
        content_types[block.element_type] = content_types.get(block.element_type, 0) + 1

    print(f"\n📊 Content Type Breakdown:")
    for content_type, count in sorted(content_types.items()):
        print(f"  {content_type}: {count} blocks")

    return result

# 🚀 Run thorough extraction
result = asyncio.run(thorough_extraction_example())
```

### ⚖️ Balanced Configuration

```python
from maestro.src.web_maestro.config.base import STANDARD_CONFIG

async def balanced_extraction_example():
    """⚖️ Balanced approach for most use cases."""

    # 🎯 Standard configuration with custom tweaks
    balanced_config = STANDARD_CONFIG.copy()
    balanced_config.update({
        "max_interactions": 25,
        "stability_timeout": 4,
        "enable_hover_exploration": True,
        "enable_ai_scout": True,
        "ai_scout_confidence_threshold": 0.7,
        "max_concurrent_interactions": 3,
        "timeout_seconds": 180
    })

    urls = [
        "https://restaurant1.com/menu",
        "https://restaurant2.com/food",
        "https://restaurant3.com/dining"
    ]

    results = []

    for url in urls:
        print(f"⚖️ Processing {url} with balanced config...")

        result = await fetch_with_ai_scout(
            url=url,
            extraction_goal="Extract menu content efficiently",
            config=balanced_config
        )

        results.append({
            "url": url,
            "blocks_found": len(result.blocks),
            "extraction_time": result.extraction_time,
            "efficiency_score": len(result.blocks) / result.extraction_time
        })

        print(f"  📊 Found {len(result.blocks)} blocks in {result.extraction_time:.1f}s")

    # 📊 Performance summary
    avg_efficiency = sum(r["efficiency_score"] for r in results) / len(results)
    print(f"\n📊 Balanced Config Performance:")
    print(f"  🎯 Average Efficiency: {avg_efficiency:.1f} blocks/second")
    print(f"  ⚖️ Good balance of speed and comprehensiveness")

    return results

# 🚀 Run balanced extraction
results = asyncio.run(balanced_extraction_example())
```

## 🎨 Domain-Specific Extraction

### 🍽️ Restaurant Domain

```python
from maestro.src.web_maestro.domains.domain_config import create_domain_config

async def restaurant_domain_example():
    """🍽️ Restaurant-optimized extraction."""

    # 🎯 Restaurant domain configuration
    restaurant_config = create_domain_config(
        domain_type="restaurant",
        custom_keywords=[
            "menu", "food", "dining", "cuisine", "special", "daily",
            "appetizer", "entree", "dessert", "beverage", "wine",
            "price", "dollar", "$", "chef", "seasonal"
        ],
        navigation_patterns=[
            "menu", "food", "dining", "order", "delivery",
            "takeout", "specials", "wine", "drinks"
        ],
        quality_threshold=0.8
    )

    result = await fetch_with_ai_scout(
        url="https://fine-dining-restaurant.com",
        extraction_goal="Extract comprehensive restaurant menu with all sections",
        domain_config=restaurant_config,
        config=THOROUGH_CONFIG
    )

    # 🍽️ Analyze restaurant-specific content
    menu_blocks = []
    price_blocks = []
    special_blocks = []

    for block in result.blocks:
        content_lower = block.content.lower()

        if any(keyword in content_lower for keyword in ["appetizer", "entree", "dessert", "main"]):
            menu_blocks.append(block)

        if "$" in block.content or any(price_term in content_lower for price_term in ["price", "cost", "dollar"]):
            price_blocks.append(block)

        if any(special_term in content_lower for special_term in ["special", "daily", "chef", "seasonal"]):
            special_blocks.append(block)

    print(f"🍽️ Restaurant Content Analysis:")
    print(f"  📋 Menu Blocks: {len(menu_blocks)}")
    print(f"  💰 Price Blocks: {len(price_blocks)}")
    print(f"  ⭐ Special Blocks: {len(special_blocks)}")
    print(f"  📊 Total Blocks: {len(result.blocks)}")

    return {
        "menu_content": menu_blocks,
        "pricing_info": price_blocks,
        "specials": special_blocks,
        "full_result": result
    }

# 🚀 Run restaurant domain extraction
result = asyncio.run(restaurant_domain_example())
```

### 🛒 E-commerce Domain

```python
async def ecommerce_domain_example():
    """🛒 E-commerce optimized extraction."""

    # 🎯 E-commerce domain configuration
    ecommerce_config = create_domain_config(
        domain_type="ecommerce",
        custom_keywords=[
            "product", "price", "buy", "cart", "checkout", "shipping",
            "review", "rating", "stock", "sale", "discount", "offer"
        ],
        navigation_patterns=[
            "shop", "products", "catalog", "categories", "search",
            "cart", "checkout", "account"
        ],
        quality_threshold=0.75
    )

    result = await fetch_with_ai_scout(
        url="https://example-store.com/category/electronics",
        extraction_goal="Extract product catalog with prices and descriptions",
        domain_config=ecommerce_config
    )

    # 🛒 Analyze e-commerce content
    product_blocks = []
    pricing_blocks = []
    review_blocks = []

    for block in result.blocks:
        content_lower = block.content.lower()

        if any(keyword in content_lower for keyword in ["product", "item", "model"]):
            product_blocks.append(block)

        if any(price_indicator in block.content for price_indicator in ["$", "€", "£", "price"]):
            pricing_blocks.append(block)

        if any(review_term in content_lower for review_term in ["review", "rating", "star", "feedback"]):
            review_blocks.append(block)

    print(f"🛒 E-commerce Content Analysis:")
    print(f"  📦 Product Blocks: {len(product_blocks)}")
    print(f"  💰 Pricing Blocks: {len(pricing_blocks)}")
    print(f"  ⭐ Review Blocks: {len(review_blocks)}")

    return {
        "products": product_blocks,
        "pricing": pricing_blocks,
        "reviews": review_blocks,
        "full_result": result
    }

# 🚀 Run e-commerce extraction
result = asyncio.run(ecommerce_domain_example())
```

### 📰 News Domain

```python
async def news_domain_example():
    """📰 News/content optimized extraction."""

    # 🎯 News domain configuration
    news_config = create_domain_config(
        domain_type="news",
        custom_keywords=[
            "article", "news", "story", "headline", "breaking",
            "reporter", "author", "published", "updated", "source"
        ],
        navigation_patterns=[
            "news", "articles", "stories", "breaking", "latest",
            "categories", "sections", "archive"
        ],
        quality_threshold=0.85
    )

    result = await fetch_with_ai_scout(
        url="https://news-website.com/technology",
        extraction_goal="Extract news articles with headlines, content, and metadata",
        domain_config=news_config
    )

    # 📰 Analyze news content
    headline_blocks = []
    article_blocks = []
    metadata_blocks = []

    for block in result.blocks:
        content_lower = block.content.lower()

        if block.element_type in ["h1", "h2", "h3"] and len(block.content) < 200:
            headline_blocks.append(block)

        if len(block.content) > 200 and any(article_indicator in content_lower
                                           for article_indicator in ["article", "story", "report"]):
            article_blocks.append(block)

        if any(meta_term in content_lower for meta_term in ["published", "author", "date", "source"]):
            metadata_blocks.append(block)

    print(f"📰 News Content Analysis:")
    print(f"  📰 Headlines: {len(headline_blocks)}")
    print(f"  📄 Articles: {len(article_blocks)}")
    print(f"  📊 Metadata: {len(metadata_blocks)}")

    return {
        "headlines": headline_blocks,
        "articles": article_blocks,
        "metadata": metadata_blocks,
        "full_result": result
    }

# 🚀 Run news extraction
result = asyncio.run(news_domain_example())
```

## 📈 Progressive Content Discovery

### 🔄 Multi-Phase Extraction

```python
async def multi_phase_extraction():
    """🔄 Progressive extraction with multiple phases."""

    phases = [
        {
            "name": "Quick Scan",
            "config": FAST_CONFIG,
            "goal": "Initial content discovery"
        },
        {
            "name": "Tab Expansion",
            "config": {**STANDARD_CONFIG, "focus_on_tabs": True},
            "goal": "Discover tabbed content"
        },
        {
            "name": "Menu Exploration",
            "config": {**STANDARD_CONFIG, "focus_on_menus": True},
            "goal": "Navigate through menu systems"
        },
        {
            "name": "Deep Dive",
            "config": THOROUGH_CONFIG,
            "goal": "Comprehensive content extraction"
        }
    ]

    url = "https://complex-restaurant.com"
    all_content = []

    for phase in phases:
        print(f"🔄 Phase: {phase['name']}")

        result = await fetch_with_ai_scout(
            url=url,
            extraction_goal=phase['goal'],
            config=phase['config']
        )

        phase_content = [
            block for block in result.blocks
            if block not in all_content  # Avoid duplicates
        ]

        all_content.extend(phase_content)

        print(f"  📊 New content blocks: {len(phase_content)}")
        print(f"  📈 Total content blocks: {len(all_content)}")
        print(f"  ⏱️ Phase time: {result.extraction_time:.2f}s")
        print("---")

    print(f"🎯 Multi-Phase Extraction Complete:")
    print(f"  📊 Total unique blocks: {len(all_content)}")
    print(f"  🎭 Content diversity: {len(set(b.element_type for b in all_content))} types")

    return all_content

# 🚀 Run multi-phase extraction
content = asyncio.run(multi_phase_extraction())
```

### 📊 Incremental Content Analysis

```python
async def incremental_content_analysis():
    """📊 Analyze content as it's discovered."""

    url = "https://restaurant.com/menu"
    discovered_content = []

    # 📈 Progress callback function
    def content_discovered_callback(new_blocks):
        """📊 Analyze content as it's discovered."""
        discovered_content.extend(new_blocks)

        # 📊 Real-time analysis
        menu_items = len([b for b in new_blocks if "price" in b.content.lower()])
        high_confidence = len([b for b in new_blocks if b.confidence > 0.8])

        print(f"📊 New content discovered:")
        print(f"  📋 Menu items: {menu_items}")
        print(f"  🎯 High confidence: {high_confidence}")
        print(f"  📈 Total discovered: {len(discovered_content)}")

    # 🔄 Extraction with progress tracking
    result = await fetch_with_ai_scout(
        url=url,
        extraction_goal="Extract menu with real-time analysis",
        progress_callback=content_discovered_callback,
        config=STANDARD_CONFIG
    )

    # 📊 Final analysis
    print(f"\n🎯 Final Content Analysis:")

    # Group by confidence levels
    confidence_groups = {
        "high": [b for b in discovered_content if b.confidence > 0.8],
        "medium": [b for b in discovered_content if 0.5 < b.confidence <= 0.8],
        "low": [b for b in discovered_content if b.confidence <= 0.5]
    }

    for level, blocks in confidence_groups.items():
        print(f"  📊 {level.title()} confidence: {len(blocks)} blocks")

    return discovered_content

# 🚀 Run incremental analysis
content = asyncio.run(incremental_content_analysis())
```

## 🏭 Production Patterns

### 🔄 Retry and Fallback Strategies

```python
import time
from typing import Dict, Any

async def robust_extraction_with_fallbacks(url: str) -> Dict[str, Any]:
    """🛡️ Production-ready extraction with fallback strategies."""

    strategies = [
        {
            "name": "Fast Attempt",
            "config": FAST_CONFIG,
            "timeout": 60,
            "max_retries": 1
        },
        {
            "name": "Standard Attempt",
            "config": STANDARD_CONFIG,
            "timeout": 120,
            "max_retries": 2
        },
        {
            "name": "Thorough Attempt",
            "config": THOROUGH_CONFIG,
            "timeout": 300,
            "max_retries": 1
        }
    ]

    for strategy in strategies:
        for attempt in range(strategy["max_retries"] + 1):
            try:
                print(f"🔄 {strategy['name']} - Attempt {attempt + 1}")

                start_time = time.time()

                result = await fetch_with_ai_scout(
                    url=url,
                    extraction_goal="Extract content with fallback strategy",
                    config=strategy["config"],
                    timeout=strategy["timeout"]
                )

                execution_time = time.time() - start_time

                # ✅ Success criteria
                if (len(result.blocks) > 0 and
                    result.success and
                    execution_time < strategy["timeout"]):

                    print(f"✅ Success with {strategy['name']}")
                    return {
                        "status": "success",
                        "strategy_used": strategy["name"],
                        "attempt_number": attempt + 1,
                        "execution_time": execution_time,
                        "blocks_found": len(result.blocks),
                        "result": result
                    }

            except Exception as e:
                print(f"❌ {strategy['name']} failed: {str(e)}")

                # 🔄 Wait before retry
                if attempt < strategy["max_retries"]:
                    wait_time = (attempt + 1) * 2  # Exponential backoff
                    print(f"⏳ Waiting {wait_time}s before retry...")
                    await asyncio.sleep(wait_time)

    # 🚨 All strategies failed
    return {
        "status": "failed",
        "error": "All extraction strategies exhausted",
        "strategies_attempted": len(strategies)
    }

# 🚀 Run robust extraction
result = asyncio.run(robust_extraction_with_fallbacks("https://difficult-site.com"))
```

### 📊 Performance Monitoring

```python
import json
from datetime import datetime
from collections import defaultdict

class WebMaestroMonitor:
    """📊 Production monitoring for Web Maestro operations."""

    def __init__(self):
        self.metrics = defaultdict(list)
        self.start_time = time.time()

    def record_extraction(self, url: str, result: Dict[str, Any],
                         strategy: str, execution_time: float):
        """📈 Record extraction metrics."""

        metric = {
            "timestamp": datetime.now().isoformat(),
            "url": url,
            "strategy": strategy,
            "execution_time": execution_time,
            "success": result.get("status") == "success",
            "blocks_found": result.get("blocks_found", 0),
            "confidence_avg": self._calculate_avg_confidence(result),
            "content_types": self._analyze_content_types(result)
        }

        self.metrics["extractions"].append(metric)

    def _calculate_avg_confidence(self, result: Dict[str, Any]) -> float:
        """📊 Calculate average confidence score."""
        if "result" in result and hasattr(result["result"], "blocks"):
            blocks = result["result"].blocks
            if blocks:
                return sum(block.confidence for block in blocks) / len(blocks)
        return 0.0

    def _analyze_content_types(self, result: Dict[str, Any]) -> Dict[str, int]:
        """📊 Analyze content type distribution."""
        if "result" in result and hasattr(result["result"], "blocks"):
            blocks = result["result"].blocks
            types = defaultdict(int)
            for block in blocks:
                types[block.element_type] += 1
            return dict(types)
        return {}

    def get_performance_report(self) -> Dict[str, Any]:
        """📊 Generate performance report."""
        extractions = self.metrics["extractions"]

        if not extractions:
            return {"error": "No extractions recorded"}

        # 📊 Calculate statistics
        total = len(extractions)
        successful = sum(1 for e in extractions if e["success"])
        success_rate = successful / total if total > 0 else 0

        execution_times = [e["execution_time"] for e in extractions]
        avg_time = sum(execution_times) / len(execution_times)

        # 📈 Strategy performance
        strategy_stats = defaultdict(lambda: {"total": 0, "successful": 0, "avg_time": 0})

        for extraction in extractions:
            strategy = extraction["strategy"]
            strategy_stats[strategy]["total"] += 1
            if extraction["success"]:
                strategy_stats[strategy]["successful"] += 1
            strategy_stats[strategy]["avg_time"] += extraction["execution_time"]

        # 📊 Finalize strategy stats
        for strategy, stats in strategy_stats.items():
            stats["success_rate"] = stats["successful"] / stats["total"]
            stats["avg_time"] /= stats["total"]

        return {
            "summary": {
                "total_extractions": total,
                "success_rate": success_rate,
                "average_execution_time": avg_time,
                "uptime_hours": (time.time() - self.start_time) / 3600
            },
            "strategy_performance": dict(strategy_stats),
            "recent_extractions": extractions[-10:]  # Last 10
        }

    def save_report(self, filename: str):
        """💾 Save performance report to file."""
        report = self.get_performance_report()
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"📊 Performance report saved to {filename}")

# 🚀 Usage example
async def monitored_extraction_example():
    """📊 Example with performance monitoring."""

    monitor = WebMaestroMonitor()

    test_urls = [
        "https://restaurant1.com/menu",
        "https://restaurant2.com/food",
        "https://restaurant3.com/dining"
    ]

    for url in test_urls:
        print(f"🌐 Processing: {url}")

        start_time = time.time()
        result = await robust_extraction_with_fallbacks(url)
        execution_time = time.time() - start_time

        # 📊 Record metrics
        monitor.record_extraction(
            url=url,
            result=result,
            strategy=result.get("strategy_used", "unknown"),
            execution_time=execution_time
        )

    # 📊 Generate report
    report = monitor.get_performance_report()
    print(f"\n📊 Performance Report:")
    print(f"  🎯 Success Rate: {report['summary']['success_rate']:.2%}")
    print(f"  ⏱️ Avg Time: {report['summary']['average_execution_time']:.2f}s")
    print(f"  🚀 Total Extractions: {report['summary']['total_extractions']}")

    # 💾 Save detailed report
    monitor.save_report("web_maestro_performance.json")

    return report

# 🚀 Run monitored extraction
report = asyncio.run(monitored_extraction_example())
```

## 🧪 Advanced Techniques

### 🎯 Content Quality Assessment

```python
async def content_quality_assessment():
    """🎯 Advanced content quality assessment."""

    url = "https://restaurant.com/menu"

    result = await fetch_with_ai_scout(
        url=url,
        extraction_goal="Extract menu content with quality assessment",
        config=THOROUGH_CONFIG
    )

    # 🎯 Quality assessment criteria
    quality_metrics = {
        "high_confidence": 0,
        "has_pricing": 0,
        "detailed_descriptions": 0,
        "structured_content": 0,
        "relevant_keywords": 0
    }

    relevant_keywords = ["menu", "food", "price", "dish", "appetizer", "entree", "dessert"]

    for block in result.blocks:
        # 📊 High confidence content
        if block.confidence > 0.8:
            quality_metrics["high_confidence"] += 1

        # 💰 Pricing information
        if "$" in block.content or "price" in block.content.lower():
            quality_metrics["has_pricing"] += 1

        # 📝 Detailed descriptions (longer content)
        if len(block.content) > 50:
            quality_metrics["detailed_descriptions"] += 1

        # 🏗️ Structured content (specific HTML elements)
        if block.element_type in ["div", "li", "td", "article"]:
            quality_metrics["structured_content"] += 1

        # 🎯 Relevant keywords
        if any(keyword in block.content.lower() for keyword in relevant_keywords):
            quality_metrics["relevant_keywords"] += 1

    # 📊 Calculate quality score
    total_blocks = len(result.blocks)
    quality_score = sum(quality_metrics.values()) / (total_blocks * len(quality_metrics))

    print(f"🎯 Content Quality Assessment:")
    print(f"  📊 Total Blocks: {total_blocks}")
    print(f"  🎯 High Confidence: {quality_metrics['high_confidence']} ({quality_metrics['high_confidence']/total_blocks:.1%})")
    print(f"  💰 Has Pricing: {quality_metrics['has_pricing']} ({quality_metrics['has_pricing']/total_blocks:.1%})")
    print(f"  📝 Detailed Descriptions: {quality_metrics['detailed_descriptions']} ({quality_metrics['detailed_descriptions']/total_blocks:.1%})")
    print(f"  🏗️ Structured Content: {quality_metrics['structured_content']} ({quality_metrics['structured_content']/total_blocks:.1%})")
    print(f"  🎯 Relevant Keywords: {quality_metrics['relevant_keywords']} ({quality_metrics['relevant_keywords']/total_blocks:.1%})")
    print(f"  🏆 Overall Quality Score: {quality_score:.2f}")

    return {
        "quality_metrics": quality_metrics,
        "quality_score": quality_score,
        "total_blocks": total_blocks,
        "result": result
    }

# 🚀 Run quality assessment
assessment = asyncio.run(content_quality_assessment())
```

### 🔍 Content Deduplication

```python
import hashlib
from typing import List, Set

async def content_deduplication_example():
    """🔍 Advanced content deduplication techniques."""

    result = await fetch_with_ai_scout(
        url="https://restaurant.com/menu",
        extraction_goal="Extract content with deduplication",
        config=THOROUGH_CONFIG
    )

    # 🔍 Different deduplication strategies
    exact_duplicates: Set[str] = set()
    content_hashes: Set[str] = set()
    semantic_groups: Dict[str, List] = defaultdict(list)

    unique_blocks = []
    duplicate_count = 0

    for block in result.blocks:
        content = block.content.strip()

        # 🎯 Exact duplicate detection
        if content in exact_duplicates:
            duplicate_count += 1
            continue
        exact_duplicates.add(content)

        # 🔍 Hash-based deduplication (normalize whitespace)
        normalized_content = " ".join(content.split())
        content_hash = hashlib.md5(normalized_content.encode()).hexdigest()

        if content_hash in content_hashes:
            duplicate_count += 1
            continue
        content_hashes.add(content_hash)

        # 📊 Semantic grouping (by content length and type)
        semantic_key = f"{block.element_type}_{len(content)//50*50}"  # Group by type and length ranges
        semantic_groups[semantic_key].append(block)

        unique_blocks.append(block)

    print(f"🔍 Content Deduplication Results:")
    print(f"  📊 Original Blocks: {len(result.blocks)}")
    print(f"  ✨ Unique Blocks: {len(unique_blocks)}")
    print(f"  🗑️ Duplicates Removed: {duplicate_count}")
    print(f"  📈 Deduplication Rate: {duplicate_count/len(result.blocks):.1%}")

    # 📊 Semantic group analysis
    print(f"\n📊 Semantic Groups:")
    for group_key, blocks in semantic_groups.items():
        if len(blocks) > 1:
            print(f"  🏷️ {group_key}: {len(blocks)} similar blocks")

    return {
        "original_count": len(result.blocks),
        "unique_blocks": unique_blocks,
        "duplicates_removed": duplicate_count,
        "semantic_groups": semantic_groups
    }

# 🚀 Run deduplication
result = asyncio.run(content_deduplication_example())
```

## 🛠️ Custom Extensions

### 🎨 Custom DOM Capture Strategy

```python
from maestro.src.web_maestro.dom_capture.capture import CaptureStrategy

class CustomMenuCaptureStrategy(CaptureStrategy):
    """🎨 Custom capture strategy for restaurant menus."""

    async def capture_content(self, page, config):
        """🍽️ Custom menu-focused capture logic."""

        # 🔍 Look for menu-specific elements first
        menu_selectors = [
            ".menu-item", ".food-item", ".dish",
            "[data-menu]", "[data-food]", ".restaurant-menu",
            ".menu-section", ".food-category"
        ]

        captured_blocks = []

        for selector in menu_selectors:
            try:
                elements = await page.query_selector_all(selector)

                for element in elements:
                    # 📝 Extract element content
                    content = await element.text_content()
                    if content and len(content.strip()) > 5:

                        # 🎯 Calculate relevance score
                        relevance = self._calculate_menu_relevance(content)

                        if relevance > 0.5:
                            captured_blocks.append({
                                "content": content.strip(),
                                "element_type": "menu-item",
                                "confidence": relevance,
                                "source_info": {
                                    "selector": selector,
                                    "custom_strategy": "menu_focused"
                                }
                            })

            except Exception as e:
                print(f"❌ Error with selector {selector}: {e}")

        return captured_blocks

    def _calculate_menu_relevance(self, content: str) -> float:
        """🎯 Calculate how relevant content is to menus."""

        menu_indicators = [
            "price", "$", "dollar", "appetizer", "entree", "dessert",
            "beverage", "wine", "beer", "cocktail", "dish", "served",
            "ingredients", "sauce", "grilled", "fried", "baked"
        ]

        content_lower = content.lower()
        matches = sum(1 for indicator in menu_indicators if indicator in content_lower)

        # 📊 Base relevance on keyword density
        relevance = min(matches / 5, 1.0)  # Max out at 5 matches

        # 🎯 Boost for price indicators
        if "$" in content or "price" in content_lower:
            relevance += 0.3

        # 📏 Penalize very short or very long content
        if len(content) < 10:
            relevance *= 0.5
        elif len(content) > 500:
            relevance *= 0.7

        return min(relevance, 1.0)

# 🚀 Usage example
async def custom_strategy_example():
    """🎨 Example using custom capture strategy."""

    custom_strategy = CustomMenuCaptureStrategy()

    # Note: Integration would require modifying the core capture system
    # This is a conceptual example of how custom strategies could work

    print("🎨 Custom menu capture strategy would be applied here")
    return custom_strategy

# 🚀 Run custom strategy example
strategy = asyncio.run(custom_strategy_example())
```

### 🔧 Custom AI Scout Implementation

```python
from maestro.src.web_maestro.agents.scout_bridge import ScoutBridge

class RestaurantAIScout(ScoutBridge):
    """🔧 Custom AI Scout specialized for restaurant websites."""

    def __init__(self, client):
        super().__init__(client)
        self.restaurant_keywords = [
            "menu", "food", "dining", "cuisine", "special", "wine",
            "appetizer", "entree", "dessert", "chef", "seasonal"
        ]

    async def should_interact_with_element(self, element, context):
        """🤔 Restaurant-specific interaction decisions."""

        element_text = element.get("text", "").lower()
        element_href = element.get("href", "").lower()

        # 🍽️ High priority for menu-related elements
        menu_priority = self._calculate_menu_priority(element_text, element_href)

        if menu_priority > 0.8:
            return {
                "action": "click",
                "confidence": menu_priority,
                "reasoning": f"High menu relevance: {element_text[:50]}",
                "priority": "high"
            }

        # 🧠 Use AI for borderline cases
        if menu_priority > 0.3:
            ai_decision = await self._get_ai_decision(element, context)
            return ai_decision

        # 🚫 Skip irrelevant elements
        return {
            "action": "skip",
            "confidence": 1.0 - menu_priority,
            "reasoning": "Low restaurant relevance",
            "priority": "low"
        }

    def _calculate_menu_priority(self, text: str, href: str) -> float:
        """🎯 Calculate restaurant-specific priority."""

        priority = 0.0

        # 🍽️ Text-based indicators
        for keyword in self.restaurant_keywords:
            if keyword in text:
                priority += 0.2

        # 🔗 URL-based indicators
        menu_url_indicators = ["menu", "food", "dining", "wine", "drinks"]
        for indicator in menu_url_indicators:
            if indicator in href:
                priority += 0.3

        # 🚫 Negative indicators
        negative_indicators = ["about", "contact", "location", "hours", "reservation"]
        for negative in negative_indicators:
            if negative in text or negative in href:
                priority -= 0.2

        return max(0.0, min(1.0, priority))

    async def _get_ai_decision(self, element, context):
        """🧠 Get AI decision for complex cases."""

        prompt = f"""
        You are a restaurant menu extraction specialist.

        Context: {context.get('extraction_goal', 'Extract restaurant menu')}
        Element: {element.get('text', '')[:100]}
        URL: {element.get('href', 'no link')}

        Should I interact with this element to find menu content?
        Consider: Will this likely lead to menu items, prices, or food descriptions?

        Respond with JSON: {{"action": "click/skip", "confidence": 0.0-1.0, "reasoning": "explanation"}}
        """

        # Mock AI response (would use actual LLM client)
        return {
            "action": "click" if "menu" in element.get("text", "").lower() else "skip",
            "confidence": 0.7,
            "reasoning": "AI analysis based on restaurant context",
            "priority": "medium"
        }

# 🚀 Usage example
async def custom_scout_example():
    """🔧 Example using custom restaurant AI scout."""

    client = PortkeyToolClient()
    restaurant_scout = RestaurantAIScout(client)

    # 🧪 Test element
    test_element = {
        "text": "Wine Selection",
        "href": "/wines",
        "tag": "a"
    }

    test_context = {
        "extraction_goal": "Extract comprehensive wine menu"
    }

    decision = await restaurant_scout.should_interact_with_element(
        test_element, test_context
    )

    print(f"🔧 Custom Scout Decision:")
    print(f"  🎯 Action: {decision['action']}")
    print(f"  📊 Confidence: {decision['confidence']:.2f}")
    print(f"  🧠 Reasoning: {decision['reasoning']}")

    return decision

# 🚀 Run custom scout example
decision = asyncio.run(custom_scout_example())
```

This comprehensive Web Maestro examples guide demonstrates the full spectrum of intelligent web automation capabilities, from basic extraction to advanced production patterns and custom extensions! 🌐✨
