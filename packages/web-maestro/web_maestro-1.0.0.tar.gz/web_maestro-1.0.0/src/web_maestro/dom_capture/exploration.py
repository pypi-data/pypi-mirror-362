"""Exploratory Interaction Utilities for Dynamic Web Pages.

This module provides functions for interacting with visible, likely-interactive
elements on a page using Playwright. It is designed to trigger modals, drawers,
menus, or other UI elements that require user interaction to become visible.

Core Features:
- Scans the DOM for tab, accordion, button, and menu-like elements.
- Filters to visible, text-containing, reasonably sized components.
- Clicks each one using resilient strategies (via `safe_click`).
- Waits for DOM stability and captures HTML after each interaction.
- Avoids collecting duplicate content snapshots using MD5 hashing.

Intended for:
- Menu and content discovery post-load.
- Capturing progressive UI states in agentic crawlers.
- Low-risk interaction in exploratory phases.
"""

import asyncio
import hashlib
import logging

from playwright.async_api import ElementHandle, Page

from ..core.context import SessionContext
from .click_strategies import safe_click
from .stability import wait_until_dom_stable

logger = logging.getLogger(__name__)

# Interactive selectors to explore in priority order
EXPLORATION_SELECTORS = [
    "button:not([disabled])",
    "[role='button']:not([disabled])",
    ".menu-item",
    ".accordion-header",
    ".tab",
]


async def explore_hover_and_click(
    page: Page, max_elements: int, ctx: SessionContext | None = None
) -> list[str]:
    """Explore and interact with a list of interactive elements on the page.

    Captures unique DOM states after each successful click.

    Args:
        page (Page): The Playwright page object.
        max_elements (int): Max number of interactive elements to attempt clicking.
        ctx (Optional[SessionContext]): Context for teardown safety and task tracking.

    Returns:
        List[str]: A list of HTML content snapshots (with deduplicated DOM states).
    """
    if (ctx is not None and ctx.cleanup_started) or page.is_closed():
        return []

    captured_html: list[str] = []
    seen_hashes: set[str] = set()

    try:
        elements = await _find_explorable_elements(page, max_elements)
        logger.info(f"🧭 Found {len(elements)} explorable elements.")

        for idx, el in enumerate(elements):
            if (ctx is not None and ctx.cleanup_started) or page.is_closed():
                break

            label = await _get_element_label(el, idx)
            success = await safe_click(page=page, el=el, label=label, ctx=ctx)

            if not success:
                continue

            await asyncio.sleep(0.2)
            try:
                await wait_until_dom_stable(page=page, mode="QUICK", ctx=ctx)
            except Exception as e:
                logger.debug(f"⚠️ DOM stability wait failed: {e}", exc_info=True)

            try:
                html = await page.content()
                html_hash = hashlib.sha256(html.encode("utf-8")).hexdigest()

                if html_hash not in seen_hashes:
                    seen_hashes.add(html_hash)
                    comment = f"<!-- EXPLORE CLICK {idx}: {label} -->"
                    captured_html.append(f"{comment}\n{html}")
                else:
                    logger.debug(
                        f"🔁 Skipped duplicate DOM state after clicking {label}."
                    )

            except Exception as e:
                logger.debug(f"⚠️ Failed to capture content after {label}: {e}")

    except Exception as e:
        logger.warning(f"⚠️ explore_hover_and_click failed: {e}", exc_info=True)

    return captured_html


async def _find_explorable_elements(page: Page, limit: int) -> list[ElementHandle]:
    """Selects visible and interactable elements based on class, role, and tag hints.

    Args:
        page (Page): Playwright page.
        limit (int): Max number of elements to return.

    Returns:
        List[ElementHandle]: Filtered and prioritized elements for interaction.
    """
    selector = ",".join(EXPLORATION_SELECTORS)
    try:
        raw = await page.query_selector_all(selector)
    except Exception as e:
        logger.warning(f"⚠️ Failed to query explorable elements: {e}", exc_info=True)
        return []

    filtered: list[ElementHandle] = []

    for el in raw:
        try:
            if not await el.is_visible():
                continue

            box = await el.bounding_box()
            if not box or box["width"] < 30 or box["height"] < 20:
                continue

            text = await el.inner_text()
            if not text.strip():
                continue

            filtered.append(el)

        except Exception as e:
            logger.debug(f"⚠️ Error filtering elements: {e}", exc_info=True)
            continue

    return filtered[:limit]


async def _get_element_label(el: ElementHandle, idx: int) -> str:
    """Generates a human-readable label for logging and comment markup.

    Args:
        el (ElementHandle): The element in question.
        idx (int): Index of the element in the exploration list.

    Returns:
        str: A log-friendly label.
    """
    try:
        text = await el.inner_text()
        text = text.strip()
        if text:
            return f"[{idx}] {text[:60]}"
    except Exception as e:
        logger.debug(f"⚠️ Error getting element label: {e}", exc_info=True)
    return f"[{idx}] <unknown element>"
