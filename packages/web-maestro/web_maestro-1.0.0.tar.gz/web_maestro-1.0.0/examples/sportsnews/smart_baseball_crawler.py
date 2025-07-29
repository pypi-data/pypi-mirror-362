"""Smart Baseball News Crawler with LLM-Powered Content Extraction

This crawler uses LLM analysis to identify and extract meaningful baseball news
paragraphs, filtering out navigation, marketing, and irrelevant content.

Now supports external configuration via YAML files for better maintainability.
"""

import argparse
import asyncio
from datetime import datetime
import hashlib
import json
import logging
import os
from typing import Any

# Configuration loader
from config_loader import BaseballCrawlerConfig, create_default_config, load_config

from web_maestro.config.base import create_default_config as create_web_maestro_config
from web_maestro.context import SessionContext
from web_maestro.fetch import fetch_rendered_html
from web_maestro.models.types import CapturedBlock

# Core web_maestro imports
from web_maestro.providers.base import LLMConfig
from web_maestro.providers.portkey import PortkeyProvider

# Try to import scout bridge, fallback if not available
try:
    from web_maestro.agents.scout_bridge import (
        LLMScoutBridge,
        NavigationAction,
        NavigationContext,
    )

    SCOUT_BRIDGE_AVAILABLE = True
except ImportError:
    SCOUT_BRIDGE_AVAILABLE = False
    LLMScoutBridge = None
    NavigationContext = None
    NavigationAction = None


def setup_logging(config: BaseballCrawlerConfig):
    """Configure logging based on configuration."""
    # Configure comprehensive logging with detailed tracing
    logging.basicConfig(
        level=getattr(logging, config.logging.level),
        format="%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(config.logging.detailed_log_file),
            logging.FileHandler(config.logging.error_log_file, mode="w"),
        ],
    )

    # Set specific log levels for different modules
    for module, level in config.logging.modules.items():
        logging.getLogger(module).setLevel(getattr(logging, level))

    # Create error-only handler
    error_handler = logging.FileHandler(config.logging.error_log_file, mode="w")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logging.getLogger().addHandler(error_handler)


# Global config and logger will be set in main()
config = None
logger = None


async def generate_final_summary(
    baseball_news: list[dict[str, Any]],
    provider: PortkeyProvider,
    config: BaseballCrawlerConfig,
) -> dict[str, Any]:
    """Generate a comprehensive summary of all extracted baseball news."""
    if not baseball_news:
        return {
            "summary": "No baseball news was extracted.",
            "key_topics": [],
            "total_articles": 0,
            "word_count": 0,
        }

    # Combine all news content for analysis
    all_content = []
    total_word_count = 0

    for news_item in baseball_news[:20]:  # Limit to top 20 articles for summary
        content = news_item["content"]
        all_content.append(content)
        total_word_count += len(content.split())

    combined_text = "\n\n---\n\n".join(all_content)

    # Create LLM prompt for summary using config template
    prompt = config.llm.summary_prompt.format(
        article_count=len(all_content), content=combined_text[:8000]
    )

    try:
        logger.info("Generating final summary with LLM")
        response = await provider.complete(prompt)

        if response.success:
            import re

            # Extract JSON from response
            json_match = re.search(r"\{.*\}", response.content, re.DOTALL)
            if json_match:
                summary_data = json.loads(json_match.group())
                summary_data.update(
                    {
                        "total_articles": len(baseball_news),
                        "word_count": total_word_count,
                        "generation_method": "llm_analysis",
                    }
                )
                logger.info("Successfully generated final summary")
                return summary_data
            else:
                logger.warning("Could not parse LLM summary response")

    except Exception as e:
        logger.error(f"Error generating final summary: {e}")

    # Fallback summary
    return {
        "summary": f"Extracted {len(baseball_news)} baseball news articles with {total_word_count} total words.",
        "key_topics": ["baseball", "mlb"],
        "total_articles": len(baseball_news),
        "word_count": total_word_count,
        "generation_method": "fallback",
    }


async def extract_baseball_news_with_llm(
    url: str,
    blocks: list[CapturedBlock],
    provider: PortkeyProvider,
    config: BaseballCrawlerConfig,
) -> dict[str, Any]:
    """Use LLM to extract meaningful baseball news content from page blocks.

    Args:
        url: The URL of the page
        blocks: Captured content blocks from the page
        provider: LLM provider for content analysis

    Returns:
        Dict containing extracted baseball news paragraphs
    """
    logger.info(f"Starting LLM analysis of {url}: {len(blocks)} blocks")
    print(f"  🤖 LLM analysis of {url}: {len(blocks)} blocks")

    # Filter to meaningful text blocks using config settings
    text_blocks = []
    logger.debug(f"🔍 Processing {len(blocks)} blocks for meaningful content")

    for i, block in enumerate(blocks):
        if hasattr(block, "content") and isinstance(block.content, str):
            content_length = len(block.content.strip())
            logger.debug(
                f"   Block {i}: content_length={content_length}, type={getattr(block, 'capture_type', 'unknown')}"
            )

            # Use config for content size filtering
            min_chars = config.crawler.content_size_range["min_chars"]
            max_chars = config.crawler.content_size_range["max_chars"]
            if min_chars <= content_length <= max_chars:
                # Skip obvious navigation/menu content using config patterns
                content = block.content.strip().lower()
                skip_patterns = config.crawler.skip_patterns

                # Look for content that might contain actual sentences/news
                has_sentences = "." in content and (
                    " the " in content or " a " in content or " an " in content
                )
                is_likely_news = has_sentences and not any(
                    skip in content for skip in skip_patterns
                )

                if is_likely_news:
                    text_blocks.append(block.content.strip())
                    logger.debug(f"   ✅ Block {i} accepted: {content[:100]}...")
                else:
                    logger.debug(
                        f"   ❌ Block {i} skipped (navigation/scores): {content[:50]}..."
                    )
            else:
                logger.debug(f"   ❌ Block {i} skipped (size): {content_length} chars")
        else:
            logger.debug(f"   ❌ Block {i} skipped (no content): {type(block)}")

    logger.info(f"Found {len(text_blocks)} substantial text blocks for {url}")
    print(f"    Found {len(text_blocks)} substantial text blocks")

    if not text_blocks:
        logger.warning(f"No substantial text blocks found for {url}")
        return {"url": url, "baseball_news": [], "analysis_performed": False}

    # Combine blocks into chunks for LLM analysis using config settings
    chunk_size = config.llm.chunk_size
    baseball_news = []

    # Limit total blocks to analyze using config
    text_blocks = sorted(text_blocks, key=len, reverse=True)[
        : config.llm.max_blocks_to_analyze
    ]

    for i in range(0, len(text_blocks), chunk_size):
        chunk_blocks = text_blocks[i : i + chunk_size]
        combined_text = "\n\n---BLOCK---\n\n".join(chunk_blocks)

        # LLM prompt using config template
        prompt = config.llm.extraction_prompt.format(
            content=combined_text[: config.llm.content_preview_length]
        )

        try:
            response = await provider.complete(prompt)
            if response.success:
                logger.debug(
                    f"🤖 LLM response for chunk {i // chunk_size + 1}: {response.content}"
                )
                # Parse LLM response
                try:
                    import re

                    # Extract JSON from response (handle ```json wrapper)
                    content = response.content.strip()

                    # Remove ```json wrapper if present
                    if content.startswith("```json"):
                        content = content[7:]  # Remove ```json
                    if content.startswith("```"):
                        content = content[3:]  # Remove just ```
                    if content.endswith("```"):
                        content = content[:-3]  # Remove closing ```

                    # Try to extract JSON from the cleaned content
                    json_match = re.search(
                        r'\{[^}]*"baseball_news"[^}]*\}', content, re.DOTALL
                    )
                    if json_match:
                        json_text = json_match.group()
                        logger.debug(f"📝 Extracted JSON: {json_text}")
                        result = json.loads(json_text)
                        news_items = result.get("baseball_news", [])

                        logger.debug(
                            f"🔍 Found {len(news_items)} news items in LLM response"
                        )

                        # Validate and clean news items - require substantial content
                        valid_items = 0
                        for item in news_items:
                            if isinstance(item, str) and len(item.strip()) > 300:
                                baseball_news.append(
                                    {
                                        "content": item.strip(),
                                        "url": url,
                                        "chunk_index": i // chunk_size,
                                        "extracted_by": "llm",
                                    }
                                )
                                valid_items += 1
                                logger.debug(f"   ✅ Valid item: {item[:100]}...")
                            else:
                                logger.debug(f"   ❌ Invalid item: {item}")

                        logger.info(
                            f"LLM extracted {valid_items} valid news items from chunk {i // chunk_size + 1} of {url}"
                        )
                        print(
                            f"      ⚾ LLM extracted {valid_items} news items from chunk {i // chunk_size + 1}"
                        )
                    else:
                        logger.warning(
                            f"No JSON found in LLM response: {response.content[:200]}..."
                        )

                except (json.JSONDecodeError, KeyError) as e:
                    logger.error(f"Failed to parse LLM response for {url}: {e}")
                    logger.debug(f"Raw response: {response.content}")
                    print(f"      ⚠️ Failed to parse LLM response: {e}")
            else:
                logger.error(f"LLM request failed for {url}: {response.error}")

        except Exception as e:
            logger.error(f"LLM analysis failed for {url}: {e}")
            print(f"      ❌ LLM analysis failed: {e}")

    logger.info(f"Total baseball news extracted from {url}: {len(baseball_news)}")
    print(f"    📰 Total baseball news extracted: {len(baseball_news)}")

    return {
        "url": url,
        "total_blocks": len(blocks),
        "analyzed_blocks": len(text_blocks),
        "baseball_news": baseball_news,
        "analysis_performed": True,
    }


if SCOUT_BRIDGE_AVAILABLE:

    class BaseballScoutBridge(LLMScoutBridge):
        """Baseball-specific scout bridge for intelligent navigation."""

        def __init__(self, provider: PortkeyProvider, config: BaseballCrawlerConfig):
            """Initialize with Portkey provider and config."""
            self.provider = provider
            self.config = config
            domain_config = {
                "extraction_goal": "baseball_news_content",
                "target_domain": "espn.com",
                "content_types": ["articles", "news", "stories", "reports"],
            }
            super().__init__(provider, domain_config)

        async def should_follow_link(
            self, url: str, link_text: str, context_url: str
        ) -> bool:
            """Determine if a link should be followed for baseball content."""
            logger.debug(f"Scout bridge evaluating link: {url}")

            # Basic technical filters
            skip_patterns = [
                ".pdf",
                ".jpg",
                ".png",
                ".gif",
                "#",
                "mailto:",
                "javascript:",
                "facebook.com",
                "twitter.com",
                "instagram.com",
                "tiktok.com",
            ]

            url_lower = url.lower()
            if any(pattern in url_lower for pattern in skip_patterns):
                logger.debug(f"Skipping link (technical filter): {url}")
                return False

            # Use LLM for intelligent decision with config template
            prompt = self.config.scout_bridge.link_filter_prompt.format(
                context_url=context_url, link_url=url, link_text=link_text
            )

            try:
                response = await self.provider.complete(prompt)
                if response.success:
                    decision_text = response.content.strip().upper()
                    should_follow = decision_text.startswith("FOLLOW")
                    action = "accepted" if should_follow else "rejected"
                    logger.info(f"Scout bridge decision for {url}: {action}")
                    logger.debug(f"Scout reasoning: {response.content.strip()}")
                    return should_follow
                else:
                    logger.warning(
                        f"Scout bridge failed for {url}, defaulting to False"
                    )
                    return False
            except Exception as e:
                logger.error(f"Scout bridge error for {url}: {e}")
                return False

else:

    class BaseballScoutBridge:
        """Fallback scout bridge when the real one isn't available."""

        def __init__(self, provider: PortkeyProvider, config: BaseballCrawlerConfig):
            self.provider = provider
            self.config = config
            logger.warning("Scout bridge not available, using simple fallback")

        async def should_follow_link(
            self, url: str, link_text: str, context_url: str
        ) -> bool:
            """Simple fallback link filter."""
            url_lower = url.lower()
            skip_patterns = [
                ".pdf",
                ".jpg",
                ".png",
                ".gif",
                "#",
                "mailto:",
                "javascript:",
                "facebook.com",
                "twitter.com",
                "instagram.com",
                "tiktok.com",
            ]

            if any(pattern in url_lower for pattern in skip_patterns):
                return False

            # Use config keywords for filtering
            keywords = self.config.scout_bridge.baseball_keywords + [
                "/sports/",
                "/news/",
            ]
            return any(keyword in url_lower for keyword in keywords)


def deduplicate_news_items(news_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Remove duplicate news items using content-based hashing with fuzzy matching.

    Args:
        news_items: List of news item dictionaries with 'content' field

    Returns:
        List of unique news items, keeping the first occurrence of each
    """
    logger = logging.getLogger(__name__)

    if not news_items:
        return news_items

    seen_hashes = set()
    seen_normalized = set()
    unique_items = []

    for i, item in enumerate(news_items):
        content = item.get("content", "").strip()

        if not content:
            continue

        # Method 1: Exact content hash (catches identical content)
        content_hash = hashlib.md5(content.encode("utf-8")).hexdigest()  # noqa: S324

        # Method 2: Normalized content hash (catches near-duplicates)
        # Remove punctuation, extra whitespace, and convert to lowercase
        normalized = " ".join(
            content.lower()
            .replace("—", "-")
            .replace('"', "")
            .replace('"', "")
            .replace("'", "")
            .replace(",", "")
            .replace(".", "")
            .replace("!", "")
            .replace("?", "")
            .replace(":", "")
            .replace(";", "")
            .split()
        )
        normalized_hash = hashlib.md5(
            normalized.encode("utf-8")
        ).hexdigest()  # noqa: S324

        # Method 3: Title-based deduplication (for headlines)
        # Extract potential title (first sentence or up to first dash/colon)
        title_candidates = [
            content.split("—")[0].strip(),
            content.split(":")[0].strip(),
            content.split(".")[0].strip(),
        ]
        title = min(title_candidates, key=len) if title_candidates else content[:100]
        title_normalized = " ".join(title.lower().split())
        title_hash = hashlib.md5(
            title_normalized.encode("utf-8")
        ).hexdigest()  # noqa: S324

        # Check for duplicates using any of the three methods
        if (
            content_hash in seen_hashes
            or normalized_hash in seen_normalized
            or title_hash in seen_hashes
        ):
            logger.debug(f"🧹 Removing duplicate {i+1}: {content[:60]}...")
            continue

        # Mark as seen using all hash types
        seen_hashes.add(content_hash)
        seen_hashes.add(title_hash)
        seen_normalized.add(normalized_hash)

        unique_items.append(item)
        logger.debug(f"✅ Keeping unique item {i+1}: {content[:60]}...")

    return unique_items


def baseball_link_filter(base_url: str, target_url: str) -> bool:
    """Simple fallback filter - will be replaced by LLM filter in crawl function."""
    # Basic technical filters only
    skip_patterns = [
        ".pdf",
        ".jpg",
        ".png",
        ".gif",
        "#",
        "mailto:",
        "javascript:",
        "facebook.com",
        "twitter.com",
        "instagram.com",
        "tiktok.com",
        "/login",
        "/register",
        "/subscribe",
    ]

    target_lower = target_url.lower()
    if any(pattern in target_lower for pattern in skip_patterns):
        return False

    # Allow most links for LLM evaluation
    return True


async def crawl_baseball_news_smart(
    config: BaseballCrawlerConfig, depth: int = None, max_pages: int = None
) -> dict[str, Any]:
    """Crawl ESPN for baseball news using LLM-powered content extraction.

    Args:
        config: Baseball crawler configuration
        depth: Maximum crawl depth (overrides config if provided)
        max_pages: Maximum number of pages to crawl (overrides config if provided)

    Returns:
        Dict containing crawl results and extracted baseball news
    """

    # Use config values if not overridden
    if depth is None:
        depth = config.crawler.max_depth
    if max_pages is None:
        max_pages = config.crawler.max_pages
    # Setup LLM provider
    try:
        from espn_config import PORTKEY_CONFIG

        llm_config = LLMConfig(**PORTKEY_CONFIG)
    except ImportError:
        llm_config = LLMConfig(
            provider="portkey",
            api_key=os.getenv("PORTKEY_API_KEY"),
            model="gpt-4o",
            extra_params={"virtual_key": os.getenv("PORTKEY_VIRTUAL_KEY")},
        )

    provider = PortkeyProvider(llm_config)

    # Initialize scout bridge for intelligent navigation
    scout = BaseballScoutBridge(provider, config)
    logger.info("Initialized Baseball Scout Bridge for intelligent link filtering")

    print("🤖 Smart Baseball News Crawler (Scout Bridge + LLM)")
    print(f"📊 Settings: depth={depth}, max_pages={max_pages}")
    print("-" * 60)

    # Configure DOM capture using config settings
    dom_config = create_web_maestro_config("fast")
    dom_config["max_tabs"] = 1
    dom_config["expand_buttons"] = False  # Skip expansion for speed
    dom_config["explore_elements"] = 10  # Fewer elements
    dom_config["max_scrolls"] = 2
    dom_config["scroll"] = True
    dom_config["max_concurrent_crawls"] = config.crawler.max_concurrent_crawls

    ctx = SessionContext()

    # Content processor that uses LLM
    async def llm_content_processor(
        url: str, blocks: list[CapturedBlock]
    ) -> dict[str, Any]:
        return await extract_baseball_news_with_llm(url, blocks, provider, config)

    print("🌐 Starting smart crawl from ESPN MLB section...")
    start_time = datetime.now()

    # Custom crawl function with LLM link filtering and detailed tracing
    async def smart_crawl_recursive(
        url: str, current_depth: int = 0, visited: set[str] = None
    ) -> dict[str, Any]:
        if visited is None:
            visited = set()

        logger.debug(
            f"🔄 smart_crawl_recursive called: url={url}, depth={current_depth}, visited_count={len(visited)}"
        )

        # Check depth and page limits
        if current_depth > depth:
            logger.debug(f"❌ Depth limit reached: {current_depth} > {depth}")
            return {"pages": []}

        if len(visited) >= max_pages:
            logger.debug(f"❌ Page limit reached: {len(visited)} >= {max_pages}")
            return {"pages": []}

        normalized_url = url.strip()
        logger.debug(f"🔗 Processing URL: {normalized_url}")

        if normalized_url in visited:
            logger.debug(f"⏭️ URL already visited, skipping: {normalized_url}")
            return {"pages": []}

        visited.add(normalized_url)
        logger.info(
            f"🎯 Crawling page {len(visited)}/{max_pages} at depth {current_depth}: {normalized_url}"
        )
        logger.debug(
            f"📊 Current state: depth={current_depth}/{depth}, pages={len(visited)}/{max_pages}"
        )

        try:
            # Fetch the page with detailed timing
            logger.info(f"🌐 Starting fetch for: {normalized_url}")
            fetch_start = datetime.now()
            captured_blocks = await fetch_rendered_html(
                normalized_url, config=dom_config, ctx=ctx
            )
            fetch_time = (datetime.now() - fetch_start).total_seconds()
            logger.info(
                f"✅ Page fetch completed in {fetch_time:.2f}s - blocks: {len(captured_blocks) if captured_blocks else 0}"
            )

            if not captured_blocks:
                logger.warning(f"⚠️ No content blocks retrieved from {normalized_url}")
                return {"pages": []}

            # Process content with LLM
            logger.info(f"🤖 Starting LLM content processing for: {normalized_url}")
            llm_start = datetime.now()
            processed_result = await llm_content_processor(
                normalized_url, captured_blocks
            )
            llm_time = (datetime.now() - llm_start).total_seconds()
            logger.info(
                f"✅ LLM processing completed in {llm_time:.2f}s - baseball news: {len(processed_result.get('baseball_news', []))}"
            )

            page_data = {
                "url": normalized_url,
                "depth": current_depth,
                "blocks": captured_blocks,
                "processed_result": processed_result,
                "fetch_time": fetch_time,
                "llm_time": llm_time,
                "total_time": fetch_time + llm_time,
            }

            pages = [page_data]
            logger.debug(
                f"📦 Created page data for {normalized_url}: {len(captured_blocks)} blocks, {len(processed_result.get('baseball_news', []))} news items"
            )

            # Extract and filter links for next depth
            if current_depth < depth and len(visited) < max_pages:
                logger.info(
                    f"🔗 Extracting links from {normalized_url} (depth {current_depth})"
                )
                links = set()

                # Extract links from blocks
                for i, block in enumerate(captured_blocks):
                    if hasattr(block, "links") and block.links:
                        logger.debug(f"📎 Block {i} has {len(block.links)} links")
                        for link in block.links:
                            if basic_filter(normalized_url, link):
                                links.add(link)
                                logger.debug(f"✅ Link passed basic filter: {link}")
                            else:
                                logger.debug(f"❌ Link failed basic filter: {link}")

                logger.info(
                    f"📊 Found {len(links)} candidate links after basic filtering"
                )

                # Use Scout Bridge to filter links intelligently
                logger.info(
                    f"🔍 Starting Scout Bridge evaluation for {min(len(links), 10)} links"
                )
                scout_start = datetime.now()
                filtered_links = []

                for i, link in enumerate(
                    list(links)[:10], 1
                ):  # Limit to avoid too many scout calls
                    logger.debug(f"🤖 Scout evaluating link {i}/10: {link}")
                    if await scout.should_follow_link(link, "", normalized_url):
                        filtered_links.append(link)
                        logger.debug(f"✅ Scout approved link: {link}")
                    else:
                        logger.debug(f"❌ Scout rejected link: {link}")

                scout_time = (datetime.now() - scout_start).total_seconds()
                logger.info(
                    f"🎯 Scout bridge filtered {len(filtered_links)} links from {len(links)} candidates in {scout_time:.2f}s"
                )

                # Crawl filtered links
                if filtered_links:
                    logger.info(
                        f"🚀 Starting crawl of {min(len(filtered_links), 5)} filtered links"
                    )
                    for i, link in enumerate(
                        filtered_links[:5], 1
                    ):  # Limit concurrent crawls
                        if len(visited) >= max_pages:
                            logger.info(
                                f"🛑 Stopping crawl: page limit {max_pages} reached"
                            )
                            break

                        logger.info(
                            f"📖 Crawling link {i}/{min(len(filtered_links), 5)}: {link}"
                        )
                        sub_result = await smart_crawl_recursive(
                            link, current_depth + 1, visited
                        )
                        pages.extend(sub_result["pages"])
                        logger.debug(
                            f"✅ Sub-crawl completed, added {len(sub_result['pages'])} pages"
                        )
                else:
                    logger.info(f"🔚 No links to follow from {normalized_url}")
            else:
                logger.debug(
                    f"⏹️ Skipping link extraction: depth={current_depth}/{depth}, visited={len(visited)}/{max_pages}"
                )

            return {"pages": pages}

        except Exception as e:
            logger.error(f"❌ Error crawling {normalized_url}: {type(e).__name__}: {e}")
            logger.debug("🔍 Error details:", exc_info=True)
            return {"pages": []}

    def basic_filter(base_url: str, target_url: str) -> bool:
        """Basic non-LLM filters for performance"""
        return baseball_link_filter(base_url, target_url)

    # Perform the smart crawl
    crawl_result = await smart_crawl_recursive("https://www.espn.com/mlb/")

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # Analyze results
    all_pages = crawl_result["pages"]

    print(f"\n✅ Smart crawl completed in {duration:.2f} seconds")
    print(f"📄 Total pages crawled: {len(all_pages)}")

    # Aggregate all baseball news with detailed debugging
    all_baseball_news = []
    pages_with_news = 0

    logger.info(f"🔍 Analyzing results from {len(all_pages)} pages")
    for i, page in enumerate(all_pages):
        page_url = page.get("url", "unknown")
        processed = page.get("processed_result", {})
        baseball_news = processed.get("baseball_news", [])

        logger.debug(f"📄 Page {i+1}: {page_url}")
        logger.debug(f"   Processed result keys: {list(processed.keys())}")
        logger.debug(f"   Baseball news count: {len(baseball_news)}")

        if baseball_news:
            all_baseball_news.extend(baseball_news)
            pages_with_news += 1
            logger.info(
                f"✅ Page {i+1} contributed {len(baseball_news)} baseball news items"
            )
        else:
            logger.warning(f"❌ Page {i+1} had no baseball news: {page_url}")

    print(f"📰 Pages with baseball news: {pages_with_news}")
    print(f"📝 Total news paragraphs extracted: {len(all_baseball_news)}")
    logger.info(
        f"📊 Final aggregation: {len(all_baseball_news)} baseball news items from {pages_with_news} pages"
    )

    # Sort by content length (longer articles first)
    all_baseball_news.sort(key=lambda x: len(x["content"]), reverse=True)

    # Remove duplicates using content hash deduplication
    logger.info(f"🔍 Starting deduplication - input: {len(all_baseball_news)} items")
    deduplicated_news = deduplicate_news_items(all_baseball_news)
    removed_count = len(all_baseball_news) - len(deduplicated_news)
    all_baseball_news = deduplicated_news

    if removed_count > 0:
        logger.info(
            f"🧹 Removed {removed_count} duplicate items - remaining: {len(all_baseball_news)}"
        )
        print(
            f"🧹 Removed {removed_count} duplicates - {len(all_baseball_news)} unique items remaining"
        )
    else:
        logger.info(f"✅ No duplicates found - {len(all_baseball_news)} unique items")

    # Generate final summary using LLM
    logger.info("Generating final summary of all extracted baseball news")
    if all_baseball_news:
        logger.info(
            f"📝 Generating summary for {len(all_baseball_news)} baseball news items"
        )
        final_summary = await generate_final_summary(
            all_baseball_news, provider, config
        )
    else:
        logger.warning("⚠️ No baseball news found, skipping summary generation")
        final_summary = {
            "summary": "No baseball news was extracted from the crawled pages.",
            "key_topics": [],
            "total_articles": 0,
            "word_count": 0,
            "generation_method": "no_content",
        }

    # Create result summary
    result = {
        "crawl_info": {
            "start_url": "https://www.espn.com/mlb/",
            "max_depth": depth,
            "max_pages": max_pages,
            "duration_seconds": duration,
            "timestamp": datetime.now().isoformat(),
            "extraction_method": "llm_powered",
        },
        "statistics": {
            "total_pages": len(all_pages),
            "pages_with_news": pages_with_news,
            "total_news_paragraphs": len(all_baseball_news),
            "average_paragraphs_per_page": (
                len(all_baseball_news) / len(all_pages) if all_pages else 0
            ),
            "pages_by_depth": {},
        },
        "baseball_news": all_baseball_news,
        "final_summary": final_summary,
        "crawled_urls": [p["url"] for p in all_pages],
        "page_details": [],
    }

    # Add page-by-page details
    for page in all_pages:
        processed = page.get("processed_result", {})
        result["page_details"].append(
            {
                "url": page["url"],
                "depth": page["depth"],
                "news_count": len(processed.get("baseball_news", [])),
                "analysis_performed": processed.get("analysis_performed", False),
            }
        )

    # Calculate pages by depth
    for page in all_pages:
        depth_level = page["depth"]
        if depth_level not in result["statistics"]["pages_by_depth"]:
            result["statistics"]["pages_by_depth"][depth_level] = 0
        result["statistics"]["pages_by_depth"][depth_level] += 1

    return result


def create_smart_txt_report(result: dict[str, Any], output_path: str) -> None:
    """Create a formatted TXT report from smart crawl results.

    Args:
        result: The crawl result dictionary
        output_path: Path to save the TXT file
    """
    with open(output_path, "w", encoding="utf-8") as f:
        # Header
        f.write("=" * 80 + "\n")
        f.write("SMART BASEBALL NEWS EXTRACTION REPORT\n")
        f.write("=" * 80 + "\n\n")

        # Summary
        crawl_info = result["crawl_info"]
        stats = result["statistics"]

        f.write("CRAWL SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Start URL: {crawl_info['start_url']}\n")
        f.write(f"Extraction Method: {crawl_info['extraction_method']}\n")
        f.write(f"Max Depth: {crawl_info['max_depth']}\n")
        f.write(f"Max Pages: {crawl_info['max_pages']}\n")
        f.write(f"Duration: {crawl_info['duration_seconds']:.2f} seconds\n")
        f.write(f"Timestamp: {crawl_info['timestamp']}\n\n")

        f.write("STATISTICS\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total pages crawled: {stats['total_pages']}\n")
        f.write(f"Pages with news: {stats['pages_with_news']}\n")
        f.write(f"Total news paragraphs: {stats['total_news_paragraphs']}\n")
        f.write(
            f"Average paragraphs per page: {stats['average_paragraphs_per_page']:.1f}\n\n"
        )

        f.write("Pages by depth:\n")
        for depth, count in sorted(stats["pages_by_depth"].items()):
            f.write(f"  Depth {depth}: {count} pages\n")
        f.write("\n")

        # Final Summary
        if "final_summary" in result:
            summary = result["final_summary"]
            f.write("FINAL SUMMARY\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total articles analyzed: {summary.get('total_articles', 0)}\n")
            f.write(f"Total word count: {summary.get('word_count', 0)}\n")
            f.write(
                f"Generation method: {summary.get('generation_method', 'unknown')}\n\n"
            )

            f.write("Summary:\n")
            f.write(summary.get("summary", "No summary available") + "\n\n")

            if summary.get("key_topics"):
                f.write("Key Topics:\n")
                for topic in summary["key_topics"]:
                    f.write(f"  • {topic}\n")
                f.write("\n")

            if summary.get("major_players"):
                f.write("Major Players:\n")
                for player in summary["major_players"]:
                    f.write(f"  • {player}\n")
                f.write("\n")

            if summary.get("major_teams"):
                f.write("Major Teams:\n")
                for team in summary["major_teams"]:
                    f.write(f"  • {team}\n")
                f.write("\n")

            if summary.get("major_events"):
                f.write("Major Events:\n")
                for event in summary["major_events"]:
                    f.write(f"  • {event}\n")
                f.write("\n")

        # Page details
        f.write("PAGE ANALYSIS RESULTS\n")
        f.write("-" * 40 + "\n")
        for page in result["page_details"]:
            f.write(f"[Depth {page['depth']}] {page['url']}\n")
            f.write(f"  News paragraphs found: {page['news_count']}\n")
            f.write(f"  LLM analysis: {'✓' if page['analysis_performed'] else '✗'}\n\n")

        # Baseball News Content
        f.write("EXTRACTED BASEBALL NEWS\n")
        f.write("=" * 80 + "\n")

        if result["baseball_news"]:
            for i, news_item in enumerate(result["baseball_news"], 1):
                f.write(f"\n{i}. NEWS PARAGRAPH\n")
                f.write("-" * 60 + "\n")
                f.write(f"Source: {news_item['url']}\n")
                f.write(f"Length: {len(news_item['content'])} characters\n")
                f.write(f"Extraction: {news_item.get('extracted_by', 'unknown')}\n\n")

                # Format the content nicely
                content = news_item["content"]
                # Break long lines for readability
                words = content.split()
                lines = []
                current_line = ""

                for word in words:
                    if len(current_line + " " + word) <= 80:
                        current_line += (" " + word) if current_line else word
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = word

                if current_line:
                    lines.append(current_line)

                for line in lines:
                    f.write(f"  {line}\n")

                f.write("\n" + "=" * 80 + "\n")
        else:
            f.write("\nNo baseball news paragraphs were extracted.\n")


async def main():
    """Main function with CLI."""
    parser = argparse.ArgumentParser(
        description="Smart baseball news crawler with LLM-powered content extraction"
    )
    parser.add_argument(
        "-d",
        "--depth",
        type=int,
        help="Maximum crawl depth (overrides config). Default: from config",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        help="Maximum number of pages to crawl (overrides config). Default: from config",
    )
    parser.add_argument("--config", type=str, help="Path to configuration YAML file")
    parser.add_argument(
        "--json-output", type=str, help="JSON output file path (overrides config)"
    )
    parser.add_argument(
        "--txt-output", type=str, help="TXT output file path (overrides config)"
    )
    parser.add_argument("--no-json", action="store_true", help="Skip JSON output")
    parser.add_argument("--no-txt", action="store_true", help="Skip TXT output")

    args = parser.parse_args()

    # Load configuration
    try:
        if args.config:
            config = load_config(args.config)
            print(f"✅ Loaded configuration from {args.config}")
        else:
            config = load_config()  # Try default locations
            print("✅ Loaded configuration from default location")
    except FileNotFoundError as e:
        print(f"⚠️  Config file not found: {e}")
        print("Using default configuration")
        config = create_default_config()
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        print("Using default configuration")
        config = create_default_config()

    # Setup logging with config
    setup_logging(config)
    global logger
    logger = logging.getLogger(__name__)
    # Make config and logger available globally
    globals()["config"] = config

    logger.info(
        f"Starting baseball crawler with config: depth={config.crawler.max_depth}, max_pages={config.crawler.max_pages}"
    )

    try:
        # Run the smart crawler with config
        result = await crawl_baseball_news_smart(
            config=config, depth=args.depth, max_pages=args.max_pages
        )

        # Display results
        print("\n" + "=" * 60)
        print("🤖 SMART BASEBALL NEWS EXTRACTION SUMMARY")
        print("=" * 60)

        stats = result["statistics"]
        print(f"Total pages crawled: {stats['total_pages']}")
        print(f"Pages with news: {stats['pages_with_news']}")
        print(f"News paragraphs extracted: {stats['total_news_paragraphs']}")

        print("\n📈 Pages by depth:")
        for depth, count in sorted(stats["pages_by_depth"].items()):
            print(f"  Depth {depth}: {count} pages")

        print("\n🔗 Page analysis results:")
        for page in result["page_details"]:
            print(
                f"  [{page['depth']}] {page['url']} - {page['news_count']} paragraphs"
            )

        if result["baseball_news"]:
            print("\n📰 Sample news paragraphs:")
            for i, news in enumerate(result["baseball_news"][:3], 1):
                preview = (
                    news["content"][:150] + "..."
                    if len(news["content"]) > 150
                    else news["content"]
                )
                print(f"\n{i}. [{len(news['content'])} chars] {preview}")
                print(f"   From: {news['url']}")

        # Display final summary
        if "final_summary" in result:
            summary = result["final_summary"]
            print("\n🎯 FINAL SUMMARY")
            print("=" * 60)
            print(f"Articles analyzed: {summary.get('total_articles', 0)}")
            print(f"Total words: {summary.get('word_count', 0)}")
            if summary.get("key_topics"):
                print(f"Key topics: {', '.join(summary['key_topics'][:5])}")
            print(
                f"\nSummary: {summary.get('summary', 'No summary available')[:200]}..."
            )
            logger.info("Final summary displayed to user")

        # Save results
        os.makedirs("output", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save JSON output
        if not args.no_json:
            json_path = (
                args.json_output or f"output/smart_baseball_news_{timestamp}.json"
            )
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\n💾 JSON results saved to: {json_path}")

        # Save TXT output
        if not args.no_txt:
            txt_path = args.txt_output or f"output/smart_baseball_news_{timestamp}.txt"
            create_smart_txt_report(result, txt_path)
            print(f"📄 TXT report saved to: {txt_path}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
