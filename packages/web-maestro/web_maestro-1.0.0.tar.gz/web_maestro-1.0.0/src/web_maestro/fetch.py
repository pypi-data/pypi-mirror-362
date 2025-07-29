"""Main fetch functionality for web_maestro.

This module provides the main entry point for fetching and extracting
content from web pages using Playwright with AI Scout capabilities.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from playwright.async_api import async_playwright

from .capture import capture_dom_stages_universal
from .context import SessionContext
from .models.types import CapturedBlock

logger = logging.getLogger(__name__)


async def fetch_rendered_html(
    url: str,
    ctx: SessionContext | None = None,
    config: dict[str, Any] | None = None,
    ai_navigation_bridge=None,  # Legacy parameter for compatibility
    ai_scout_bridge=None,  # New parameter name
) -> list[CapturedBlock] | None:
    """Fetch HTML using Playwright with optional AI-guided navigation.

    Args:
        url: Target URL to render
        ctx: Session context
        config: Configuration dict
        ai_navigation_bridge: Legacy parameter (use ai_scout_bridge)
        ai_scout_bridge: Optional AI scout bridge for smart interactions

    Returns:
        List of captured blocks or None on failure
    """
    # Handle legacy parameter
    if ai_navigation_bridge and not ai_scout_bridge:
        ai_scout_bridge = ai_navigation_bridge

    if ctx is None:
        ctx = SessionContext()

    config = config or {}
    trace_id = getattr(ctx, "trace_id", None) or str(asyncio.current_task().get_name())
    trace = f"[trace={trace_id}] " if trace_id else ""

    logger.info(f"{trace}🚀 Starting WebMaestro rendering for: {url}")
    logger.debug(f"{trace}📋 Config: {config}")
    logger.debug(
        f"{trace}🔧 Context: trace_id={trace_id}, has_ai_scout={ai_scout_bridge is not None}"
    )

    async with async_playwright() as p:
        browser = None
        try:
            # Launch browser
            launch_options = {
                "headless": config.get("headless", True),
                "args": [
                    "--disable-gpu",
                    "--disable-dev-shm-usage",
                    "--disable-setuid-sandbox",
                    "--no-sandbox",
                ],
            }
            logger.debug(
                f"{trace}🌐 Launching Chromium browser with options: {launch_options}"
            )
            browser = await p.chromium.launch(**launch_options)
            logger.info(f"{trace}✅ Browser launched successfully")

            # Create context with viewport
            viewport = config.get("viewport", {"width": 1920, "height": 1080})
            user_agent = config.get(
                "user_agent",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            )
            logger.debug(
                f"{trace}📱 Creating browser context - viewport: {viewport}, user_agent: {user_agent[:50]}..."
            )
            context = await browser.new_context(
                viewport=viewport,
                user_agent=user_agent,
            )
            logger.info(f"{trace}🎭 Browser context created")

            # Create page
            logger.debug(f"{trace}📄 Creating new page")
            page = await context.new_page()
            logger.info(f"{trace}✅ Page created")

            # Set up request blocking if configured
            if config.get("block_resources", False):
                blocked_types = config.get(
                    "blocked_resource_types", ["image", "media", "font"]
                )
                logger.info(
                    f"{trace}🚫 Setting up resource blocking for: {blocked_types}"
                )
                await page.route(
                    "**/*",
                    lambda route: (
                        route.abort()
                        if route.request.resource_type in blocked_types
                        else route.continue_()
                    ),
                )
                logger.debug(f"{trace}✅ Resource blocking configured")

            # Navigate to URL
            logger.info(f"{trace}📍 Navigating to: {url}")
            timeout = config.get("page_timeout", 30000)
            logger.debug(f"{trace}⏱️ Page timeout set to: {timeout}ms")

            start_nav = asyncio.get_event_loop().time()
            await page.goto(url, wait_until="domcontentloaded", timeout=timeout)
            nav_time = (asyncio.get_event_loop().time() - start_nav) * 1000
            logger.info(f"{trace}✅ Navigation completed in {nav_time:.0f}ms")

            # Wait for initial content
            initial_wait = config.get("initial_wait", 2000)
            logger.debug(f"{trace}⏳ Waiting {initial_wait}ms for initial content")
            await page.wait_for_timeout(initial_wait)
            logger.debug(f"{trace}✅ Initial wait completed")

            # Capture DOM content using the universal capture function
            logger.info(f"{trace}🔍 Starting DOM capture")
            capture_start = asyncio.get_event_loop().time()
            capture_config = {
                "scroll": config.get("scroll", True),
                "debug_screenshot_path": config.get("debug_screenshot_path"),
            }
            logger.debug(f"{trace}⚙️ DOM capture config: {capture_config}")

            captured_blocks = await capture_dom_stages_universal(
                page=page,
                scroll=capture_config["scroll"],
                debug_screenshot_path=capture_config["debug_screenshot_path"],
                ctx=ctx,
                config=config,
            )

            capture_time = (asyncio.get_event_loop().time() - capture_start) * 1000
            logger.info(f"{trace}⏱️ DOM capture completed in {capture_time:.0f}ms")

            # Log results with detailed breakdown
            if captured_blocks:
                block_types = {}
                total_content_length = 0
                for block in captured_blocks:
                    block_type = getattr(block, "capture_type", "unknown")
                    block_types[block_type] = block_types.get(block_type, 0) + 1
                    if hasattr(block, "content"):
                        total_content_length += len(str(block.content))

                logger.info(f"{trace}✅ Captured {len(captured_blocks)} content blocks")
                logger.debug(f"{trace}📊 Block types: {block_types}")
                logger.debug(
                    f"{trace}📝 Total content length: {total_content_length} chars"
                )
            else:
                logger.warning(f"{trace}⚠️ No content blocks captured")

            return captured_blocks

        except asyncio.CancelledError:
            logger.info(f"{trace}🛑 Fetch cancelled")
            raise
        except Exception as e:
            logger.error(f"{trace}❌ Error during fetch: {type(e).__name__}: {e}")

            # Take screenshot on error if configured
            if config.get("screenshot_on_error") and page:
                try:
                    screenshot_path = f"error_{trace_id}.png"
                    await page.screenshot(path=screenshot_path)
                    logger.info(
                        f"{trace}📸 Error screenshot saved to {screenshot_path}"
                    )
                except Exception as screenshot_error:
                    logger.warning(
                        f"{trace}⚠️ Failed to capture error screenshot: {screenshot_error}"
                    )

            return None

        finally:
            # Cleanup
            if browser:
                try:
                    await browser.close()
                except Exception as e:
                    logger.warning(f"{trace}⚠️ Error closing browser: {e}")


# Legacy alias for backward compatibility
fetch_rendered_html_v3 = fetch_rendered_html
