"""Enhanced extraction module with multimodal vision support for image content.

This module provides an alternative to OCR-based image extraction by using
vision-capable models to directly analyze images for structured content extraction.
"""

import json
import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from web_maestro.providers.base import BaseLLMProvider

logger = logging.getLogger(__name__)


async def extract_content_from_image_url_multimodal(
    url: str,
    client: "BaseLLMProvider",
    content_type: str,
    classification_key: str,
    extraction_key: str | None = None,
    trace_id: str | None = None,
    use_vision_api: bool = True,
    custom_prompt: str | None = None,
) -> dict[str, Any]:
    """Extract structured content from an image URL using vision API.

    This function can use vision APIs to directly analyze images for any type
    of structured content without OCR, providing better accuracy for complex layouts.

    Args:
        url: Remote image URL (e.g. JPG, PNG, WebP).
        client: LLM client interface (standard or multimodal).
        content_type: Type of content to extract (e.g., "menu", "product", "document").
        classification_key: Classification key (e.g., "is_menu", "is_product").
        extraction_key: Structured field to extract (e.g., "menu_items", "products").
                       If None, only classification is performed.
        trace_id: Optional trace ID for logging context.
        use_vision_api: Whether to use vision API.
        custom_prompt: Optional custom prompt for specific extraction needs.

    Returns:
        Extracted structured content, or fallback result on failure.
    """
    trace = f"[trace={trace_id}] " if trace_id else ""

    # All BaseProvider instances now support vision API
    has_vision_support = True

    # Guardrail: Prevent PDFs from being processed as images
    if url.lower().endswith(".pdf"):
        logger.error(f"{trace}❌ PDF URL passed to image handler: {url}")
        logger.error(
            f"{trace}❌ PDFs should be routed to PDF handler, not image handler"
        )
        if extraction_key is None:
            return {classification_key: False}
        return {extraction_key: [], "currency": "USD", "error": "pdf_in_image_handler"}

    # Try vision API first if available
    if use_vision_api and has_vision_support:
        logger.info(f"{trace}👁️ Using vision API to analyze image: {url}")

        try:
            # Create a vision-specific prompt
            if custom_prompt:
                vision_prompt = custom_prompt
            else:
                vision_prompt = f"""Analyze this image and determine if it contains {content_type} content.

                Classification: Is this a {content_type}? Answer with a boolean {classification_key} field.

                {"Extraction: If this is a " + content_type + ", extract all relevant items with their details." if extraction_key else ""}

                Return your response in JSON format with:
                - "{classification_key}": true/false
                {'- "' + extraction_key + '": array of extracted items' if extraction_key else ""}
                {'- "currency": detected currency (default "USD")' if extraction_key else ""}
                """

            # Create messages with image URL for vision analysis
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": vision_prompt},
                        {"type": "image_url", "image_url": {"url": url}},
                    ],
                }
            ]

            # Use the multimodal client to analyze the image
            completion = await client.create_completion_async(
                messages=messages, max_tokens=1000
            )

            # Extract response content
            if hasattr(completion, "choices") and len(completion.choices) > 0:
                response_text = completion.choices[0].message.content

                # Clean up response text - remove markdown code blocks if present
                response_text = response_text.strip()
                if response_text.startswith("```json"):
                    response_text = response_text[7:]  # Remove ```json
                if response_text.startswith("```"):
                    response_text = response_text[3:]  # Remove ```
                if response_text.endswith("```"):
                    response_text = response_text[:-3]  # Remove trailing ```

                # Parse JSON response
                try:
                    result = json.loads(response_text)

                    # Add metadata
                    result["extraction_method"] = "vision_api"
                    result["source"] = "image_url"
                    result["content_type"] = content_type

                    # Log successful extraction
                    classification_result = result.get(classification_key, False)
                    item_count = (
                        len(result.get(extraction_key, [])) if extraction_key else 0
                    )

                    logger.info(
                        f"{trace}✅ Vision API analysis: {classification_key}={classification_result}"
                        f"{f', extracted {item_count} items' if extraction_key else ''}"
                    )

                    return result

                except json.JSONDecodeError as e:
                    logger.warning(
                        f"{trace}⚠️ Failed to parse vision API response as JSON: {e}"
                    )
                    logger.debug(f"{trace}Raw response: {response_text[:200]}...")

                    # Return error result
                    if extraction_key is None:
                        return {classification_key: False, "error": "json_parse_error"}
                    return {
                        extraction_key: [],
                        "currency": "USD",
                        "error": "json_parse_error",
                    }

            else:
                logger.warning(f"{trace}⚠️ No response from vision API")
                if extraction_key is None:
                    return {classification_key: False, "error": "no_response"}
                return {extraction_key: [], "currency": "USD", "error": "no_response"}

        except Exception as e:
            logger.error(f"{trace}❌ Vision API failed: {e}")
            if extraction_key is None:
                return {classification_key: False, "error": str(e)}
            return {extraction_key: [], "currency": "USD", "error": str(e)}

    else:
        # Vision API not available or not requested
        logger.warning(
            f"{trace}⚠️ Vision API not available or not enabled for image: {url}"
        )
        if extraction_key is None:
            return {classification_key: False, "error": "no_vision_support"}
        return {extraction_key: [], "currency": "USD", "error": "no_vision_support"}


# Convenience function for common content types
async def extract_menu_from_image_url(
    url: str,
    client: "BaseLLMProvider",
    trace_id: str | None = None,
    extraction_only: bool = False,
) -> dict[str, Any]:
    """Extract menu content from an image URL - convenience function.

    Args:
        url: Image URL to analyze
        client: Multimodal LLM client
        trace_id: Optional trace ID for logging
        extraction_only: If True, extract items; if False, only classify

    Returns:
        Menu extraction results
    """
    return await extract_content_from_image_url_multimodal(
        url=url,
        client=client,
        content_type="menu",
        classification_key="is_menu",
        extraction_key="menu_items" if extraction_only else None,
        trace_id=trace_id,
    )


async def extract_product_from_image_url(
    url: str,
    client: "BaseLLMProvider",
    trace_id: str | None = None,
    extraction_only: bool = False,
) -> dict[str, Any]:
    """Extract product content from an image URL - convenience function.

    Args:
        url: Image URL to analyze
        client: Multimodal LLM client
        trace_id: Optional trace ID for logging
        extraction_only: If True, extract items; if False, only classify

    Returns:
        Product extraction results
    """
    return await extract_content_from_image_url_multimodal(
        url=url,
        client=client,
        content_type="product catalog",
        classification_key="is_product_catalog",
        extraction_key="products" if extraction_only else None,
        trace_id=trace_id,
    )


async def extract_document_from_image_url(
    url: str,
    client: "BaseLLMProvider",
    trace_id: str | None = None,
    extraction_only: bool = False,
) -> dict[str, Any]:
    """Extract document content from an image URL - convenience function.

    Args:
        url: Image URL to analyze
        client: Multimodal LLM client
        trace_id: Optional trace ID for logging
        extraction_only: If True, extract content; if False, only classify

    Returns:
        Document extraction results
    """
    return await extract_content_from_image_url_multimodal(
        url=url,
        client=client,
        content_type="document",
        classification_key="is_document",
        extraction_key="content" if extraction_only else None,
        trace_id=trace_id,
    )
