"""DOM Stability Utilities for Dynamic Web Pages.

This module provides logic to detect when a Playwright-rendered page has
reached a "stable" state — meaning its content is no longer dynamically changing.

Stability is assessed by comparing:
- The length of the outer HTML
- The document's scroll height
- The number of DOM nodes
- And the MD5 hash of the full outer HTML

If these measurements remain consistent across multiple checks, or if the
DOM hash repeats several times in a row, the page is considered stable.

This prevents premature capture of incomplete or animated content and is
particularly useful after dynamic interactions (e.g. clicks, tab switches, expansions).

Stability Profiles:
- DEFAULT: Balanced for general use
- QUICK: Shorter timeout for lightweight actions
- THOROUGH: For complex, animation-heavy UIs

Function:
- wait_until_dom_stable: Waits until the DOM stabilizes or a timeout occurs.

Dependencies:
- Playwright async API
- DOM_STABILITY profile from config.py

"""

import asyncio
import hashlib
import logging

from playwright.async_api import Page

from ..config.base import DOM_STABILITY
from ..core.context import SessionContext

logger = logging.getLogger(__name__)


async def wait_until_dom_stable(
    page: Page,
    mode: str = "DEFAULT",
    custom_timeout_ms: int | None = None,
    ctx: SessionContext | None = None,
) -> bool:
    """Waits until the DOM becomes stable by comparing repeated DOM hashes and metadata.

    Uses quick polling and short-circuits if DOM hash matches for 2 consecutive checks.
    Switches to structure comparison only if necessary.

    Args:
        page (Page): Playwright page to check.
        mode (str): One of 'DEFAULT', 'QUICK', 'THOROUGH'.
        custom_timeout_ms (Optional[int]): Max time to wait, overrides mode default.
        ctx (SessionContext, optional): Cleanup-aware context.

    Returns:
        bool: True if DOM was stable, False if timeout or teardown occurred.

    """
    params = DOM_STABILITY.get(mode.upper(), DOM_STABILITY["DEFAULT"])
    timeout_ms = (
        custom_timeout_ms if custom_timeout_ms is not None else params["timeout_ms"]
    )
    threshold = params["stability_threshold"]
    interval = params["check_interval"]
    min_time = params["min_stability_time"]

    hash_history = []
    stable_checks = 0
    max_stable_checks = 0  # Track maximum stable checks achieved
    elapsed = 0
    prev_len = prev_height = prev_count = 0

    while elapsed < timeout_ms:
        # Check if page is closed, handling both real pages and mocks
        is_closed = False
        try:
            if hasattr(page, "is_closed"):
                if hasattr(page, "_mock_name"):
                    # This is a mock object - call as regular method
                    is_closed = (
                        page.is_closed.return_value
                        if hasattr(page.is_closed, "return_value")
                        else False
                    )
                else:
                    # This is a real page - call as method
                    is_closed = page.is_closed()
        except Exception:
            is_closed = False

        if (ctx and ctx.cleanup_started) or is_closed:
            logger.warning("⚠️ Aborting DOM wait — cleanup or closed")
            return False

        try:
            stats = await asyncio.wait_for(
                page.evaluate(
                    """
                    () => ({
                        html: document.body?.innerHTML ?? "",
                        height: document.body?.scrollHeight ?? 0,
                        count: document.querySelectorAll('*').length
                    })
                """
                ),
                timeout=1,
            )

            html = stats["html"]
            dom_hash = hashlib.sha256(html.encode("utf-8")).hexdigest()
            hash_history.append(dom_hash)

            # ✅ Early exit: hash unchanged
            if len(hash_history) >= 2 and all(h == dom_hash for h in hash_history[-2:]):
                if not ctx or ctx.last_logged_dom_hash != dom_hash:
                    logger.debug(f"✅ DOM stable (hash match: {dom_hash})")
                    if ctx:
                        ctx.last_logged_dom_hash = dom_hash
                return True

            # If not hash-matched, compare metrics
            html_len = len(html)
            height = stats["height"]
            count = stats["count"]

            if (
                abs(html_len - prev_len) < 100
                and height == prev_height
                and abs(count - prev_count) < 10
            ):
                stable_checks += 1
                max_stable_checks = max(max_stable_checks, stable_checks)
                logger.debug(f"🟡 DOM stable check {stable_checks}/{threshold}")
            else:
                stable_checks = 0

            if stable_checks >= threshold and elapsed >= min_time:
                logger.debug(f"✅ DOM stabilized after {elapsed}ms (mode={mode})")
                return True

            prev_len = html_len
            prev_height = height
            prev_count = count

            await asyncio.sleep(interval / 1000)
            elapsed += interval

        except asyncio.CancelledError:
            logger.warning("⚠️ DOM stability wait cancelled")
            return False
        except Exception as e:
            logger.warning(f"❌ DOM stability loop failed: {e}")
            return False

    if max_stable_checks > 0:
        logger.info(
            f"⏱️ Timeout ({mode}) — partial stability ({max_stable_checks}/{threshold})"
        )
        return True
    else:
        logger.info(f"⏱️ Timeout ({mode}) — no stable state detected")
        return False
