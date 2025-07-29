"""Module for classifying elements using configurable AI Scout."""

import logging
from typing import Union

from ..config.llm_config import get_llm_client

logger = logging.getLogger(__name__)


def classify_element(
    label: str, classification_prompt: Union[str, None] = None
) -> bool:
    """Use LLM to classify whether an element matches the given criteria.

    Args:
        label: A string representing the element label to classify.
        classification_prompt: Custom prompt template for classification.
                             Should contain {label} placeholder.
                             If None, returns True (no filtering).

    Returns:
        A boolean indicating whether the element matches the classification criteria.
        Returns True if no prompt is provided (no filtering).
        Returns False if no LLM client is configured.

    Logs:
        The prompt, LLM response, and decision.
    """
    # If no prompt provided, don't filter
    if not classification_prompt:
        logger.debug(
            f"[AI-SCOUT] No classification prompt provided, accepting '{label}'"
        )
        return True

    client = get_llm_client()
    if not client or not client.is_available():
        logger.debug(
            f"[AI-SCOUT] No LLM client available, skipping classification for '{label}'"
        )
        return False

    # Format the prompt with the label
    prompt = classification_prompt.format(label=label)

    logger.debug(f"[AI-SCOUT] Prompt for label: '{label}' → {prompt!r}")

    response = client.create_completion(prompt, max_tokens=5)

    if response.error:
        logger.warning(f"[AI-SCOUT] LLM returned error: {response.error}")
        return False

    try:
        content = response.content.strip()
        logger.debug(f"[AI-SCOUT] Response for label '{label}': {content!r}")

        decision = content.lower().startswith("yes")
        logger.info(
            f"[AI-SCOUT] Element '{label}' → {'ACCEPTED' if decision else 'REJECTED'}"
        )
        return decision

    except Exception as err:
        logger.error(
            f"[AI-SCOUT] Failed to parse LLM response for label '{label}': {err}"
        )
        return False
