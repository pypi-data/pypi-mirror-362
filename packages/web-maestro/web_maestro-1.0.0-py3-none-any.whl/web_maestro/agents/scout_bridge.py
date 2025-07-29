"""Bridge interface between agents and Playwright navigation."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any

from ..models.types import DOMElement


class NavigationAction(Enum):
    """Types of navigation actions."""

    CLICK_ELEMENT = "click_element"
    SCROLL_PAGE = "scroll_page"
    WAIT_FOR_CONTENT = "wait_for_content"
    EXTRACT_CONTENT = "extract_content"
    SKIP_ELEMENT = "skip_element"
    STOP_NAVIGATION = "stop_navigation"


@dataclass
class NavigationDecision:
    """Decision made by agent about navigation."""

    action: NavigationAction
    target_element: DOMElement | None = None
    parameters: dict[str, Any] = None
    confidence: float = 1.0
    reasoning: str = ""

    def __post_init__(self):
        """Initialize default parameters if not provided."""
        if self.parameters is None:
            self.parameters = {}


@dataclass
class NavigationContext:
    """Context provided to agent for navigation decisions."""

    current_url: str
    page_title: str
    available_elements: list[DOMElement]
    extraction_goal: str  # e.g., "restaurant_menu", "product_catalog"
    previous_actions: list[NavigationDecision]
    page_state: dict[str, Any]


class AgentScoutBridge(ABC):
    """Bridge that allows AI Scout agents to control Playwright navigation."""

    @abstractmethod
    async def should_interact_with_element(
        self, element: DOMElement, context: NavigationContext
    ) -> NavigationDecision:
        """Ask agent if we should interact with this element."""
        pass

    @abstractmethod
    async def choose_navigation_strategy(
        self, available_elements: list[DOMElement], context: NavigationContext
    ) -> list[NavigationDecision]:
        """Ask agent to choose overall navigation strategy."""
        pass

    @abstractmethod
    async def should_extract_content(
        self, potential_content_elements: list[DOMElement], context: NavigationContext
    ) -> NavigationDecision:
        """Ask agent if current content should be extracted."""
        pass

    @abstractmethod
    async def is_navigation_complete(
        self, extracted_content: list[dict[str, Any]], context: NavigationContext
    ) -> bool:
        """Ask agent if navigation/extraction is complete."""
        pass


class LLMScoutBridge(AgentScoutBridge):
    """Implementation using LLM for AI Scout decisions."""

    def __init__(
        self,
        llm_client: Any,
        domain_config: dict[str, Any],
        custom_prompts: dict[str, str] | None = None,
    ):
        """Initialize with LLM client and domain configuration."""
        self.llm_client = llm_client
        self.domain_config = domain_config
        self.custom_prompts = custom_prompts or {}

        # Default prompts that can be overridden
        self.default_prompts = {
            "element_interaction": """
You are helping extract {extraction_goal} content from a website.

Current context:
- URL: {current_url}
- Page title: {page_title}
- Goal: {extraction_goal}

Element information:
- Tag: {element_tag}
- Text: {element_text}
- Attributes: {element_attributes}

Should I interact with this element? Consider:
1. Does this element likely lead to {extraction_goal} content?
2. Is this a navigation element (tab, button, link) for {extraction_goal}?
3. Will clicking this reveal more {extraction_goal} content?

Respond with: CLICK, SKIP, or EXTRACT
Reasoning: [brief explanation]
""",
            "navigation_strategy": """
You are planning navigation strategy for extracting {extraction_goal} content.

Current page has these interactive elements:
{elements_summary}

Goal: Extract {extraction_goal} content efficiently.

Plan the navigation sequence:
1. Which elements should be clicked first?
2. What content should be extracted?
3. When should navigation stop?

Respond with a prioritized list of actions.
""",
            "content_extraction": """
You are deciding whether to extract content for {extraction_goal}.

Available content elements found:
{content_summary}

Current extraction goal: {extraction_goal}
Already extracted: {previous_extractions} items

Should I extract content now?
- YES: If current elements contain good {extraction_goal} content
- NO: If more navigation is needed first
- DONE: If extraction is complete

Respond: YES, NO, or DONE
""",
            "completion_check": """
You are determining if {extraction_goal} extraction is complete.

Extracted so far:
- Total items: {total_items}
- Categories/sections: {categories}
- Quality assessment: {quality_summary}

Current goal: {extraction_goal}
Target coverage: {target_coverage}

Is the extraction complete and satisfactory?
Respond: COMPLETE or CONTINUE
Reasoning: [brief explanation]
""",
        }

    async def should_interact_with_element(
        self, element: DOMElement, context: NavigationContext
    ) -> NavigationDecision:
        """Use LLM to decide on element interaction."""
        # Access element properties directly from the dataclass
        prompt = self._get_prompt("element_interaction").format(
            extraction_goal=context.extraction_goal,
            current_url=context.current_url,
            page_title=context.page_title,
            element_tag=element.selector.split()[0] if element.selector else "unknown",
            element_text=element.text[:200],  # Truncate long text
            element_attributes=str(element.attributes),
        )

        try:
            response = await self._call_llm(prompt)
            decision_text = response.strip().upper()

            if decision_text.startswith("CLICK"):
                action = NavigationAction.CLICK_ELEMENT
            elif decision_text.startswith("EXTRACT"):
                action = NavigationAction.EXTRACT_CONTENT
            else:
                action = NavigationAction.SKIP_ELEMENT

            return NavigationDecision(
                action=action,
                target_element=element,
                confidence=0.8,  # Could extract from LLM response
                reasoning=response,
            )

        except Exception as e:
            # Fallback to conservative approach
            return NavigationDecision(
                action=NavigationAction.SKIP_ELEMENT, reasoning=f"LLM call failed: {e}"
            )

    async def choose_navigation_strategy(
        self, available_elements: list[DOMElement], context: NavigationContext
    ) -> list[NavigationDecision]:
        """Use LLM to plan navigation strategy."""
        # Summarize elements for LLM
        elements_summary = []
        for i, element in enumerate(available_elements[:10]):  # Limit for LLM
            tag_name = element.selector.split()[0] if element.selector else "unknown"
            elements_summary.append(f"{i + 1}. {tag_name}: '{element.text[:50]}...'")

        prompt = self._get_prompt("navigation_strategy").format(
            extraction_goal=context.extraction_goal,
            elements_summary="\n".join(elements_summary),
        )

        try:
            await self._call_llm(prompt)
            # Parse LLM response into decisions
            # This would need more sophisticated parsing in practice

            # For now, return a simple strategy
            decisions = []
            for element in available_elements[:3]:  # Interact with first 3
                decisions.append(
                    NavigationDecision(
                        action=NavigationAction.CLICK_ELEMENT,
                        target_element=element,
                        reasoning="LLM strategy planning",
                    )
                )

            return decisions

        except Exception as e:
            # Fallback strategy
            return [
                NavigationDecision(
                    action=NavigationAction.EXTRACT_CONTENT,
                    reasoning=f"Fallback due to LLM error: {e}",
                )
            ]

    async def should_extract_content(
        self, potential_content_elements: list[DOMElement], context: NavigationContext
    ) -> NavigationDecision:
        """Use LLM to decide on content extraction."""
        content_summary = (
            f"Found {len(potential_content_elements)} potential content elements"
        )

        prompt = self._get_prompt("content_extraction").format(
            extraction_goal=context.extraction_goal,
            content_summary=content_summary,
            previous_extractions=len(context.previous_actions),
        )

        try:
            response = await self._call_llm(prompt)

            if "YES" in response.upper():
                action = NavigationAction.EXTRACT_CONTENT
            elif "DONE" in response.upper():
                action = NavigationAction.STOP_NAVIGATION
            else:
                action = NavigationAction.SCROLL_PAGE

            return NavigationDecision(action=action, reasoning=response)

        except Exception as e:
            return NavigationDecision(
                action=NavigationAction.EXTRACT_CONTENT,
                reasoning=f"Fallback extraction due to error: {e}",
            )

    async def is_navigation_complete(
        self, extracted_content: list[dict[str, Any]], context: NavigationContext
    ) -> bool:
        """Use LLM to determine if extraction is complete."""
        prompt = self._get_prompt("completion_check").format(
            extraction_goal=context.extraction_goal,
            total_items=len(extracted_content),
            categories="[analysis would go here]",
            sections="[analysis would go here]",
            quality_summary=f"Extracted {len(extracted_content)} items",
            target_coverage=self.domain_config.get("target_coverage", "comprehensive"),
        )

        try:
            response = await self._call_llm(prompt)
            return "COMPLETE" in response.upper()

        except Exception:
            # Conservative: assume not complete on error
            return False

    def _get_prompt(self, prompt_type: str) -> str:
        """Get prompt template, allowing custom overrides."""
        return self.custom_prompts.get(prompt_type, self.default_prompts[prompt_type])

    async def _call_llm(self, prompt: str) -> str:
        """Call the LLM with error handling."""
        if hasattr(self.llm_client, "acreate_completion"):
            result = await self.llm_client.acreate_completion(prompt, max_tokens=200)
        else:
            # Use the async method if available, otherwise fallback to sync
            if hasattr(self.llm_client, "create_completion"):
                result = await self.llm_client.create_completion(prompt, max_tokens=200)
            else:
                # Sync fallback
                import asyncio

                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None,
                    lambda: self.llm_client.create_completion(prompt, max_tokens=200),
                )

        # Parse result based on your LLM client format
        if hasattr(result, "choices") and len(result.choices) > 0:
            return result.choices[0].message.content.strip()
        elif isinstance(result, dict) and "content" in result:
            return result["content"].strip()
        else:
            return str(result).strip()


class SimpleScoutBridge(AgentScoutBridge):
    """Simple rule-based scout for testing/fallback."""

    def __init__(self, domain_config: dict[str, Any]):
        """Initialize SimpleScoutBridge with domain configuration."""
        self.domain_config = domain_config
        self.target_keywords = domain_config.get("target_keywords", [])

    async def should_interact_with_element(
        self, element: DOMElement, context: NavigationContext
    ) -> NavigationDecision:
        """Simple keyword-based decision."""
        text = element.text
        text_lower = text.lower()

        # Check if element text contains target keywords
        for keyword in self.target_keywords:
            if keyword.lower() in text_lower:
                return NavigationDecision(
                    action=NavigationAction.CLICK_ELEMENT,
                    target_element=element,
                    confidence=0.7,
                    reasoning=f"Contains keyword: {keyword}",
                )

        return NavigationDecision(
            action=NavigationAction.SKIP_ELEMENT, reasoning="No target keywords found"
        )

    async def choose_navigation_strategy(
        self, available_elements: list[DOMElement], context: NavigationContext
    ) -> list[NavigationDecision]:
        """Simple strategy: interact with keyword-matching elements."""
        decisions = []

        for element in available_elements:
            decision = await self.should_interact_with_element(element, context)
            if decision.action != NavigationAction.SKIP_ELEMENT:
                decisions.append(decision)

        return decisions

    async def should_extract_content(
        self, potential_content_elements: list[DOMElement], context: NavigationContext
    ) -> NavigationDecision:
        """Extract if we have reasonable amount of content."""
        if len(potential_content_elements) > 3:
            return NavigationDecision(
                action=NavigationAction.EXTRACT_CONTENT,
                reasoning=f"Found {len(potential_content_elements)} content elements",
            )
        else:
            return NavigationDecision(
                action=NavigationAction.SCROLL_PAGE,
                reasoning="Need more content elements",
            )

    async def is_navigation_complete(
        self, extracted_content: list[dict[str, Any]], context: NavigationContext
    ) -> bool:
        """Complete if we have minimum target items."""
        min_items = self.domain_config.get("min_target_items", 5)
        return len(extracted_content) >= min_items
