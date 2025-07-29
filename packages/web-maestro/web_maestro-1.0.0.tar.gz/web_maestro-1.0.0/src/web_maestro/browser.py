"""Browser Setup and Teardown Utilities for Playwright Crawling.

This module defines:
- `_setup_playwright_browser`: Launches Playwright, configures the browser context,
  sets up resource blocking, and returns the fully initialized page object.

- `_finalize_and_cleanup`: Cancels any fire-and-forget tasks, closes all pages and contexts,
  tears down the browser instance, and optionally deletes a trace file.

- `playwright_session`: Context manager for safe Playwright session management.

These functions are intended for use in structured HTML rendering and crawling workflows.
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
import logging
import os

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)

from .context import SessionContext
from .models.types import BrowserConfig
from .trace_utils import _handle_console_message

logger = logging.getLogger(__name__)


async def _setup_playwright_browser(
    ctx: SessionContext,
    enable_tracing: bool = False,
) -> tuple[
    Playwright | None,
    Browser | None,
    BrowserContext | None,
    Page | None,
    str | None,  # trace_path
]:
    """Launches a Chromium browser and prepares a Playwright context for crawling.

    Includes:
    - JS enabled, CSP bypassed
    - Resource blocking
    - Navigation protection and console logging.
    - Optional tracing

    Args:
        ctx (SessionContext): The session context.
        enable_tracing (bool): Whether to enable Playwright tracing.

    Returns:
        Tuple[Optional[Playwright], Optional[Browser], Optional[BrowserContext], Optional[Page], Optional[str]]:
        A tuple containing the Playwright instance, Browser instance, Browser Context, Page instance, and trace path.
        Returns all None on failure/cleanup.
    """
    if ctx.cleanup_started:
        logger.warning("🛑 Aborting browser setup — cleanup has already started")
        return None, None, None, None, None

    trace_path = None

    try:
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(
            headless=True,
            args=[
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-web-security",
                "--disable-features=IsolateOrigins,site-per-process",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-tools",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-translate",
                "--disable-extensions",
                "--disable-background-timer-throttling",
                "--disable-renderer-backgrounding",
                "--disable-features=TranslateUI",
                "--disable-ipc-flooding-protection",
            ],
        )
        context = await browser.new_context(
            viewport={"width": 1920, "height": 3000},
            java_script_enabled=True,
            bypass_csp=True,
        )

        # Start tracing if enabled
        if enable_tracing:
            trace_path = f"trace_{id(context)}.zip"
            await context.tracing.start(screenshots=True, snapshots=True, sources=True)

        await _add_resource_blocking_routes(context)

        page = await context.new_page()

        await page.add_init_script(
            """
            // Prevent all <a> navigation (internal or external)
            document.addEventListener('click', function(e) {
                const a = e.target.closest('a');
                if (a && a.href) {
                    e.preventDefault();
                    e.stopPropagation();
                }
            }, true);

            // Block popups
            window.alert = function() {};
            window.confirm = function() { return true; };
            window.open = function() { return null; };

            // Optional: prevent window.location redirects
            Object.defineProperty(window, 'location', {
                value: Object.freeze({
                    ...window.location,
                    assign: function() {},
                    replace: function() {},
                    reload: function() {},
                }),
                writable: false
            });
            """
        )

        page.on("console", lambda msg: _handle_console_message(msg))

        return playwright, browser, context, page, trace_path

    except Exception as err:
        logger.error(f"❌ Failed to setup Playwright browser: {err}")
        raise RuntimeError("Failed to setup Playwright browser") from err


async def _cancel_all_pending_tasks(ctx: SessionContext) -> None:
    """Cancel all background tasks and any other pending asyncio tasks.

    This includes both tracked background tasks and Playwright's internal tasks
    that might still be running.

    Args:
        ctx (SessionContext): The session context containing tracked background tasks.
    """
    # Cancel tracked background tasks
    if ctx.background_tasks:
        logger.info(f"🛑 Cancelling {len(ctx.background_tasks)} background tasks")
        for task in ctx.background_tasks:
            if not task.done():
                try:
                    task.cancel()
                except Exception as e:
                    logger.debug(f"Error cancelling background task: {e}")

    # Also cancel any other pending tasks (like Playwright's internal ones)
    current_task = asyncio.current_task()
    all_tasks = [
        task for task in asyncio.all_tasks() if not task.done() and task != current_task
    ]

    if all_tasks:
        logger.debug(f"🛑 Cancelling {len(all_tasks)} additional pending tasks")
        for task in all_tasks:
            try:
                task.cancel()
            except Exception as e:
                logger.debug(
                    f"Failed to cancel task: {e}"
                )  # Ignore cancellation errors

    # Wait for all tasks to complete/cancel
    tasks_to_wait = list(ctx.background_tasks) + all_tasks
    if tasks_to_wait:
        try:
            # Use shield to prevent recursive cancellation
            await asyncio.wait_for(
                asyncio.shield(asyncio.gather(*tasks_to_wait, return_exceptions=True)),
                timeout=1.0,
            )
        except asyncio.TimeoutError:
            logger.debug("⏱️ Some tasks didn't cancel within timeout — continuing")
        except asyncio.CancelledError:
            logger.debug("⚠️ Cancellation during task cleanup — continuing")
        except Exception as e:
            logger.debug(f"⚠️ Error during task cancellation: {e}")

    ctx.background_tasks.clear()


async def _safe_stop_tracing(context: BrowserContext, trace_path: str) -> None:
    """Safely stop tracing and save to file.

    Args:
        context (BrowserContext): The browser context with active tracing.
        trace_path (str): Path where to save the trace file.
    """
    try:
        await asyncio.wait_for(context.tracing.stop(path=trace_path), timeout=5.0)
        logger.debug(f"✅ Trace saved to: {trace_path}")
    except asyncio.TimeoutError:
        logger.warning(f"⏱️ Tracing stop timed out for: {trace_path}")
    except Exception as e:
        logger.debug(f"⚠️ Failed to stop tracing: {e}")


async def _safe_delete_trace_file(trace_path: str, max_retries: int = 3) -> None:
    """Safely delete trace file with retries.

    Args:
        trace_path (str): Path to the trace file to delete.
        max_retries (int): Maximum number of deletion attempts.
    """
    if not trace_path or not os.path.exists(trace_path):
        return

    for attempt in range(max_retries):
        try:
            # Small delay to ensure file is not being written to
            if attempt > 0:
                await asyncio.sleep(0.1 * attempt)

            os.remove(trace_path)
            logger.debug(f"🗑️ Deleted trace file: {trace_path}")
            return
        except (OSError, PermissionError) as e:
            if attempt == max_retries - 1:
                logger.warning(
                    f"⚠️ Failed to delete trace file after {max_retries} attempts: {trace_path} - {e}"
                )
            else:
                logger.debug(
                    f"⚠️ Attempt {attempt + 1} to delete trace file failed: {e}"
                )
        except Exception as e:
            logger.debug(f"⚠️ Unexpected error deleting trace file: {trace_path} - {e}")
            break


async def _finalize_and_cleanup(
    playwright: Playwright | None,
    browser: Browser | None,
    context: BrowserContext | None,
    trace_path: str | None,
    ctx: SessionContext,
) -> None:
    """Cleans up all Playwright resources after a crawl session.

    Cancels tasks, closes all pages and contexts, and removes any trace.
    Follows proper cleanup order: tasks → tracing → pages → context → browser → playwright → trace file.

    Args:
        playwright (Optional[Playwright]): The Playwright instance.
        browser (Optional[Browser]): The browser instance.
        context (Optional[BrowserContext]): The browser context.
        trace_path (Optional[str]): File path for the trace file.
        ctx (SessionContext): The session context.
    """
    logger.info("🧹 Starting cleanup...")
    ctx.cleanup_started = True

    # Step 1: Cancel all pending tasks (most important for preventing TargetClosedError)
    try:
        await _cancel_all_pending_tasks(ctx)
    except Exception as e:
        logger.debug(f"⚠️ Error during task cancellation: {e}")

    # Step 2: Stop tracing if active
    if context and trace_path:
        try:
            await _safe_stop_tracing(context, trace_path)
        except Exception as e:
            logger.debug(f"⚠️ Error stopping tracing: {e}")

    # Step 3: Close pages and context
    if context:
        try:
            # Close all pages first
            pages = context.pages.copy()  # Create a copy to avoid iteration issues
            for page in pages:
                try:
                    if not page.is_closed():
                        await asyncio.wait_for(page.close(), timeout=1)
                except Exception as e:
                    logger.debug(f"⚠️ Failed to close page: {e}")

            # Then close the context
            await asyncio.wait_for(context.close(), timeout=2)
            logger.debug("✅ Context closed")
        except Exception as e:
            logger.debug(f"⚠️ Context close failed: {e}", exc_info=True)

    # Step 4: Close browser
    if browser:
        try:
            if browser.is_connected():
                await asyncio.wait_for(browser.close(), timeout=2)
            logger.debug("✅ Browser closed")
        except Exception as e:
            logger.debug(f"⚠️ Browser close failed: {e}", exc_info=True)

    # Step 5: Stop Playwright instance (crucial for preventing TargetClosedError)
    if playwright:
        try:
            await asyncio.wait_for(playwright.stop(), timeout=2)
            logger.debug("✅ Playwright stopped")
        except Exception as e:
            logger.debug(f"⚠️ Playwright stop failed: {e}", exc_info=True)

    # Step 6: Clean up trace file (after everything is closed)
    if trace_path:
        try:
            await _safe_delete_trace_file(trace_path)
        except Exception as e:
            logger.debug(f"⚠️ Error during trace file cleanup: {e}")

    logger.info("🧹 Cleanup completed")


@asynccontextmanager
async def playwright_session(ctx: SessionContext, enable_tracing: bool = False):
    """Context manager for safe Playwright session management.

    Automatically handles setup and cleanup of Playwright resources.
    Ensures proper cleanup even if exceptions occur.

    Args:
        ctx (SessionContext): The session context.
        enable_tracing (bool): Whether to enable Playwright tracing for debugging.

    Yields:
        Tuple[Optional[Playwright], Optional[Browser], Optional[BrowserContext], Optional[Page]]:
        The initialized Playwright resources.

    Example:
        async with playwright_session(ctx) as (playwright, browser, context, page):
            if page:
                await page.goto("https://example.com")
                # Your scraping logic here
            # Automatic cleanup happens here

        # For debugging with traces:
        async with playwright_session(ctx, enable_tracing=True) as (playwright, browser, context, page):
            # Trace will be saved and cleaned up automatically
    """
    playwright, browser, context, page, trace_path = None, None, None, None, None

    try:
        (
            playwright,
            browser,
            context,
            page,
            trace_path,
        ) = await _setup_playwright_browser(ctx, enable_tracing)
        yield playwright, browser, context, page
    except Exception as e:
        logger.error(f"❌ Error in Playwright session: {e}")
        raise
    finally:
        await _finalize_and_cleanup(playwright, browser, context, trace_path, ctx)


async def _add_resource_blocking_routes(
    context: BrowserContext, aggressive: bool = False
) -> None:
    """Adds route handlers to block non-essential resources (images, fonts, tracking).

    Args:
        context (BrowserContext): The browser context.
        aggressive (bool): If True, blocks more resource types for faster loading.
    """
    # Block images and media files
    await context.route(
        "**/*.{png,jpg,jpeg,gif,webp,svg,ico}", lambda route: route.abort()
    )

    # Block fonts
    await context.route("**/*.{woff,woff2,ttf,otf,eot}", lambda route: route.abort())

    # Block analytics and tracking
    await context.route(
        "**/{analytics,ga,gtm,hotjar,tracking,pixel}*", lambda route: route.abort()
    )

    # Block ads
    await context.route("**/ads/**", lambda route: route.abort())

    if aggressive:
        # Block CSS files for validation mode
        await context.route("**/*.css", lambda route: route.abort())

        # Block videos
        await context.route("**/*.{mp4,webm,ogg,mov,avi}", lambda route: route.abort())

        # Block social media embeds
        await context.route(
            "**/{facebook,twitter,instagram,tiktok}**", lambda route: route.abort()
        )

        # Block third-party scripts except essentials
        await context.route(
            lambda url: url.startswith(
                ("https://cdn.", "https://cdnjs.", "https://unpkg.")
            )
            and url.endswith(".js"),
            lambda route: route.abort(),
        )

    # Block video and audio files
    await context.route(
        "**/*.{mp4,webm,ogg,avi,mov,mp3,wav,aac}", lambda route: route.abort()
    )

    # Block social media widgets
    await context.route(
        "**/{facebook,twitter,linkedin,instagram}*", lambda route: route.abort()
    )


async def setup_browser(
    config: BrowserConfig | None = None,
    ctx: SessionContext | None = None,
    enable_tracing: bool = False,
) -> tuple[
    Playwright | None, Browser | None, BrowserContext | None, Page | None, str | None
]:
    """Setup a browser with the given configuration.

    Public wrapper around _setup_playwright_browser for API compatibility.

    Args:
        config: Browser configuration (unused in current implementation)
        ctx: Session context
        enable_tracing: Whether to enable tracing

    Returns:
        Tuple of (playwright, browser, context, page, trace_path)
    """
    from .core.context import create_session_context

    if ctx is None:
        ctx = create_session_context()

    return await _setup_playwright_browser(ctx, enable_tracing)


async def create_browser_context(
    config: BrowserConfig | None = None,
    browser: Browser | None = None,
) -> BrowserContext:
    """Create a browser context with the given configuration.

    Args:
        config: Browser configuration
        browser: Browser instance (if None, creates a new browser)

    Returns:
        BrowserContext instance
    """
    if config is None:
        config = BrowserConfig()

    if browser is None:
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(
            headless=config.headless,
            args=[
                *config.extra_args,
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-web-security",
                "--disable-features=IsolateOrigins,site-per-process",
                "--disable-blink-features=AutomationControlled",
            ],
        )

    context = await browser.new_context(
        viewport=config.viewport,
        user_agent=config.user_agent,
        locale=config.locale,
        timezone_id=config.timezone,
        permissions=config.permissions,
        ignore_https_errors=config.ignore_https_errors,
        bypass_csp=config.bypass_csp,
        java_script_enabled=True,
    )

    return context
