"""Universal Click-and-Capture Utility.

This module performs a wide-sweep of interaction across potentially clickable
elements on the page (tabs, menu items, buttons, toggles) and captures the
DOM after each successful interaction.

Designed for broad DOM exploration where the structure is unknown but may
contain deferred or hidden content behind click-based triggers.

Features:
- Clicks interactive elements in visual order (top-down, left-to-right).
- Uses resilient click logic (`safe_click`).
- Waits for DOM stabilization after each click.
- Skips duplicate content snapshots using hash-based deduplication.

Functions:
- universal_click_everything_and_capture: Main click-capture loop.

"""

from __future__ import annotations

import asyncio
import hashlib
import logging

from playwright.async_api import ElementHandle, Page

from ..config.base import (
    ADDITIONAL_CLICKABLE_PATTERNS,
    FOCUSED_CLICKABLE_SELECTOR,
    UNIVERSAL_CLICKABLE_SELECTOR,
)
from ..core.context import SessionContext
from .ai_scout import classify_element
from .click_strategies import safe_click
from .stability import wait_until_dom_stable

logger = logging.getLogger(__name__)


async def universal_click_everything_and_capture(
    page: Page,
    max_elements: int = 50,
    timeout_per_element: int = 2000,
    ctx: SessionContext | None = None,
    classification_prompt: str | None = None,
) -> list[str]:
    """Clicks a filtered set of interactive elements on the page and captures the DOM after each.

    Returns a list of unique snapshots (based on DOM hash).

    Only clicks elements that match the classification criteria (if provided).

    Args:
        page (Page): The Playwright page object.
        max_elements (int): Maximum number of elements to click.
        timeout_per_element (int): Timeout per element in milliseconds.
        ctx (Optional[SessionContext]): Session context for cleanup awareness.
        classification_prompt (Optional[str]): Prompt for element classification.

    Returns:
        List[str]: List of unique snapshots of the DOM.
    """
    if (ctx and ctx.cleanup_started) or page.is_closed():
        logger.debug("🛑 Universal click aborted - cleanup started or page closed")
        return []

    html_blocks: list[str] = []
    seen_hashes: set[str] = set()

    # Capture initial DOM state
    try:
        html = await page.content()
        h = hashlib.sha256(html.encode()).hexdigest()
        seen_hashes.add(h)
        html_blocks.append("<!-- INITIAL -->\n" + html)
        logger.debug("📄 Captured initial DOM state")
    except Exception as e:
        logger.warning(f"⚠️ Failed to capture initial DOM: {type(e).__name__}: {e}")

    # Query clickable elements
    try:
        # Concatenate all three with commas
        all_clickable_selectors = (
            FOCUSED_CLICKABLE_SELECTOR
            + ", "
            + UNIVERSAL_CLICKABLE_SELECTOR
            + ", "
            + ADDITIONAL_CLICKABLE_PATTERNS
        )
        elements = await page.query_selector_all(all_clickable_selectors)
        logger.info(f"🔍 Found {len(elements)} potentially clickable elements")
    except Exception as e:
        logger.error(f"❌ Failed to query clickable elements: {type(e).__name__}: {e}")
        return html_blocks

    # Filter elements by visibility and size
    filtered: list[tuple[ElementHandle, int, float, float]] = []

    for i, el in enumerate(elements):
        try:
            if (ctx and ctx.cleanup_started) or page.is_closed():
                logger.debug(
                    f"🛑 Element filtering stopped at index {i} - cleanup/close"
                )
                break

            try:
                is_visible = await el.is_visible()
                if not is_visible:
                    logger.debug(f"👻 Element {i} not visible, skipping")
                    continue
            except Exception as e:
                logger.debug(
                    f"🔧 Failed to check visibility for element {i}: {type(e).__name__}: {e}"
                )
                continue

            try:
                box = await el.bounding_box()
                if not box or box["width"] < 5 or box["height"] < 5:
                    logger.debug(f"📏 Element {i} too small (box: {box}), skipping")
                    continue
            except Exception as e:
                logger.debug(
                    f"🔧 Failed to get bounding box for element {i}: {type(e).__name__}: {e}"
                )
                continue

            try:
                is_enabled = await el.is_enabled()
                if not is_enabled:
                    logger.debug(f"🚫 Element {i} not enabled, skipping")
                    continue
            except Exception as e:
                logger.debug(
                    f"🔧 Failed to check enabled state for element {i}: {type(e).__name__}: {e}"
                )
                # Continue anyway - some elements might not support is_enabled()

            try:
                filtered.append((el, i, box["x"], box["y"]))
                logger.debug(
                    f"✅ Element {i} passed filters - position ({box['x']}, {box['y']})"
                )
            except Exception as e:
                logger.debug(
                    f"🔧 Failed to add element {i} to filtered list: {type(e).__name__}: {e}"
                )

        except Exception as e:
            logger.debug(
                f"🔧 Unexpected error processing element {i}: {type(e).__name__}: {e}"
            )

    logger.info(
        f"🎯 Filtered to {len(filtered)} clickable elements from {len(elements)} total"
    )

    # Sort top-down, left-to-right
    try:
        filtered.sort(key=lambda x: (x[3], x[2]))
        filtered = filtered[:max_elements]
        logger.debug(f"📊 Processing top {len(filtered)} elements in visual order")
    except Exception as e:
        logger.warning(f"⚠️ Failed to sort filtered elements: {type(e).__name__}: {e}")

    # Click each filtered element
    successful_clicks = 0
    for el, idx, x, y in filtered:
        try:
            if (ctx and ctx.cleanup_started) or page.is_closed():
                logger.debug(f"🛑 Click loop stopped at element {idx} - cleanup/close")
                break

            label = f"el-{idx}-at-{int(x)}x{int(y)}"

            # ✅ LLM-based relevance check before click
            try:
                is_relevant = (
                    classify_element(label, classification_prompt)
                    if classification_prompt
                    else True
                )
                if not is_relevant:
                    logger.debug(
                        f"[LLM-CLICK] ⏭️ Skipping irrelevant element: '{label}'"
                    )
                    continue
                else:
                    logger.debug(f"[LLM-CLICK] ✅ Element deemed relevant: '{label}'")
            except Exception as e:
                logger.debug(
                    f"🔧 LLM check failed for {label}, proceeding anyway: {type(e).__name__}: {e}"
                )

            try:
                clicked = await safe_click(
                    page, el, label=label, ctx=ctx, timeout=timeout_per_element / 1000
                )
                if not clicked:
                    logger.debug(f"❌ Safe click failed for {label}")
                    continue

                successful_clicks += 1
                logger.debug(f"✅ Successfully clicked {label}")

                try:
                    await asyncio.sleep(0.2)
                    await wait_until_dom_stable(page, mode="QUICK", ctx=ctx)
                except Exception as e:
                    logger.debug(
                        f"🔧 DOM stabilization failed after clicking {label}: {type(e).__name__}: {e}"
                    )

                try:
                    html = await page.content()
                    h = hashlib.sha256(html.encode()).hexdigest()
                    if h not in seen_hashes:
                        seen_hashes.add(h)
                        html_blocks.append(f"<!-- CLICK {label} -->\n{html}")
                        logger.debug(
                            f"📄 Captured new DOM state after clicking {label}"
                        )
                    else:
                        logger.debug(f"🔁 Skipped duplicate DOM after clicking {label}")
                except Exception as e:
                    logger.warning(
                        f"⚠️ Failed to capture DOM after clicking {label}: {type(e).__name__}: {e}"
                    )

            except Exception as e:
                logger.debug(
                    f"🔧 Click operation failed for {label}: {type(e).__name__}: {e}"
                )

        except Exception as e:
            logger.warning(
                f"⚠️ Unexpected error during universal click for element {idx}: {type(e).__name__}: {e}"
            )

    logger.info(
        f"🎯 Universal click completed: {successful_clicks} successful clicks, {len(html_blocks)} unique DOM snapshots"
    )
    return html_blocks


async def expand_hidden_menus(page: Page, ctx: SessionContext) -> None:
    """Expands common hidden UI menus, navs, and sections using fallback strategies.

    This function is designed to trigger hidden or collapsible UI
    elements such as:
    - <details> HTML elements
    - Hamburger menus
    - Navigation drawers
    - Accordions and dropdown toggles

    All interactions are teardown-safe and do not rely on hover.

    Args:
        page (Page): Playwright page object.
        ctx (SessionContext): Shared context for cleanup awareness.

    """
    if ctx.cleanup_started or page.is_closed():
        logger.debug(
            "🚫 Skipping expand_hidden_menus — cleanup started or page is closed"
        )
        return

    logger.info("🔄 Starting hidden menu expansion")

    # Expand <details> elements
    try:
        await _expand_details(page)
    except Exception as e:
        logger.warning(
            f"⚠️ Failed to expand <details> elements: {type(e).__name__}: {e}"
        )

    # Click expandable triggers
    try:
        await _click_expandable_triggers(page, ctx=ctx)
    except Exception as e:
        logger.warning(
            f"⚠️ Failed to click expandable triggers: {type(e).__name__}: {e}"
        )

    # Log visible nav links
    try:
        await _log_visible_nav_links(page)
    except Exception as e:
        logger.warning(f"⚠️ Failed to log visible nav links: {type(e).__name__}: {e}")

    logger.info("✅ Hidden menu expansion completed")


async def _expand_details(page: Page) -> None:
    """Expands all <details> elements that are not already open.

    Args:
        page (Page): Playwright page object.

    """
    try:
        if page.is_closed():
            logger.debug("🚫 Page closed, skipping details expansion")
            return

        try:
            details = await page.query_selector_all("details:not([open])")
            logger.debug(f"🔍 Found {len(details)} closed <details> elements")
        except Exception as e:
            logger.warning(
                f"❌ Failed to query <details> elements: {type(e).__name__}: {e}"
            )
            return

        expanded_count = 0
        for i, d in enumerate(details):
            try:
                await page.evaluate("(el) => el.setAttribute('open', '')", d)
                await asyncio.sleep(0.1)
                expanded_count += 1
                logger.debug(f"✅ Expanded <details> element {i}")
            except Exception as e:
                logger.debug(
                    f"🔧 Failed to expand <details> element {i}: {type(e).__name__}: {e}"
                )

        if expanded_count > 0:
            logger.info(f"Expanded {expanded_count} <details> elements")
        else:
            logger.debug("i️ No <details> elements to expand")

    except Exception as e:
        logger.error(f"❌ Critical error in details expansion: {type(e).__name__}: {e}")


async def _get_expandable_menu_selector() -> str:
    """Returns a comprehensive selector for buttons/menus that toggle content.

    Includes hamburger icons, drawer triggers, accordions, and more.

    Returns:
        str: The selector for expandable menu elements.
    """
    return (
        "button[aria-expanded='false'],[role='button'][aria-expanded='false'],"
        "[aria-haspopup='true'],[aria-label*='menu' i],[aria-label*='navigation' i],"
        "[aria-label*='expand' i],[aria-label*='toggle' i],[data-toggle],"
        "[data-target*='menu'],button.menu-toggle,button.burger,button.hamburger,"
        ".menu-icon,.hamburger,.drawer-toggle,.dropdown-toggle,"
        ".accordion,.accordion-toggle,.expandable-menu,.hidden-menu"
    )


async def _click_expandable_triggers(
    page: Page,
    max_expands: int = 12,
    max_failures: int = 2,
    ctx: SessionContext | None = None,
) -> None:
    """Clicks expandable menu triggers (hamburgers, accordions, drawers).

    Args:
        page (Page): Playwright page object.
        max_expands (int): Max elements to try.
        max_failures (int): Abort after this many consecutive failures.
        ctx (Optional[SessionContext]): Teardown-aware context.

    """
    if (ctx and ctx.cleanup_started) or page.is_closed():
        logger.debug("🚫 Skipping expandable triggers - cleanup started or page closed")
        return

    try:
        try:
            selector = await _get_expandable_menu_selector()
            elements = await page.query_selector_all(selector)
            logger.info(f"🔘 Found {len(elements)} expandable trigger elements")
        except Exception as e:
            logger.error(
                f"❌ Failed to query expandable triggers: {type(e).__name__}: {e}"
            )
            return

        clicked = 0
        failures = 0

        for idx, el in enumerate(elements[:max_expands]):
            try:
                if (ctx and ctx.cleanup_started) or page.is_closed():
                    logger.debug(
                        f"🛑 Expandable trigger loop stopped at element {idx} - cleanup/close"
                    )
                    break

                try:
                    is_visible = await el.is_visible()
                    if not is_visible:
                        logger.debug(
                            f"👻 Expandable trigger {idx} not visible, skipping"
                        )
                        continue
                except Exception as e:
                    logger.debug(
                        f"🔧 Failed to check visibility for trigger {idx}: {type(e).__name__}: {e}"
                    )
                    continue

                try:
                    await el.scroll_into_view_if_needed()
                except Exception as e:
                    logger.debug(
                        f"🔧 Failed to scroll trigger {idx} into view: {type(e).__name__}: {e}"
                    )

                try:
                    success = await safe_click(
                        page, el, label=f"expand-btn-{idx}", ctx=ctx
                    )

                    if success:
                        clicked += 1
                        failures = 0
                        logger.debug(
                            f"✅ Successfully clicked expandable trigger {idx}"
                        )
                        try:
                            await asyncio.sleep(0.2)
                        except Exception as e:
                            logger.debug(
                                f"🔧 Sleep interrupted after clicking trigger {idx}: {type(e).__name__}: {e}"
                            )
                    else:
                        failures += 1
                        logger.debug(f"❌ Failed to click expandable trigger {idx}")

                    if failures >= max_failures:
                        logger.warning(
                            f"🚫 Too many consecutive failures ({failures}) — stopping expandable triggers"
                        )
                        break

                except Exception as e:
                    logger.debug(
                        f"🔧 Click failed for expandable trigger {idx}: {type(e).__name__}: {e}"
                    )
                    failures += 1
                    if failures >= max_failures:
                        logger.warning(
                            f"🚫 Failure threshold reached ({failures}) — stopping expandable triggers"
                        )
                        break

            except Exception as e:
                logger.warning(
                    f"⚠️ Unexpected error processing expandable trigger {idx}: {type(e).__name__}: {e}"
                )
                failures += 1
                if failures >= max_failures:
                    break

        if clicked > 0:
            logger.info(f"Successfully clicked {clicked} expandable trigger(s)")
        else:
            logger.debug("i No expandable triggers were clicked")

    except Exception as e:
        logger.error(
            f"❌ Critical error in expandable triggers: {type(e).__name__}: {e}"
        )


async def _log_visible_nav_links(page: Page) -> None:
    """Logs visible links from nav, sidebar, or drawer menus.

    Args:
        page (Page): Playwright page object.

    """
    if page.is_closed():
        logger.debug("🚫 Page closed, skipping nav links logging")
        return

    try:
        try:
            links = await page.query_selector_all(
                "nav a, .sidebar a, .drawer a, .menu a"
            )
            logger.debug(f"🔍 Found {len(links)} potential navigation links")
        except Exception as e:
            logger.warning(
                f"⚠️ Failed to query navigation links: {type(e).__name__}: {e}"
            )
            return

        count = 0
        logged_count = 0

        for i, link in enumerate(links):
            try:
                try:
                    is_visible = await link.is_visible()
                    if not is_visible:
                        continue
                except Exception as e:
                    logger.debug(
                        f"🔧 Failed to check visibility for nav link {i}: {type(e).__name__}: {e}"
                    )
                    continue

                try:
                    text = (await link.inner_text()).strip()
                except Exception as e:
                    logger.debug(
                        f"🔧 Failed to get text for nav link {i}: {type(e).__name__}: {e}"
                    )
                    text = "no label"

                try:
                    href = await link.get_attribute("href")
                    if href:
                        logger.info(f"🔗 NAV: {text or 'no label'} → {href}")
                        logged_count += 1
                        count += 1
                        if count >= 5:
                            break
                except Exception as e:
                    logger.debug(
                        f"🔧 Failed to get href for nav link {i}: {type(e).__name__}: {e}"
                    )

            except Exception as e:
                logger.debug(
                    f"🔧 Failed to process nav link {i}: {type(e).__name__}: {e}"
                )

        if logged_count > 0:
            logger.debug(f"📝 Logged {logged_count} visible navigation links")
        else:
            logger.debug("i No visible navigation links found")

    except Exception as e:
        logger.error(
            f"❌ Critical error logging visible nav links: {type(e).__name__}: {e}"
        )
