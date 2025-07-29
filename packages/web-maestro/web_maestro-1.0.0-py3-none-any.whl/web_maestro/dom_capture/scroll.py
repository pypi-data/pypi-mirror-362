"""Module for handling scrolling operations in a web page using Playwright."""

import asyncio
import hashlib
import logging

from playwright.async_api import Page

from ..core.context import SessionContext

logger = logging.getLogger(__name__)


async def scroll_until_stable(
    page: Page, max_scrolls: int = 15, ctx: SessionContext | None = None
) -> None:
    """Scrolls the page downward until either the scroll height or DOM hash becomes stable.

    This function continues to scroll the page downward until the scroll height or DOM
    hash is stable for at least 3 consecutive attempts or until the maximum number of
    scrolls is reached.

    Args:
        page (Page): The Playwright page object.
        max_scrolls (int): Maximum number of scroll rounds before stopping.
        ctx (Optional[SessionContext]): Context for teardown safety.
    """
    if ctx and ctx.cleanup_started:
        logger.debug("⚠️ Skipping scroll — cleanup started")
        return
    if page.is_closed():
        logger.debug("⚠️ Skipping scroll — page is closed")
        return

    try:
        last_height = await asyncio.wait_for(
            page.evaluate("() => document?.body?.scrollHeight ?? 0"), timeout=2
        )
        last_html = await asyncio.wait_for(page.content(), timeout=2)
        last_hash = hashlib.sha256(last_html.encode("utf-8")).hexdigest()

    except Exception as e:
        logger.warning(f"⚠️ Failed to get initial scroll state: {e}")
        return

    height_stable_count = 0
    hash_stable_count = 0
    scroll_count = 0

    while (
        scroll_count < max_scrolls and max(height_stable_count, hash_stable_count) < 3
    ):
        if (ctx and ctx.cleanup_started) or page.is_closed():
            logger.debug("🛑 Exiting scroll loop — teardown or closed")
            return

        try:
            await page.mouse.wheel(0, 1000)
            await asyncio.sleep(0.3)

            new_height = await asyncio.wait_for(
                page.evaluate("() => document?.body?.scrollHeight ?? 0"), timeout=2
            )
            new_html = await asyncio.wait_for(page.content(), timeout=2)
            new_hash = hashlib.sha256(new_html.encode("utf-8")).hexdigest()

            # Track scroll height stability
            if new_height == last_height:
                height_stable_count += 1
                logger.debug(
                    f"📏 Scroll height stable at {new_height} ({height_stable_count}/3)"
                )
            else:
                height_stable_count = 0
                last_height = new_height
                logger.debug(f"📏 Scroll height changed → {new_height}")

            # Track DOM content stability via hash
            if new_hash == last_hash:
                hash_stable_count += 1
                logger.debug(f"🔁 DOM hash stable ({hash_stable_count}/3)")
            else:
                hash_stable_count = 0
                last_hash = new_hash
                logger.debug("🔁 DOM hash changed")

            scroll_count += 1

        except asyncio.CancelledError:
            logger.warning("⚠️ Scroll cancelled mid-execution")
            return
        except Exception as e:
            logger.warning(f"⚠️ Scroll error on attempt {scroll_count}: {e}")
            return

    if height_stable_count >= 3:
        logger.info(f"✅ Scrolling stabilized by height after {scroll_count} scrolls")
    elif hash_stable_count >= 3:
        logger.info(f"✅ Scrolling stabilized by DOM hash after {scroll_count} scrolls")
    else:
        logger.info(
            f"⏱️ Max scrolls reached ({max_scrolls}), content may still be loading"
        )
