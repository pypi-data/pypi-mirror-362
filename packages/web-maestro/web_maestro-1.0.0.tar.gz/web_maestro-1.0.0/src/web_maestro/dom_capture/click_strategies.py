"""Click Strategies for Robust DOM Interaction.

This module provides safe, teardown-aware clicking utilities for interacting
with dynamic content using Playwright. Multiple fallback strategies are
attempted in order to maximize interaction success while avoiding common
issues such as pointer interception, overlays, detached handles, or external links.

Core Entrypoints:
- safe_click: Used in teardown-safe, pointer-safe click scenarios.
- universal_click_element: Used in universal exploration or tab traversal.

Shared logic is encapsulated in the ClickStrategyExecutor class for clarity,
reuse, and debug traceability.

"""

import asyncio
import logging

from playwright.async_api import ElementHandle, Page

from ..core.context import SessionContext
from .ai_scout import classify_element

logger = logging.getLogger(__name__)


class ClickStrategyExecutor:
    """Encapsulates a sequence of safe click strategies, executed in order.

    Returns:
        bool: True on success and tracks which strategy succeeded.
    """

    def __init__(
        self,
        page: Page,
        element: ElementHandle,
        label: str,
        timeout_ms: int,
        ctx: SessionContext | None = None,
        skip_keyboard: bool = False,
    ) -> None:
        """Initializes the ClickStrategyExecutor.

        Args:
            page (Page): Playwright page.
            element (ElementHandle): Element to interact with.
            label (str): Logging label.
            timeout_ms (int): Timeout in milliseconds for each strategy.
            ctx (Optional[SessionContext], optional): Session context. Defaults to None.
            skip_keyboard (bool): Whether to skip keyboard-based interactions.
        """
        self.page = page
        self.el = element
        self.label = label
        self.timeout_ms = timeout_ms
        self.ctx = ctx
        self.skip_keyboard = skip_keyboard

    async def run(self) -> tuple[bool, str | None]:
        """Executes multiple click strategies until one succeeds.

        Returns:
            Tuple[bool, Optional[str]]: Success status and strategy used.
        """
        if self._should_skip():
            return False, None

        # Strategy 1: JavaScript click (with overlay suppression)
        if await self._js_click():
            return True, "js_click"

        # Strategy 2: Playwright force click
        if await self._force_click():
            return True, "force_click"

        # Strategy 3: Dispatch click event
        if await self._dispatch_event():
            return True, "dispatch_event"

        # Strategy 4: Coordinate-based click
        if await self._coordinate_click():
            return True, "coordinate_click"

        # Strategy 5: Keyboard trigger (Enter/Space)
        if not self.skip_keyboard:
            if await self._keyboard_trigger():
                return True, "keyboard_trigger"

        logger.debug(f"❌ All strategies failed for '{self.label}'")
        return False, None

    def _should_skip(self) -> bool:
        """Determines if the strategy execution should be skipped.

        Returns:
            bool: True if should skip, otherwise False.
        """
        return (self.ctx and self.ctx.cleanup_started) or self.page.is_closed()

    async def _js_click(self) -> bool:
        """Attempts a JavaScript click on the element.

        Returns:
            bool: True if successful, otherwise False.
        """
        try:
            await asyncio.wait_for(
                self.page.evaluate(
                    """(el) => {
                    const overlays = document.querySelectorAll('[id*="overlay"], [class*="overlay"]');
                    overlays.forEach(o => {
                        if (o.style) {
                            o.style.pointerEvents = 'none';
                            o.style.zIndex = '-1';
                        }
                    });
                    if (el?.click) el.click();
                }""",
                    self.el,
                ),
                timeout=1,
            )
            logger.debug(f"✅ JS click succeeded for '{self.label}'")
            return True
        except Exception as e:
            logger.debug(f"JS click failed for '{self.label}': {e}")
            return False

    async def _force_click(self) -> bool:
        """Attempts a forceful click using Playwright.

        Returns:
            bool: True if successful, otherwise False.
        """
        try:
            await asyncio.wait_for(
                self.el.click(force=True, timeout=self.timeout_ms, no_wait_after=True),
                timeout=1,
            )
            logger.debug(f"✅ Force click succeeded for '{self.label}'")
            return True
        except Exception as e:
            logger.debug(f"Force click failed for '{self.label}': {e}")
            return False

    async def _dispatch_event(self) -> bool:
        """Dispatches a click event using JavaScript.

        Returns:
            bool: True if successful, otherwise False.
        """
        try:
            await self.page.evaluate(
                """
                (el) => {
                    const event = new MouseEvent('click', {
                        view: window,
                        bubbles: true,
                        cancelable: true,
                        button: 0
                    });
                    el.dispatchEvent(event);
                }
            """,
                self.el,
            )
            logger.debug(f"✅ Dispatch event succeeded for '{self.label}'")
            return True
        except Exception as e:
            logger.debug(f"Dispatch event failed for '{self.label}': {e}")
            return False

    async def _coordinate_click(self) -> bool:
        """Attempts a click at the element's coordinates.

        Returns:
            bool: True if successful, otherwise False.
        """
        try:
            box = await self.el.bounding_box()
            if box and box["width"] > 0 and box["height"] > 0:
                x = box["x"] + box["width"] / 2
                y = box["y"] + box["height"] / 2
                await asyncio.wait_for(self.page.mouse.click(x, y), timeout=1)
                logger.debug(f"✅ Coordinate click succeeded for '{self.label}'")
                return True
        except Exception as e:
            logger.debug(f"Coordinate click failed for '{self.label}': {e}")
        return False

    async def _keyboard_trigger(self) -> bool:
        """Attempts to trigger a click using the keyboard (Enter/Space).

        Returns:
            bool: True if successful, otherwise False.
        """
        try:
            tag = await self.page.evaluate(
                "(el) => el?.tagName?.toLowerCase()", self.el
            )
            await self.el.focus()
            if tag in {"button", "a"}:
                await self.page.keyboard.press("Enter")
            else:
                await self.page.keyboard.press("Space")
            logger.debug(f"✅ Keyboard trigger succeeded for '{self.label}'")
            return True
        except Exception as e:
            logger.debug(f"Keyboard trigger failed for '{self.label}': {e}")
            return False


async def _is_clickable(page: Page, el: ElementHandle, timeout: float = 1.0) -> bool:
    """Determines whether an element is connected, visible, and enabled.

    Args:
        page (Page): The Playwright page.
        el (ElementHandle): The element to check.
        timeout (float, optional): Timeout for the checks. Defaults to 1.0.

    Returns:
        bool: True if the element is clickable, otherwise False.
    """
    try:
        is_connected = await asyncio.wait_for(
            page.evaluate("(el) => el?.isConnected ?? false", el), timeout=timeout
        )
        if not is_connected:
            return False
        visible = await asyncio.wait_for(el.is_visible(), timeout=timeout)
        enabled = await asyncio.wait_for(el.is_enabled(), timeout=timeout)
        return visible and enabled
    except Exception:
        return False


async def _scroll_into_view(el: ElementHandle, timeout: float = 2.0) -> None:
    """Scrolls the element into view if needed.

    Args:
        el (ElementHandle): The element to scroll.
        timeout (float, optional): Timeout for the scroll action. Defaults to 2.0.
    """
    try:
        await asyncio.wait_for(el.scroll_into_view_if_needed(), timeout=timeout)
        await asyncio.sleep(0.1)
    except Exception:
        logger.debug("Failed to scroll element into view")
        pass


async def safe_click(
    page: Page,
    el: ElementHandle,
    label: str,
    timeout: int = 3,
    ctx: SessionContext | None = None,
) -> bool:
    """Safe click wrapper with teardown awareness, pointer-safe, hoverless logic.

    Args:
        page (Page): Playwright page.
        el (ElementHandle): Element to click.
        label (str): Logging label.
        timeout (int): Timeout per strategy (seconds).
        ctx (SessionContext, optional): Context for cancellation.

    Returns:
        bool: True if click succeeded, else False.
    """
    if ctx and ctx.cleanup_started:
        return False

    if not await _is_clickable(page, el):
        return False

    await _scroll_into_view(el)

    executor = ClickStrategyExecutor(
        page=page,
        element=el,
        label=label,
        timeout_ms=timeout * 1000,
        ctx=ctx,
        skip_keyboard=False,
    )
    success, strategy = await executor.run()
    if success:
        logger.debug(f"✅ safe_click used strategy: {strategy}")
    return success


async def safe_click_if_relevant(
    page: Page,
    el: ElementHandle,
    label: str,
    timeout: int = 3,
    ctx: SessionContext | None = None,
    classification_prompt: str | None = None,
) -> bool:
    """LLM-enhanced safe click: only click if label matches classification criteria.

    Useful when traversing categories, tabs, or content with ambiguous labels.

    Args:
        page (Page): Playwright page.
        el (ElementHandle): Element to click.
        label (str): Visible label or aria-label for classification.
        timeout (int): Per-click strategy timeout (seconds).
        ctx (SessionContext, optional): Teardown safety context.
        classification_prompt (str, optional): Custom prompt for element classification.

    Returns:
        bool: True if element was clicked, else False.
    """
    if not classify_element(label, classification_prompt):
        logger.debug(f"⏭️ Skipped irrelevant element: '{label}'")
        return False

    return await safe_click(page, el, label, timeout=timeout, ctx=ctx)


# Backward compatibility alias
async def safe_click_if_menu_relevant(
    page: Page,
    el: ElementHandle,
    label: str,
    timeout: int = 3,
    ctx: SessionContext | None = None,
) -> bool:
    """DEPRECATED: Use safe_click_if_relevant with classification_prompt instead."""
    return await safe_click_if_relevant(
        page,
        el,
        label,
        timeout,
        ctx,
        classification_prompt=(
            "Does the following label refer to a food-related tab in a restaurant website?\n"
            "Label: '{label}'\n\n"
            "Respond only with 'Yes' or 'No'."
        ),
    )


async def universal_click_element(
    page: Page,
    el: ElementHandle,
    label: str,
    timeout_ms: int = 2000,
    ctx: SessionContext | None = None,
) -> bool:
    """Broader click utility with all strategies including keyboard fallback.

    Used during universal DOM traversal.

    Args:
        page (Page): Playwright page.
        el (ElementHandle): Element to click.
        label (str): Label used in logs.
        timeout_ms (int): Max time per click attempt.
        ctx (SessionContext, optional): Teardown context.

    Returns:
        bool: True if any strategy worked, else False.
    """
    if not await _is_clickable(page, el):
        return False

    await _scroll_into_view(el)

    executor = ClickStrategyExecutor(
        page=page,
        element=el,
        label=label,
        timeout_ms=timeout_ms,
        ctx=ctx,
        skip_keyboard=False,
    )
    success, strategy = await executor.run()
    if success:
        logger.debug(f"✅ universal_click_element used strategy: {strategy}")
    return success
