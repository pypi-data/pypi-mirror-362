"""Structured DOM Interaction and Capture Pipeline for Dynamic Web Pages.

This module defines `capture_dom_stages_universal`, a high-level controller that interacts
with dynamic web pages using Playwright and extracts meaningful structured content in
a modular, phase-aware, and deduplicated manner.

The capture process follows four core phases:

1. Navigation and Setup:
   - Navigates to the page
   - Waits for initial DOM stabilization
   - Optionally scrolls to load lazy content
   - Prepares session context and stability markers

2. Structured Interaction Phases:
   - Phase 1: Tab expansion (e.g. <button id="tab-menu"> → <div id="menu">)
   - Phase 2: Menu expansion (e.g. hamburger menus, dropdowns)
   - Phase 3: Universal click (buttons, links, other interactive elements)
   - Phase 4: Hover + click exploration (hover-based UIs)

3. DOM Snapshot Collection:
   - Captures the DOM after each interaction step
   - Deduplicates DOMs using content hashing
   - Annotates each DOM snapshot with a `<!-- SOURCE: ... -->` marker

4. Structured Content Extraction:
   - Runs per-phase `capture_*` functions to extract structured content (menus, blobs, tabs)
   - Logs extracted blocks with readable `source_id`s and content previews
   - Deduplicates content blocks within each DOM snapshot
   - Tracks per-phase extraction totals

This module is used by `fetch_rendered_html(...)` as the backend engine for
DOM crawling, structured content discovery, and rendering audit.

All extracted content is represented as `CapturedBlock`, which includes:
- `content`: The extracted raw or summarized string
- `source_id`: A DOM-based identifier (e.g. `#footer`, `script[0]`, `tab-content[menu]`)

Output:
- Returns a list of annotated raw HTML snapshots
- Content block extraction is logged during each capture step
"""

from __future__ import annotations

from collections.abc import Callable
import hashlib
import json
import logging
from typing import Any
from urllib.parse import urlparse

from bs4 import BeautifulSoup, Tag
from playwright.async_api import Page

from ..config.base import FAST_CONFIG
from ..core.context import SessionContext
from ..models.types import CapturedBlock
from ..utils.logging import log_block_group
from .expansion import expand_hidden_menus
from .exploration import explore_hover_and_click
from .scroll import scroll_until_stable
from .stability import wait_until_dom_stable
from .tab_expansion import expand_tabs_and_capture
from .universal_capture import universal_click_everything_and_capture

logger = logging.getLogger(__name__)


def deduplicate_and_capture_blocks(
    captures: list[tuple[str, str]],
    seen_hashes: set[str],
    capture_funcs: list[tuple[str, Callable]],
    trace_prefix: str = "",
) -> tuple[list[CapturedBlock], int]:
    """Deduplicates HTML DOM snapshots and extracts structured content blocks from each unique snapshot.

    For each DOM state:
    - Hashes the full HTML to detect duplicates
    - If unique, parses it with BeautifulSoup and applies the provided capture functions
    - Captures blocks like visible text, tab content, JSON blobs, etc.
    - Logs each block group with a readable source label
    - Returns all structured blocks across DOMs (not the raw HTML itself)

    Args:
        captures (List[Tuple[str, str]]): List of (label, html) DOM pairs.
        seen_hashes (set[str]): Hashes of DOMs already processed.
        capture_funcs (List[Tuple[str, Callable]]): Capture functions to apply per DOM snapshot.
        trace_prefix (str): Optional prefix added to logging tags (e.g., '[click:]').

    Returns:
        Tuple[List[CapturedBlock], int]:
            - All captured and deduplicated blocks across DOMs
            - Number of unique DOM snapshots processed
    """
    captured_blocks: list[CapturedBlock] = []
    added = 0

    for label, html in captures:
        try:
            h = hashlib.sha256(html.encode("utf-8")).hexdigest()
            if h in seen_hashes:
                logger.debug(f"🔁 Skipped duplicate DOM from {label}")
                continue

            seen_hashes.add(h)

            try:
                soup = BeautifulSoup(html, "html.parser")
            except Exception as e:
                logger.warning(
                    f"🚨 Failed to parse HTML for {label}: {type(e).__name__}: {e}"
                )
                continue

            all_by_type = {}
            for name, fn in capture_funcs:
                try:
                    blocks = safe_extract(
                        name, fn, soup, trace=f"{trace_prefix}{label}"
                    )
                    if blocks:
                        all_by_type[name] = blocks
                except Exception as e:
                    logger.warning(
                        f"🚨 Failed to extract {name} blocks from {label}: {type(e).__name__}: {e}"
                    )

            for block_type, blocks in all_by_type.items():
                try:
                    log_block_group(logger, block_type, blocks)
                except Exception as e:
                    logger.debug(
                        f"🔧 Failed to log block group {block_type}: {type(e).__name__}: {e}"
                    )

            try:
                blocks = [b for group in all_by_type.values() for b in group]
                deduped = deduplicate_blocks(blocks)
                logger.info(f"📥 Extracted {len(deduped)} unique blocks from {label}")
                captured_blocks.extend(deduped)
                added += 1
            except Exception as e:
                logger.warning(
                    f"🚨 Failed to process blocks for {label}: {type(e).__name__}: {e}"
                )

        except Exception as e:
            logger.error(
                f"❌ Critical error processing DOM capture {label}: {type(e).__name__}: {e}"
            )

    return captured_blocks, added


async def capture_dom_stages_universal(
    page: Page,
    scroll: bool,
    debug_screenshot_path: str | None,
    ctx: SessionContext,
    config: dict[str, Any] | None = None,
) -> list[CapturedBlock]:
    """Capture structured content blocks from a dynamic web page via multi-phase DOM interaction.

    Assumes `page.goto(...)` was already called.

    Simulates realistic browsing behavior (tab clicks, menu expansion, hover interactions),
    captures the DOM at each phase, and applies modular `capture_` extractors to produce
    deduplicated content blocks.

    Args:
        page: Playwright page object
        scroll: Whether to scroll the page
        debug_screenshot_path: Optional path for debug screenshots
        ctx: Session context
        config: Playwright interaction config. Uses FAST_CONFIG if None.

    Returns:
        List[CapturedBlock]: A list of unique content blocks with `.content`, `.source_id`, and `.capture_type`.
    """
    if ctx.cleanup_started:
        logger.debug("🛑 Session cleanup started, aborting DOM capture")
        return []

    # Use provided config or default to FAST_CONFIG
    if config is None:
        config = FAST_CONFIG

    captured_blocks: list[CapturedBlock] = []
    seen_hashes: set[str] = set()

    # Use VALIDATION mode for ultra-fast checks in validation mode
    is_validation = config and (
        config.get("dom_timeout_ms", 8000) < 2000 or config.get("max_tabs", 10) <= 1
    )
    stability_mode = "VALIDATION" if is_validation else "QUICK"
    try:
        await wait_until_dom_stable(page=page, mode=stability_mode, ctx=ctx)
    except Exception as e:
        logger.warning(f"⚠️ Initial DOM stabilization failed: {type(e).__name__}: {e}")

    if scroll:
        try:
            await scroll_until_stable(page=page, ctx=ctx)
        except Exception as e:
            logger.warning(f"⚠️ Scroll until stable failed: {type(e).__name__}: {e}")

    async def run_phase(
        name: str,
        html_snapshots: list[str],
        capture_funcs: list[tuple[str, Callable]],
    ):
        try:
            blocks, added = deduplicate_and_capture_blocks(
                captures=[
                    (f"{name}-{i}", html) for i, html in enumerate(html_snapshots)
                ],
                seen_hashes=seen_hashes,
                capture_funcs=capture_funcs,
                trace_prefix=f"[{name}:] ",
            )
            captured_blocks.extend(blocks)
            logger.info(
                f"📦 {name.capitalize()} phase: {added} new blocks, {len(blocks)} total blocks"
            )
        except Exception as e:
            logger.error(
                f"❌ {name.capitalize()} phase failed critically: {type(e).__name__}: {e}"
            )

    # ── Phase 1: Tab Expansion ─────────────────────
    # Skip tab expansion if max_tabs is 0 (validation mode)
    if config.get("max_tabs", 10) > 0:
        try:
            tabs = await expand_tabs_and_capture(
                page,
                tab_timeout=config["tab_timeout"],
                max_tabs=config["max_tabs"],
                ctx=ctx,
            )
            await run_phase(
                "tab",
                tabs,
                [
                    ("visible_dom", capture_from_visible_dom_and_scripts),
                    ("tab_section", capture_tab_linked_sections),
                    ("hyperlinks", capture_visible_links),
                    ("structured_links", capture_visible_links),  # Optional, if added
                ],
            )
        except Exception as e:
            logger.error(f"❌ Tab expansion phase failed: {type(e).__name__}: {e}")

    # ── Phase 2: Menu Expansion ─────────────────────
    # Skip menu expansion if expand_buttons is 0 (validation mode)
    if config.get("expand_buttons", 12) > 0:
        try:
            await expand_hidden_menus(page=page, ctx=ctx)
        except Exception as e:
            logger.warning(f"⚠️ Menu expansion failed: {type(e).__name__}: {e}")

    # ── Phase 3: Universal Click ─────────────────────
    # Skip if max_tabs is 0 (validation mode)
    if config.get("max_tabs", 10) > 0:
        try:
            clicks = await universal_click_everything_and_capture(
                page=page,
                max_elements=config["max_tabs"],
                timeout_per_element=config["tab_timeout"],
                ctx=ctx,
            )
            await run_phase(
                "click",
                clicks,
                [
                    ("script_json", capture_scripts_json_blobs),
                    ("structured_blob", capture_structured_blobs),
                    ("hyperlinks", capture_visible_links),
                    ("structured_links", capture_visible_links),
                ],
            )
        except Exception as e:
            logger.error(f"❌ Universal click phase failed: {type(e).__name__}: {e}")

    # ── Phase 4: Hover & Explore ─────────────────────
    # Skip if explore_elements is 0 (validation mode)
    if config.get("explore_elements", 25) > 0:
        try:
            explores = await explore_hover_and_click(
                page=page,
                max_elements=config["explore_elements"],
                ctx=ctx,
            )
            await run_phase(
                "explore",
                explores,
                [
                    ("visible_dom", capture_from_visible_dom_and_scripts),
                    ("structured_blob", capture_structured_blobs),
                    ("script_json", capture_scripts_json_blobs),
                    ("hyperlinks", capture_visible_links),
                    ("structured_links", capture_visible_links),
                ],
            )
        except Exception as e:
            logger.error(f"❌ Hover exploration phase failed: {type(e).__name__}: {e}")

    # Skip thorough check for validation mode
    is_validation = config and (
        config.get("dom_timeout_ms", 8000) < 2000 or config.get("max_tabs", 10) <= 1
    )
    if not is_validation:
        try:
            await wait_until_dom_stable(page=page, mode="THOROUGH", ctx=ctx)
        except Exception as e:
            logger.warning(f"⚠️ Final DOM stabilization failed: {type(e).__name__}: {e}")

    if debug_screenshot_path:
        try:
            await page.screenshot(path=debug_screenshot_path, full_page=True)
            logger.info(f"📸 Screenshot saved to {debug_screenshot_path}")
        except Exception as e:
            logger.warning(f"⚠️ Screenshot capture failed: {type(e).__name__}: {e}")

    logger.info(f"🎯 DOM capture completed — {len(captured_blocks)} captured blocks")
    return captured_blocks


def capture_visible_links(soup: BeautifulSoup) -> list[CapturedBlock]:
    """Captures <a href="..."> links from key DOM regions like <main>, <nav>, <header>, <footer>, and <aside>.

    Tags each block with a source_id like 'nav:a[3]' or 'main:menu-link'.

    Args:
        soup (BeautifulSoup): Parsed HTML soup object.

    Returns:
        List[CapturedBlock]: List of CapturedBlock instances representing hyperlinks from each section.
    """
    seen: set[str] = set()
    blocks: list[CapturedBlock] = []

    regions = ["main", "nav", "header", "footer", "aside"]
    for region in regions:
        try:
            container = soup.find(region)
            if not container:
                continue

            for i, tag in enumerate(container.find_all("a", href=True)):
                try:
                    href = tag.get("href", "").strip()
                    if not href or href in seen:
                        continue

                    parsed = urlparse(href)
                    if parsed.scheme and parsed.scheme not in {"http", "https"}:
                        continue

                    seen.add(href)

                    # Prefer ID, then first class name, then fallback to index
                    try:
                        tag_id = tag.get("id")
                        tag_classes = tag.get("class")
                        first_class = (
                            tag_classes[0]
                            if isinstance(tag_classes, list) and tag_classes
                            else None
                        )

                        descriptor = tag_id or first_class or f"a[{i}]"
                        source_id = f"{region}:{descriptor}"

                        blocks.append(CapturedBlock(content=href, source_id=source_id))
                    except Exception as e:
                        logger.debug(
                            f"🔧 Failed to create block for link {i} in {region}: {type(e).__name__}: {e}"
                        )

                except Exception as e:
                    logger.debug(
                        f"🔧 Failed to process link {i} in {region}: {type(e).__name__}: {e}"
                    )

        except Exception as e:
            logger.debug(
                f"🔧 Failed to find container for region {region}: {type(e).__name__}: {e}"
            )

    logger.debug(f"🔗 Captured {len(blocks)} visible links from {len(regions)} regions")
    return blocks


def capture_scripts_json_blobs(soup: BeautifulSoup) -> list[CapturedBlock]:
    """Captures and summarizes JSON blobs from <script type="application/json"> tags.

    Each script block is returned as an CapturedBlock with:
    - A flattened preview of key-value pairs (up to 3)
    - A source ID like 'script[type=json][i]'

    Args:
        soup (BeautifulSoup): Parsed DOM.

    Returns:
        List[CapturedBlock]: Summarized JSON blocks with traceable source IDs.
    """
    blocks: list[CapturedBlock] = []

    for i, script in enumerate(soup.find_all("script", type="application/json")):
        try:
            raw = script.string or (script.contents[0] if script.contents else "")
            if not raw or len(raw.strip()) < 20:
                continue

            try:
                obj = json.loads(raw)
                if isinstance(obj, dict):
                    summary = "; ".join(f"{k}: {v}" for k, v in list(obj.items())[:3])
                else:
                    summary = str(obj)[:300]

                source_id = f"script[type=json][{i}]"
                blocks.append(CapturedBlock(content=summary, source_id=source_id))
            except json.JSONDecodeError as e:
                logger.debug(f"📄 Script tag {i} contains invalid JSON: {e}")
            except Exception as e:
                logger.debug(
                    f"🔧 Failed to process JSON in script tag {i}: {type(e).__name__}: {e}"
                )

        except Exception as e:
            logger.debug(f"🔧 Failed to access script tag {i}: {type(e).__name__}: {e}")

    logger.debug(f"📋 Captured {len(blocks)} JSON script blocks")
    return blocks


def capture_structured_blobs(
    soup: BeautifulSoup | None, min_keys: int = 2, min_items: int = 2
) -> list[CapturedBlock]:
    """Captures structured JSON blobs from <script> or <template> tags and returns them as summarized CapturedBlock objects with traceable source identifiers.

    The extractor traverses nested dicts/lists and filters for "rich" JSON objects
    with enough meaningful keys or entries. Content is summarized for logging.

    Args:
        soup (Optional[BeautifulSoup]): Parsed BeautifulSoup DOM.
        min_keys (int): Minimum number of valid keys to accept a dict.
        min_items (int): Minimum valid list items to accept a list.

    Returns:
        List[CapturedBlock]: A list of summarized JSON blocks with source IDs.
    """
    blocks: list[CapturedBlock] = []

    if not soup:
        logger.debug("🔍 No soup provided to capture_structured_blobs")
        return blocks

    def is_rich(obj: dict | list) -> bool:
        try:
            if isinstance(obj, dict):
                return (
                    sum(
                        1
                        for v in obj.values()
                        if v not in (None, "")
                        and isinstance(v, str | int | list | dict)
                    )
                    >= min_keys
                )
            if isinstance(obj, list):
                return sum(1 for o in obj if is_rich(o)) >= min_items
            return False
        except Exception as e:
            logger.debug(
                f"🔧 Failed to check richness of object: {type(e).__name__}: {e}"
            )
            return False

    def collect(obj: dict | list, source_id: str):
        try:
            if isinstance(obj, dict) and is_rich(obj):
                summary = "; ".join(f"{k}: {v}" for k, v in list(obj.items())[:3])
                blocks.append(CapturedBlock(content=summary, source_id=source_id))
            elif isinstance(obj, list):
                for item in obj:
                    collect(item, source_id)
            elif isinstance(obj, dict):
                for v in obj.values():
                    collect(v, source_id)
        except Exception as e:
            logger.debug(
                f"🔧 Failed to collect from object in {source_id}: {type(e).__name__}: {e}"
            )

    # Track separate indices for each tag type
    tag_indices = {"script": 0, "template": 0}

    for tag in soup.find_all(["script", "template"]):
        try:
            if not tag.string:
                continue

            tag_name = tag.name
            tag_index = tag_indices[tag_name]

            try:
                data = json.loads(tag.string.strip())
                source_id = f"{tag_name}[{tag_index}]"
                collect(data, source_id)
                tag_indices[tag_name] += 1
            except json.JSONDecodeError as e:
                logger.debug(
                    f"📄 {tag_name} tag {tag_index} contains invalid JSON: {e}"
                )
            except Exception as e:
                logger.debug(
                    f"🔧 Failed to process {tag_name} tag {tag_index}: {type(e).__name__}: {e}"
                )

        except Exception as e:
            logger.debug(f"🔧 Failed to access tag: {type(e).__name__}: {e}")

    logger.debug(f"📊 Captured {len(blocks)} structured blob blocks")
    return blocks


def capture_from_data_attributes(soup: BeautifulSoup | None) -> list[CapturedBlock]:
    """Captures JSON-like values embedded in HTML data-* attributes and returns them as structured CapturedBlock objects.

    Args:
        soup (Optional[BeautifulSoup]): Parsed DOM.

    Returns:
        List[CapturedBlock]: Structured blocks with preview content and source ID.
    """
    results: list[CapturedBlock] = []
    if not soup:
        logger.debug("🔍 No soup provided to capture_from_data_attributes")
        return results

    # Track indices per tag type
    tag_indices: dict[str, int] = {}

    for tag in soup.find_all():
        try:
            tag_name = tag.name
            # Get the current index for this tag type
            tag_index = tag_indices.get(tag_name, 0)

            for key, value in tag.attrs.items():
                try:
                    if (
                        key.startswith("data-")
                        and isinstance(value, str)
                        and "{" in value
                    ):
                        try:
                            obj = json.loads(value)
                            if isinstance(obj, dict):
                                # Preview: flatten top-level keys/values
                                summary = "; ".join(
                                    f"{k}: {v}" for k, v in list(obj.items())[:3]
                                )
                                source_id = f"{tag_name}[{tag_index}].{key}"
                                results.append(
                                    CapturedBlock(content=summary, source_id=source_id)
                                )
                        except json.JSONDecodeError as e:
                            logger.debug(
                                f"📄 Data attribute {key} in {tag_name}[{tag_index}] contains invalid JSON: {e}"
                            )
                        except Exception as e:
                            logger.debug(
                                f"🔧 Failed to process data attribute {key} in {tag_name}[{tag_index}]: {type(e).__name__}: {e}"
                            )
                except Exception as e:
                    logger.debug(
                        f"🔧 Failed to check attribute {key} in {tag_name}[{tag_index}]: {type(e).__name__}: {e}"
                    )

            # Increment the index for this tag type
            tag_indices[tag_name] = tag_index + 1

        except Exception as e:
            logger.debug(
                f"🔧 Failed to process attributes for tag: {type(e).__name__}: {e}"
            )

    logger.debug(f"📊 Captured {len(results)} data attribute blocks")
    return results


def capture_tab_linked_sections(soup: BeautifulSoup | None) -> list[CapturedBlock]:
    """Captures content from sections linked to <button id="tab-XYZ"> patterns commonly used in tabbed UIs.

    This looks for buttons with IDs like "tab-menu", and retrieves content
    from elements with id="menu" if they exist and contain meaningful text.

    Args:
        soup (Optional[BeautifulSoup]): Parsed BeautifulSoup DOM.

    Returns:
        List[CapturedBlock]: A list of content blocks with source IDs indicating their tab section.
    """
    if not soup:
        logger.debug("🔍 No soup provided to capture_tab_linked_sections")
        return []

    try:
        tab_ids = set()
        for btn in soup.find_all("button"):
            try:
                if isinstance(btn, Tag) and btn.get("id", "").startswith("tab-"):
                    tab_id = btn.get("id", "").removeprefix("tab-")
                    if tab_id:
                        tab_ids.add(tab_id)
            except Exception as e:
                logger.debug(
                    f"🔧 Failed to process button for tab ID: {type(e).__name__}: {e}"
                )
    except Exception as e:
        logger.warning(f"🚨 Failed to find tab buttons: {type(e).__name__}: {e}")
        return []

    blocks: list[CapturedBlock] = []

    for section_id in tab_ids:
        try:
            section = soup.find(id=section_id)
            if section and isinstance(section, Tag):
                try:
                    text = section.get_text(" ", strip=True)
                    if len(text.split()) > 5:
                        blocks.append(
                            CapturedBlock(
                                content=" ".join(text.split()),
                                source_id=f"tab-content[{section_id}]",
                            )
                        )
                except Exception as e:
                    logger.debug(
                        f"🔧 Failed to extract text from section {section_id}: {type(e).__name__}: {e}"
                    )
        except Exception as e:
            logger.debug(
                f"🔧 Failed to find section with id {section_id}: {type(e).__name__}: {e}"
            )

    logger.debug(f"📑 Captured {len(blocks)} tab-linked section blocks")
    return blocks


def capture_from_visible_dom_and_scripts(soup: BeautifulSoup) -> list[CapturedBlock]:
    """Captures visible text blocks from <div> tags in the DOM, along with a source identifier.

    Each block is returned as a ` CapturedBlock ` containing:
    - The stripped text content of the element
    - A source identifier based on `id`, `class`, or fallback to tag name with index

    Source identifiers are formatted as:
    - "#<id>" if the element has an id
    - ".<class>" if the element has a class (first in list if multiple)
    - "<tag>[i]" as fallback (e.g., "div[3]")

    Args:
        soup (BeautifulSoup): Parsed HTML soup object.

    Returns:
        List[CapturedBlock]: Structured content blocks with source ID metadata.
    """
    blocks: list[CapturedBlock] = []

    for i, tag in enumerate(soup.find_all("div")):
        try:
            if not isinstance(tag, Tag):
                continue

            try:
                text = tag.get_text(strip=True)
                if not text:
                    continue

                try:
                    tag_class = tag.get("class")
                    class_string = (
                        tag_class[0]
                        if isinstance(tag_class, list) and tag_class
                        else None
                    )
                    source_id = tag.get("id") or class_string or f"{tag.name}[{i}]"

                    blocks.append(CapturedBlock(content=text, source_id=source_id))
                except Exception as e:
                    logger.debug(
                        f"🔧 Failed to create block for div {i}: {type(e).__name__}: {e}"
                    )

            except Exception as e:
                logger.debug(
                    f"🔧 Failed to extract text from div {i}: {type(e).__name__}: {e}"
                )

        except Exception as e:
            logger.debug(f"🔧 Failed to process div tag {i}: {type(e).__name__}: {e}")

    logger.debug(f"📝 Captured {len(blocks)} visible DOM blocks")
    return blocks


def safe_extract(name: str, fn: Callable, soup, trace: str = "") -> list[CapturedBlock]:
    """Safely executes an HTML block extractor function and catches/logs any exceptions.

    This wrapper helps prevent extractor failures from crashing the overall extraction flow,
    and logs meaningful errors for debugging.

    Args:
        name (str): Label for the extractor (e.g. 'visible_dom', 'script_json').
        fn (Callable): The extractor function that takes a BeautifulSoup object and returns a list of CapturedBlock.
        soup: The BeautifulSoup DOM object to pass into the extractor.
        trace (str): Optional logging prefix to include trace ID or URL context.

    Returns:
        List[CapturedBlock]: The list of extracted blocks, or an empty list if an error occurs or no blocks are returned.
    """
    try:
        result = fn(soup)
        if not result:
            logger.debug(f"{trace}[{name}] — No blocks extracted.")
            return []

        try:
            for block in result:
                block.capture_type = name  # 💡 Tag each block with its source type
        except Exception as e:
            logger.debug(
                f"🔧 Failed to tag blocks with capture type {name}: {type(e).__name__}: {e}"
            )

        return result

    except Exception as e:
        logger.error(
            f"{trace}❌ Error extracting with '{name}': {type(e).__name__}: {e}"
        )
        return []


def deduplicate_blocks(blocks: list[CapturedBlock]) -> list[CapturedBlock]:
    """Deduplicates content blocks based on their text content using SHA256 hashing.

    This function removes blocks with identical content, preserving only the first
    instance of each unique text. Source IDs are not considered in deduplication.

    Args:
        blocks (List[CapturedBlock]): The list of content blocks to deduplicate.

    Returns:
        List[CapturedBlock]: The list of unique blocks, in original order of appearance.
    """
    seen = set()
    unique = []

    for block in blocks:
        try:
            h = hashlib.sha256(block.content.encode("utf-8")).hexdigest()
            if h not in seen:
                seen.add(h)
                unique.append(block)
        except Exception as e:
            logger.debug(f"🔧 Failed to hash block content: {type(e).__name__}: {e}")
            # Include the block anyway to avoid losing data
            unique.append(block)

    logger.debug(f"🔄 Deduplicated {len(blocks)} blocks to {len(unique)} unique blocks")
    return unique
