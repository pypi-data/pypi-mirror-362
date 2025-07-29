"""Tab Expansion and Capture for Tabbed Interfaces.

This module provides utilities to identify and interact with tab-like elements
on a page, such as category tabs in menus or product groups. It safely clicks
each visible tab, waits for DOM stabilization, and captures resulting HTML
snapshots.

Features:
- Filters only visible and enabled tab elements.
- Sorts tabs in top-to-bottom, left-to-right visual order.
- Clicks tabs using safe, teardown-aware logic.
- Waits for DOM stability after each interaction.
- Skips duplicate DOM captures using MD5 hashing.

Function:
- expand_tabs_and_capture: Clicks and captures content from all valid tabs.
"""

import hashlib
import logging

from playwright.async_api import ElementHandle, Page

from ..config.base import FAST_CONFIG, FOCUSED_TAB_SELECTOR, TAB_SELECTOR
from ..core.context import SessionContext
from .click_strategies import safe_click
from .stability import wait_until_dom_stable

logger = logging.getLogger(__name__)


async def expand_tabs_and_capture(
    page: Page,
    max_tabs: int = FAST_CONFIG["max_tabs"],
    tab_timeout: int = FAST_CONFIG["tab_timeout"],
    ctx: SessionContext | None = None,
    priority_keywords: list[str] | None = None,
    custom_tab_selector: str | None = None,
) -> list[str]:
    """Sequentially clicks through visible tab-like elements on the page and captures.

    The resulting DOM state is captured after each click, deduplicating the results.

    Args:
        page (Page): Playwright page instance.
        max_tabs (int): Maximum number of tabs to expand (default: 10).
        tab_timeout (int): Timeout per tab interaction in milliseconds.
        ctx (Optional[SessionContext]): Session context for teardown safety and logging.
        priority_keywords (Optional[List[str]]): Keywords to prioritize when selecting tabs.
        custom_tab_selector (Optional[str]): Custom CSS selector for finding tabs.

    Returns:
        List[str]: A list of unique HTML snapshots for each tab.
    """
    # Rest of the function remains the same...
    if (ctx and ctx.cleanup_started) or page.is_closed():
        return []

    html_blocks: list[str] = []
    seen_hashes: set[str] = set()

    try:
        tab_entries = await get_sorted_tab_elements(
            page, ctx, priority_keywords, custom_tab_selector
        )
        logger.info(f"📂 Found {len(tab_entries)} tab candidates.")

        for idx, (tab, _x, _y) in enumerate(tab_entries[:max_tabs]):
            if (ctx and ctx.cleanup_started) or page.is_closed():
                break

            label = await _get_tab_label(tab, idx)
            success = await _click_tab(tab, label, ctx=ctx, timeout_ms=tab_timeout)

            if not success:
                continue

            try:
                html = await page.content()
                h = hashlib.sha256(html.encode("utf-8")).hexdigest()
                if h not in seen_hashes:
                    seen_hashes.add(h)
                    html_blocks.append(f"<!-- TAB {idx}: {label} -->\n{html}")
                else:
                    logger.debug(f"🔁 Skipped duplicate DOM after tab '{label}'.")
            except Exception as error:
                logger.warning(
                    f"⚠️ Failed to capture DOM after tab '{label}': {error}",
                    exc_info=True,
                )

        logger.info(
            f"✅ Finished tab expansion — {len(html_blocks)} unique states captured."
        )
        return html_blocks

    except Exception as error:
        logger.warning(
            f"⚠️ expand_tabs_and_capture failed: {error}",
            exc_info=True,
        )
        raise RuntimeError("Expansion and capture process failed.") from error


async def get_sorted_tab_elements(
    page: Page,
    ctx: SessionContext | None = None,
    priority_keywords: list[str] | None = None,
    custom_tab_selector: str | None = None,
) -> list[tuple[ElementHandle, float, float]]:
    """Finds all valid tabs, optionally prioritizes by keywords, then sorts visually.

    Args:
        page (Page): The Playwright page.
        ctx (Optional[SessionContext]): Optional session context for teardown safety.
        priority_keywords (Optional[List[str]]): Keywords to prioritize tabs. If None, no prioritization.
        custom_tab_selector (Optional[str]): Custom CSS selector for tabs. If None, uses default.

    Returns:
        List[Tuple[ElementHandle, float, float]]: Tab handles with their screen positions.
    """
    try:
        # Use custom selector if provided, otherwise use generic selectors
        if custom_tab_selector:
            all_tab_selectors = custom_tab_selector
        else:
            from ..config.base import GENERIC_TAB_SELECTOR

            all_tab_selectors = (
                GENERIC_TAB_SELECTOR + ", " + TAB_SELECTOR + ", " + FOCUSED_TAB_SELECTOR
            )
        raw_tabs = await page.query_selector_all(all_tab_selectors)
    except Exception as e:
        logger.warning(f"Failed to query tab elements: {e}")
        return []

    priority_tabs: list[tuple[ElementHandle, float, float, str]] = []
    regular_tabs: list[tuple[ElementHandle, float, float, str]] = []

    for tab in raw_tabs:
        try:
            if (ctx and ctx.cleanup_started) or page.is_closed():
                break

            box = await tab.bounding_box()
            if not box or box["width"] < 1 or box["height"] < 1:
                continue

            # Get tab text for prioritization
            try:
                text = await tab.inner_text()
                text_lower = text.strip().lower()
            except Exception:
                text_lower = ""

            x, y = round(box["x"], 1), round(box["y"], 1)
            tab_info = (tab, x, y, text_lower)

            # Prioritize tabs if keywords are provided
            if priority_keywords and any(
                keyword.lower() in text_lower for keyword in priority_keywords
            ):
                priority_tabs.append(tab_info)
            else:
                regular_tabs.append(tab_info)

        except Exception as e:
            logger.debug(f"Failed to process tab element: {e}")
            continue

    # Sort priority tabs by position (top-down, left-right)
    priority_tabs.sort(key=lambda t: (t[2], t[1]))

    # Sort regular tabs by position
    regular_tabs.sort(key=lambda t: (t[2], t[1]))

    # Combine: priority tabs first, then regular tabs
    # Remove the text field from the tuple before returning
    combined_tabs = [(tab, x, y) for tab, x, y, _ in priority_tabs + regular_tabs]

    logger.info(
        f"📂 Found {len(priority_tabs)} priority tabs, {len(regular_tabs)} regular tabs"
    )

    return combined_tabs


async def _click_tab(
    tab: ElementHandle,
    label: str,
    ctx: SessionContext | None = None,
    timeout_ms: int = FAST_CONFIG["tab_timeout"],
) -> bool:
    """Clicks a tab element safely and waits for the DOM to stabilize after interaction.

    This function avoids Playwright internal access and uses public APIs
    to scroll into view, verify DOM connection, perform safe interaction,
    and detect DOM stabilization.

    Args:
        tab (ElementHandle): The tab element to click.
        label (str): A descriptive label for logging.
        ctx (Optional[SessionContext]): Optional session context for teardown safety.
        timeout_ms (int): Timeout for click plus settle phase in milliseconds.

    Returns:
        bool: True if click succeeded and DOM stabilized; False otherwise.
    """
    logger.info(f"🌀 Clicking tab: {label}")

    if ctx and ctx.cleanup_started:
        return False

    try:
        is_connected = await tab.evaluate("el => el?.isConnected ?? false")
        if not is_connected:
            logger.debug(f"⚠️ Tab '{label}' is not connected to the DOM.")
            return False
    except Exception as error:
        logger.debug(
            f"⚠️ Could not verify tab connection for '{label}': {error}",
            exc_info=True,
        )
        return False

    try:
        frame = await tab.owner_frame()
        page = frame.page if frame else None
    except Exception as error:
        logger.debug(
            f"⚠️ Could not resolve parent page for tab '{label}': {error}",
            exc_info=True,
        )
        return False

    try:
        if page:
            clicked = await safe_click(
                page, tab, label, timeout=timeout_ms / 1000, ctx=ctx
            )
            if not clicked:
                return False

            await wait_until_dom_stable(page, mode="QUICK", ctx=ctx)
            logger.debug(f"✅ Tab '{label}' clicked and DOM stabilized.")
            return True
    except Exception as error:
        logger.warning(
            f"❌ Failed to click and settle tab '{label}': {error}",
            exc_info=True,
        )
        return False

    return False


async def _get_tab_label(tab: ElementHandle, idx: int) -> str:
    """Returns a readable label for logging and capture headers.

    Args:
        tab (ElementHandle): The tab element.
        idx (int): Index in tab list.

    Returns:
        str: Label string.
    """
    try:
        text = await tab.inner_text()
    except RuntimeError as error:
        logger.debug(
            f"⚠️ Could not get inner_text for tab-{idx}: {error}",
            exc_info=True,
        )
        return f"tab-{idx}"
    except Exception as error:
        logger.warning(
            f"❌ Unexpected error getting inner_text for tab-{idx}: {error}",
            exc_info=True,
        )
        return f"tab-{idx}"

    label = text.strip()
    return label if label else f"tab-{idx}"
