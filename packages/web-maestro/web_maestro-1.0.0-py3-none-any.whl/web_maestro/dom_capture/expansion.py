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
    menu_specific_selector=None,
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
        menu_specific_selector: Optional selector for menu-specific elements.
        classification_prompt: Optional prompt for LLM-based element classification.

    Returns:
        List[str]: List of unique snapshots of the DOM.
    """
    if (ctx and ctx.cleanup_started) or page.is_closed():
        return []

    html_blocks: list[str] = []
    seen_hashes: set[str] = set()

    # Capture initial DOM state
    try:
        html = await page.content()
        h = hashlib.sha256(html.encode()).hexdigest()
        seen_hashes.add(h)
        html_blocks.append("<!-- INITIAL -->\n" + html)
    except Exception as e:
        logger.warning(f"⚠️ Failed to capture initial DOM: {e}")
    try:
        # Then concatenate when you use them:
        # Concatenate all three with commas
        all_clickable_selectors = (
            FOCUSED_CLICKABLE_SELECTOR
            + ", "
            + UNIVERSAL_CLICKABLE_SELECTOR
            + ", "
            + ADDITIONAL_CLICKABLE_PATTERNS
        )
        elements = await page.query_selector_all(all_clickable_selectors)
    except Exception as e:
        logger.warning(f"⚠️ Failed to query clickable elements: {e}")
        return html_blocks

    filtered: list[tuple[ElementHandle, int, float, float]] = []

    for i, el in enumerate(elements):
        try:
            if (ctx and ctx.cleanup_started) or page.is_closed():
                break

            if not await el.is_visible():
                continue

            box = await el.bounding_box()
            if not box or box["width"] < 5 or box["height"] < 5:
                continue

            try:
                if not await el.is_enabled():
                    continue
            except Exception as e:
                logger.debug(f"⚠️ Error checking if element {i} is enabled: {e}")
                continue

            filtered.append((el, i, box["x"], box["y"]))
        except Exception as e:
            logger.info(f"⚠️ Error processing element {i}: {e}")
            continue

    # Sort top-down, left-to-right
    filtered.sort(key=lambda x: (x[3], x[2]))
    filtered = filtered[:max_elements]

    for el, idx, x, y in filtered:
        if (ctx and ctx.cleanup_started) or page.is_closed():
            break

        label = f"el-{idx}-at-{int(x)}x{int(y)}"

        # ✅ LLM-based relevance check before click (if prompt provided)
        # Note: classify_element returns True if no prompt is provided
        if classification_prompt and not classify_element(label, classification_prompt):
            logger.debug(f"[LLM-CLICK] ⏭️ Skipping irrelevant element: '{label}'")
            continue

        try:
            clicked = await safe_click(
                page, el, label=label, ctx=ctx, timeout=timeout_per_element / 1000
            )
            if not clicked:
                continue

            await asyncio.sleep(0.2)
            await wait_until_dom_stable(page, mode="QUICK", ctx=ctx)

            try:
                html = await page.content()
                h = hashlib.sha256(html.encode()).hexdigest()
                if h not in seen_hashes:
                    seen_hashes.add(h)
                    html_blocks.append(f"<!-- CLICK {label} -->\n{html}")
                else:
                    logger.debug(f"🔁 Skipped duplicate DOM after clicking {label}")
            except Exception as e:
                logger.debug(f"⚠️ Failed to capture DOM after click {label}: {e}")

        except Exception as e:
            logger.debug(f"⚠️ Error during universal click {label}: {e}")

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

    try:
        await _expand_details(page)
    except Exception as e:
        logger.warning(f"⚠️ Failed to expand <details> elements: {e}")

    try:
        await _click_expandable_triggers(page, ctx=ctx)
    except Exception as e:
        logger.warning(f"⚠️ Failed to click expandable triggers: {e}")

    try:
        await _log_visible_nav_links(page)
    except Exception as e:
        logger.warning(f"⚠️ Failed to log visible nav links: {e}")


async def _expand_details(page: Page) -> None:
    """Expands all <details> elements that are not already open.

    Args:
        page (Page): Playwright page object.

    """
    try:
        if page.is_closed():
            return

        details = await page.query_selector_all("details:not([open])")

        for d in details:
            try:
                await page.evaluate("(el) => el.setAttribute('open', '')", d)
                await asyncio.sleep(0.1)
                logger.info("✅ Expanded <details> element")
            except Exception as e:
                logger.debug(f"⚠️ Failed to expand <details>: {e}")

    except Exception as e:
        logger.warning(f"❌ Error while selecting <details>: {e}")


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
    if ctx.cleanup_started or page.is_closed():
        return

    try:
        selector = await _get_expandable_menu_selector()
        elements = await page.query_selector_all(selector)
        logger.info(f"🔘 Found {len(elements)} expandable triggers")
    except Exception as e:
        logger.warning(f"❌ Failed to query expandable triggers: {e}")
        return

    clicked = 0
    failures = 0

    for idx, el in enumerate(elements[:max_expands]):
        if ctx.cleanup_started or page.is_closed():
            break

        try:
            if not await el.is_visible():
                continue

            await el.scroll_into_view_if_needed()
            success = await safe_click(page, el, label=f"expand-btn-{idx}", ctx=ctx)

            if success:
                clicked += 1
                failures = 0
                await asyncio.sleep(0.2)
            else:
                failures += 1

            if failures >= max_failures:
                logger.warning("🚫 Too many consecutive failures — stopping")
                break

        except Exception as e:
            logger.debug(f"⚠️ Error clicking expandable trigger {idx}: {e}")
            failures += 1
            if failures >= max_failures:
                break

    if clicked:
        logger.info(f"✅ Clicked {clicked} expandable trigger(s)")


async def _log_visible_nav_links(page: Page) -> None:
    """Logs visible links from nav, sidebar, or drawer menus.

    Args:
        page (Page): Playwright page object.

    """
    if page.is_closed():
        return

    try:
        links = await page.query_selector_all("nav a, .sidebar a, .drawer a, .menu a")
        count = 0

        for link in links:
            try:
                if await link.is_visible():
                    text = (await link.inner_text()).strip()
                    href = await link.get_attribute("href")
                    if href:
                        logger.info(f"🔗 NAV: {text or 'no label'} → {href}")
                        count += 1
                        if count >= 5:
                            break
            except Exception:
                logger.warning(f"⚠️ Failed to log visible nav links for a link: {link}")
                continue

    except Exception as e:
        logger.warning(f"⚠️ Failed to log visible nav links: {e}")
