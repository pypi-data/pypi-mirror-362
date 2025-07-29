"""Enhanced PDF processing with multimodal vision support.

This module provides PDF processing capabilities using vision APIs as an alternative
to traditional OCR-based processing, offering better accuracy for complex layouts.
"""

import asyncio
import base64
from collections.abc import Callable
from io import BytesIO
import logging
from pathlib import Path
from string import Template
import tempfile
from typing import Any

try:
    from pdf2image import convert_from_path
    from PIL import Image

    PDF_DEPS_AVAILABLE = True
except ImportError:
    PDF_DEPS_AVAILABLE = False
    convert_from_path = None
    Image = None

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from web_maestro.providers.base import BaseLLMProvider

import aiohttp

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

logger = logging.getLogger(__name__)


def extract_text_from_pdf_file(pdf_path: Path, trace_id: str | None = None) -> str:
    """Extract text from PDF using available libraries.

    Args:
        pdf_path: Path to the PDF file
        trace_id: Optional trace ID for logging

    Returns:
        Extracted text content
    """
    trace = f"[trace={trace_id}] " if trace_id else ""

    # Validate file exists and has reasonable size
    if not pdf_path.exists():
        logger.error(f"{trace}❌ PDF file not found: {pdf_path}")
        return ""

    file_size = pdf_path.stat().st_size
    if file_size < 100:  # PDFs are typically larger than 100 bytes
        logger.warning(f"{trace}❌ PDF file too small: {file_size} bytes")
        return ""

    # Check PDF header to ensure it's actually a PDF
    try:
        with open(pdf_path, "rb") as f:
            header = f.read(4)
            if not header.startswith(b"%PDF"):
                logger.warning(
                    f"{trace}❌ File is not a PDF (no %PDF header): {pdf_path}"
                )
                return ""
    except Exception as e:
        logger.warning(f"{trace}❌ Could not read PDF header: {e}")
        return ""

    # Try pdfplumber first (better text extraction)
    if pdfplumber:
        try:
            logger.info(f"{trace}📄 Extracting text with pdfplumber")
            text_content = []
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(f"=== PAGE {page_num} ===\n{page_text}")
                        logger.debug(
                            f"{trace}📄 Extracted {len(page_text)} chars from page {page_num}"
                        )

            full_text = "\n\n".join(text_content)
            logger.info(
                f"{trace}✅ pdfplumber extracted {len(full_text)} total characters"
            )
            return full_text

        except Exception as e:
            logger.warning(f"{trace}⚠️ pdfplumber failed: {e}")

    # Fall back to PyPDF2
    if PyPDF2:
        try:
            logger.info(f"{trace}📄 Extracting text with PyPDF2")
            text_content = []
            with open(pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(reader.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(f"=== PAGE {page_num} ===\n{page_text}")
                        logger.debug(
                            f"{trace}📄 Extracted {len(page_text)} chars from page {page_num}"
                        )

            full_text = "\n\n".join(text_content)
            logger.info(f"{trace}✅ PyPDF2 extracted {len(full_text)} total characters")
            return full_text

        except Exception as e:
            logger.warning(f"{trace}⚠️ PyPDF2 failed: {e}")

    logger.error(f"{trace}❌ No PDF text extraction library available")
    return ""


async def extract_text_from_pdf_url_chunked(
    url: str,
    client: "BaseLLMProvider",
    cls_key: str,
    extraction_key: str | None,
    prompt: Template,
    trace_id: str | None = None,
    early_stop_after_n_valid: int | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Backward compatibility wrapper for non-streaming version."""
    return await extract_text_from_pdf_url_chunked_streaming(
        url=url,
        client=client,
        cls_key=cls_key,
        extraction_key=extraction_key,
        prompt=prompt,
        trace_id=trace_id,
        early_stop_after_n_valid=early_stop_after_n_valid,
        config=config,
        callback=None,
    )


async def extract_text_from_pdf_url_chunked_streaming(
    url: str,
    client: "BaseLLMProvider",
    cls_key: str,
    extraction_key: str | None,
    prompt: Template,
    trace_id: str | None = None,
    early_stop_after_n_valid: int | None = None,
    config: dict[str, Any] | None = None,
    callback: Callable | None = None,
) -> dict[str, Any]:
    """Extract text from PDF and process in chunks.

    Args:
        url: PDF URL to download and process
        client: LLM client for text processing
        cls_key: Classification key (e.g., "is_menu")
        extraction_key: Field to extract (e.g., "menu_items")
        prompt: Prompt template for extraction
        trace_id: Optional trace ID for logging
        early_stop_after_n_valid: Stop after finding this many valid chunks
        config: Optional configuration dict
        callback: Optional callback function during processing

    Returns:
        Extraction results from PDF text chunks
    """
    trace = f"[trace={trace_id}] " if trace_id else ""
    logger.info(f"{trace}📄 Processing PDF with text chunking: {url}")

    try:
        # Download PDF
        # Fetch binary content from URL
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                pdf_bytes = await response.read()
        if not pdf_bytes:
            logger.warning(f"{trace}❌ PDF download failed or returned no content")
            if extraction_key is None:
                return {cls_key: False}
            return {extraction_key: [], "currency": "USD"}

        # Validate it's actually a PDF before processing
        if len(pdf_bytes) < 100:
            logger.warning(
                f"{trace}❌ Downloaded content too small: {len(pdf_bytes)} bytes"
            )
            if extraction_key is None:
                return {cls_key: False, "error": "content_too_small"}
            return {extraction_key: [], "currency": "USD", "error": "content_too_small"}

        if not pdf_bytes.startswith(b"%PDF"):
            logger.warning(
                f"{trace}❌ Downloaded content is not a PDF (no %PDF header)"
            )
            if extraction_key is None:
                return {cls_key: False, "error": "not_pdf_content"}
            return {extraction_key: [], "currency": "USD", "error": "not_pdf_content"}

        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_bytes)
            tmp_file.flush()
            tmp_path = Path(tmp_file.name)

        # Extract text from PDF
        pdf_text = extract_text_from_pdf_file(tmp_path, trace_id)

        # Clean up temporary file
        try:
            tmp_path.unlink()
        except Exception as e:
            logger.debug(f"Failed to unlink temporary file: {e}")

        if not pdf_text or len(pdf_text.strip()) < 50:
            logger.warning(
                f"{trace}⚠️ PDF text extraction yielded little content ({len(pdf_text)} chars)"
            )
            if extraction_key is None:
                return {cls_key: False, "error": "insufficient_text"}
            return {extraction_key: [], "currency": "USD", "error": "insufficient_text"}

        logger.info(f"{trace}📝 Extracted {len(pdf_text)} characters from PDF")

        # Process text with streaming callback support
        import json

        from maestro.src.utils.text_processing import chunk_by_tokens_with_overlap

        # Early stop logic: only for validation mode
        early_stop = early_stop_after_n_valid if extraction_key is None else None

        if extraction_key is None:
            logger.info(
                f"{trace}🛑 Validation mode: early exit after {early_stop} valid chunks"
            )
        else:
            logger.info(
                f"{trace}📝 Extraction mode: processing ALL chunks for complete data"
            )

        # Create chunks for streaming processing
        chunk_config = {
            "max_tokens": config.get("chunk_max_tokens", 800) if config else 800,
            "overlap_tokens": (
                config.get("chunk_overlap_tokens", 200) if config else 200
            ),
        }

        chunks = chunk_by_tokens_with_overlap(
            pdf_text,
            max_tokens=chunk_config["max_tokens"],
            overlap_tokens=chunk_config["overlap_tokens"],
        )

        logger.info(
            f"{trace}📊 Created {len(chunks)} text chunks for streaming processing"
        )

        # Stream process chunks with callback
        processed_chunks = []
        valid_chunks_found = 0

        for i, chunk_text in enumerate(chunks):
            logger.info(f"{trace}🔄 Streaming chunk {i + 1}/{len(chunks)}")

            try:
                # Format prompt with chunk
                chunk_prompt = prompt.safe_substitute(chunk=chunk_text)

                # Process chunk with LLM
                response = await asyncio.to_thread(
                    client.create_completion,
                    content=chunk_prompt,
                    max_tokens=2048,
                    stream=False,
                )

                # Parse response
                if hasattr(response, "model_dump"):
                    result_dict = response.model_dump()
                else:
                    result_dict = response

                if result_dict and result_dict.get("choices"):
                    content = result_dict["choices"][0]["message"]["content"].strip()

                    # Clean response
                    if content.startswith("```"):
                        lines = content.splitlines()
                        if len(lines) >= 3:
                            content = "\n".join(lines[1:-1]).strip()
                        elif len(lines) == 2:
                            content = lines[1].strip()
                        elif len(lines) == 1 and content.endswith("```"):
                            content = content[3:-3].strip()
                            if content.startswith("json"):
                                content = content[4:].strip()

                    try:
                        chunk_result = json.loads(content)
                        chunk_result["chunk"] = chunk_text
                        chunk_result["chunk_index"] = i

                        # Check if this chunk contains target content
                        is_valid_chunk = chunk_result.get(cls_key, False)

                        if is_valid_chunk:
                            valid_chunks_found += 1
                            logger.info(
                                f"{trace}✅ Valid content detected in chunk {i + 1}!"
                            )

                            # Call callback if provided
                            if callback:
                                try:
                                    await callback(
                                        {
                                            "chunk_index": i,
                                            "is_valid": True,
                                            "chunk_result": chunk_result,
                                            "total_chunks": len(chunks),
                                            "valid_chunks_found": valid_chunks_found,
                                        }
                                    )
                                except Exception as e:
                                    logger.warning(f"{trace}⚠️ Callback failed: {e}")

                        processed_chunks.append(chunk_result)

                        # Early exit for validation mode
                        if (
                            extraction_key is None
                            and early_stop
                            and valid_chunks_found >= early_stop
                        ):
                            logger.info(
                                f"{trace}🎯 Early exit: Found {valid_chunks_found} valid chunks"
                            )
                            break

                    except json.JSONDecodeError as e:
                        logger.warning(
                            f"{trace}⚠️ Failed to parse chunk {i + 1} response: {e}"
                        )
                        processed_chunks.append(
                            {
                                cls_key: False,
                                "chunk": chunk_text,
                                "chunk_index": i,
                                "error": "parse_error",
                            }
                        )

            except Exception as e:
                logger.error(f"{trace}❌ Failed to process chunk {i + 1}: {e}")
                processed_chunks.append(
                    {
                        cls_key: False,
                        "chunk": chunk_text,
                        "chunk_index": i,
                        "error": str(e),
                    }
                )

        logger.info(
            f"{trace}📊 Processing complete: {len(processed_chunks)}/{len(chunks)} chunks"
        )

        # Create result in expected format
        result = {
            "chunks": processed_chunks,
            "streaming_mode": True,
            "chunks_processed": len(processed_chunks),
            "total_chunks": len(chunks),
            "early_exit": extraction_key is None
            and early_stop
            and valid_chunks_found >= early_stop,
        }

        # Transform result to match expected format
        if extraction_key is None:
            # Validation mode
            chunks = result.get("chunks", [])
            is_valid = any(chunk.get(cls_key) is True for chunk in chunks)
            logger.info(
                f"{trace}{'✅' if is_valid else '❌'} PDF validation: {cls_key}={is_valid}"
            )
            return {
                cls_key: is_valid,
                "chunks": chunks,
                "extraction_method": "text_chunking",
                "source": "pdf_text",
            }
        else:
            # Extraction mode
            chunks = result.get("chunks", [])
            extracted_items = []

            for chunk in chunks:
                if chunk.get(cls_key) is True and isinstance(
                    chunk.get("content", {}), dict
                ):
                    items = chunk["content"].get(extraction_key, [])
                    if isinstance(items, list):
                        extracted_items.extend(items)

            logger.info(
                f"{trace}✅ PDF extraction: {len(extracted_items)} items from {len(chunks)} chunks"
            )
            return {
                cls_key: len(extracted_items) > 0,
                extraction_key: extracted_items,
                "currency": "USD",
                "chunks": chunks,
                "extraction_method": "text_chunking",
                "source": "pdf_text",
            }

    except Exception as e:
        logger.error(f"{trace}❌ PDF text processing failed: {e}", exc_info=True)
        if extraction_key is None:
            return {cls_key: False, "error": str(e)}
        return {extraction_key: [], "currency": "USD", "error": str(e)}


def convert_pdf_to_images(
    pdf_path: Path, trace_id: str | None = None
) -> list["Image.Image"]:
    """Convert PDF pages to PIL Images for vision processing.

    Args:
        pdf_path: Path to the PDF file
        trace_id: Optional trace ID for logging

    Returns:
        List of PIL Images, one per page
    """
    trace = f"[trace={trace_id}] " if trace_id else ""

    if not PDF_DEPS_AVAILABLE:
        raise ImportError(
            "pdf2image and PIL are required for PDF to image conversion. Install with: pip install pdf2image pillow"
        )

    try:
        logger.info(f"{trace}📄 Converting PDF to images: {pdf_path}")
        images = convert_from_path(pdf_path, dpi=200)  # Higher DPI for better quality
        logger.info(f"{trace}🖼️ Converted {len(images)} page(s) to images")
        return images
    except Exception as e:
        logger.error(f"{trace}❌ Failed to convert PDF to images: {e}")
        return []


def image_to_base64(image: "Image.Image") -> str:
    """Convert PIL Image to base64 string for vision API.

    Args:
        image: PIL Image object

    Returns:
        Base64-encoded image string
    """
    if not PDF_DEPS_AVAILABLE:
        raise ImportError(
            "PIL is required for image to base64 conversion. Install with: pip install pillow"
        )

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


async def process_pdf_page_with_vision_chunked(
    image: "Image.Image",
    client: "BaseLLMProvider",
    cls_key: str,
    extraction_key: str | None,
    prompt: Template,
    page_number: int,
    trace_id: str | None = None,
    chunk_height: int = 1000,
    early_stop_after_n_valid: int | None = None,
) -> dict[str, Any]:
    """Process a PDF page using vision API with chunking.

    Args:
        image: PIL Image of the PDF page
        client: Multimodal client with vision capabilities
        cls_key: Classification key
        extraction_key: Field to extract
        prompt: Prompt template for extraction
        page_number: Page number for logging
        trace_id: Optional trace ID
        chunk_height: Height of each chunk in pixels
        early_stop_after_n_valid: Stop after finding this many valid chunks

    Returns:
        Extraction result for this page
    """
    trace = f"[trace={trace_id}] " if trace_id else ""

    # Get image dimensions
    width, height = image.size
    num_chunks = (height + chunk_height - 1) // chunk_height

    logger.info(
        f"{trace}📄 Splitting page {page_number} into {num_chunks} chunks for vision"
    )

    valid_chunks = 0
    all_results = []

    for i in range(num_chunks):
        # Calculate chunk boundaries
        top = i * chunk_height
        bottom = min((i + 1) * chunk_height, height)

        # Crop the image to get the chunk
        chunk_image = image.crop((0, top, width, bottom))

        logger.info(
            f"{trace}👁️ Processing chunk {i + 1}/{num_chunks} of page {page_number}"
        )

        # Process this chunk
        chunk_result = await process_pdf_page_with_vision(
            image=chunk_image,
            client=client,
            cls_key=cls_key,
            extraction_key=extraction_key,
            prompt=prompt,
            page_number=f"{page_number}_chunk_{i + 1}",
            trace_id=trace_id,
        )

        if chunk_result and chunk_result.get(cls_key):
            valid_chunks += 1
            all_results.append(chunk_result)

            # Early stop if configured
            if early_stop_after_n_valid and valid_chunks >= early_stop_after_n_valid:
                logger.info(
                    f"{trace}🎯 Early exit: Found {valid_chunks} valid chunks in page {page_number}"
                )
                break

    # Combine results
    if all_results:
        combined_result = {
            cls_key: True,
            "page_number": page_number,
            "extraction_method": "vision_api_chunked",
            "num_chunks": len(all_results),
            "source": "pdf_page",
        }

        # Merge extracted items if extraction mode
        if extraction_key:
            combined_items = []
            for result in all_results:
                if result.get(extraction_key):
                    combined_items.extend(result[extraction_key])
            combined_result[extraction_key] = combined_items

        return combined_result
    else:
        return {
            cls_key: False,
            "page_number": page_number,
            "extraction_method": "vision_api_chunked",
            "num_chunks": num_chunks,
            "source": "pdf_page",
        }


async def process_pdf_page_with_vision(
    image: "Image.Image",
    client: "BaseLLMProvider",
    cls_key: str,
    extraction_key: str | None,
    prompt: Template,
    page_number: int,
    trace_id: str | None = None,
) -> dict[str, Any]:
    """Process a single PDF page using vision API.

    Args:
        image: PIL Image of the PDF page
        client: Multimodal client with vision capabilities
        cls_key: Classification key
        extraction_key: Field to extract
        prompt: Prompt template for extraction
        page_number: Page number for logging
        trace_id: Optional trace ID

    Returns:
        Extraction result for this page
    """
    trace = f"[trace={trace_id}] " if trace_id else ""

    try:
        logger.info(f"{trace}👁️ Processing PDF page {page_number} with vision API")

        # Convert image to base64
        image_base64 = image_to_base64(image)

        # Create vision-specific prompt for PDF pages
        vision_prompt = f"""Analyze this PDF page and determine if it contains the target content.

        This is page {page_number} of a PDF document. Look for relevant content patterns.

        Return JSON with:
        - "{cls_key}": true if this page contains target content, false otherwise
        {'- "' + extraction_key + '": array of extracted items if relevant' if extraction_key else ""}
        - "page_number": {page_number}
        - "confidence": your confidence level (0-1)

        Extract all visible relevant content with details.
        """

        # Use vision API to analyze the page
        result = await client.create_vision_completion(
            text_prompt=vision_prompt, image_base64=image_base64, max_tokens=4096
        )

        if hasattr(result, "choices") and result.choices:
            content = result.choices[0].message.content
            try:
                import json

                # Clean the response
                content = content.strip()
                if content.startswith("```"):
                    lines = content.splitlines()
                    if len(lines) >= 3:
                        content = "\n".join(lines[1:-1]).strip()
                    elif len(lines) == 2:
                        content = lines[1].strip()
                    elif len(lines) == 1 and content.endswith("```"):
                        content = content[3:-3].strip()
                        if content.startswith("json"):
                            content = content[4:].strip()

                parsed_result = json.loads(content)

                # Add metadata
                parsed_result["page_number"] = page_number
                parsed_result["extraction_method"] = "vision_api"
                parsed_result["source"] = "pdf_page"

                logger.info(
                    f"{trace}✅ Vision API processed page {page_number}: "
                    f"{cls_key}={parsed_result.get(cls_key, False)}"
                )

                return parsed_result

            except json.JSONDecodeError as e:
                logger.warning(
                    f"{trace}⚠️ Failed to parse vision API response for page {page_number}: {e}"
                )
                logger.debug(f"{trace}⚠️ Raw content: {content[:200]}...")
                return {
                    cls_key: False,
                    "page_number": page_number,
                    "error": "parse_error",
                }
        else:
            logger.warning(
                f"{trace}⚠️ No valid response from vision API for page {page_number}"
            )
            return {cls_key: False, "page_number": page_number, "error": "no_response"}

    except Exception as e:
        logger.error(f"{trace}❌ Vision API failed for page {page_number}: {e}")
        return {cls_key: False, "page_number": page_number, "error": str(e)}


async def extract_text_from_pdf_url_multimodal(
    url: str,
    client: "BaseLLMProvider",
    cls_key: str,
    extraction_key: str | None,
    prompt: Template,
    trace_id: str | None = None,
    use_vision_api: bool = True,
    max_pages: int = 10,
    early_stop_after_n_valid: int | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Enhanced PDF extraction with multimodal vision support.

    Args:
        url: PDF URL to download and process
        client: LLM client (multimodal or standard)
        cls_key: Classification key
        extraction_key: Field to extract
        prompt: Prompt template for extraction
        trace_id: Optional trace ID
        use_vision_api: Whether to use vision API
        max_pages: Maximum pages to process
        early_stop_after_n_valid: Stop after finding this many valid pages
        config: Optional configuration dictionary

    Returns:
        Combined extraction results from all pages
    """
    trace = f"[trace={trace_id}] " if trace_id else ""
    logger.info(f"{trace}📄 Processing PDF with multimodal support: {url}")

    # All BaseProvider instances now support vision API
    has_vision_support = True

    if use_vision_api and not has_vision_support:
        logger.error(f"{trace}❌ Vision API requested but client doesn't support it.")
        if extraction_key is None:
            return {cls_key: False, "error": "no_vision_support"}
        return {extraction_key: [], "currency": "USD", "error": "no_vision_support"}

    try:
        # Download PDF
        # Fetch binary content from URL
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                pdf_bytes = await response.read()
        if not pdf_bytes:
            logger.warning(f"{trace}❌ PDF download failed or returned no content")
            if extraction_key is None:
                return {cls_key: False}
            return {extraction_key: [], "currency": "USD"}

        # Validate it's actually a PDF before processing
        if len(pdf_bytes) < 100:
            logger.warning(
                f"{trace}❌ Downloaded content too small: {len(pdf_bytes)} bytes"
            )
            if extraction_key is None:
                return {cls_key: False, "error": "content_too_small"}
            return {extraction_key: [], "currency": "USD", "error": "content_too_small"}

        if not pdf_bytes.startswith(b"%PDF"):
            logger.warning(
                f"{trace}❌ Downloaded content is not a PDF (no %PDF header)"
            )
            if extraction_key is None:
                return {cls_key: False, "error": "not_pdf_content"}
            return {extraction_key: [], "currency": "USD", "error": "not_pdf_content"}

        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(pdf_bytes)
            tmp_file.flush()
            tmp_path = Path(tmp_file.name)

        # Convert PDF to images
        images = convert_pdf_to_images(tmp_path, trace_id)
        if not images:
            logger.error(f"{trace}❌ Failed to convert PDF to images")
            if extraction_key is None:
                return {cls_key: False}
            return {extraction_key: [], "currency": "USD"}

        # Limit pages to process
        images = images[:max_pages]
        logger.info(f"{trace}📄 Processing {len(images)} pages (max: {max_pages})")

        # Process each page
        page_results = []
        valid_pages = 0

        for i, image in enumerate(images):
            page_num = i + 1
            page_result = None

            # Try vision API
            if use_vision_api and has_vision_support:
                try:
                    # Check if we should use chunking (only for validation)
                    use_chunking = (
                        config
                        and config.get("pdf_vision_chunking", False)
                        and extraction_key is None
                    )

                    if use_chunking:
                        # Use chunked processing for validation
                        chunk_height = config.get("pdf_chunk_height", 1000)
                        page_result = await process_pdf_page_with_vision_chunked(
                            image=image,
                            client=client,
                            cls_key=cls_key,
                            extraction_key=extraction_key,
                            prompt=prompt,
                            page_number=page_num,
                            trace_id=trace_id,
                            chunk_height=chunk_height,
                            early_stop_after_n_valid=early_stop_after_n_valid,
                        )
                    else:
                        # Use full page processing
                        page_result = await process_pdf_page_with_vision(
                            image=image,
                            client=client,
                            cls_key=cls_key,
                            extraction_key=extraction_key,
                            prompt=prompt,
                            page_number=page_num,
                            trace_id=trace_id,
                        )

                    if page_result.get("error"):
                        logger.warning(
                            f"{trace}⚠️ Vision API failed for page {page_num}"
                        )
                        page_result = None

                except Exception as e:
                    logger.warning(
                        f"{trace}⚠️ Vision API error for page {page_num}: {e}"
                    )
                    continue

            # No fallback - vision API only
            if page_result is None:
                logger.warning(
                    f"{trace}⚠️ Vision API failed for page {page_num}, no fallback"
                )
                page_result = {
                    cls_key: False,
                    "page_number": page_num,
                    "error": "vision_failed",
                }

            if page_result:
                page_results.append(page_result)

                # Check for early exit in validation mode
                if extraction_key is None and page_result.get(cls_key, False):
                    valid_pages += 1
                    logger.info(f"{trace}✅ Found valid content on page {page_num}")

                    # Early exit if we've found enough valid pages
                    if (
                        early_stop_after_n_valid
                        and valid_pages >= early_stop_after_n_valid
                    ):
                        logger.info(
                            f"{trace}🎯 Early exit: Found {valid_pages} valid page(s)"
                        )
                        # Return early with results so far
                        combined_result = {
                            cls_key: True,
                            "pages_processed": len(page_results),
                            "total_pages": len(images),
                            "page_results": page_results,
                            "early_exit": True,
                            "valid_pages_found": valid_pages,
                        }

                        # Clean up temporary file
                        try:
                            tmp_path.unlink()
                        except Exception as e:
                            logger.debug(
                                f"Failed to unlink temporary file during early exit: {e}"
                            )

                        return combined_result

        # Combine results from all pages
        if extraction_key is None:
            # Validation mode - return True if any page has target content
            any_page_valid = any(result.get(cls_key, False) for result in page_results)

            combined_result = {
                cls_key: any_page_valid,
                "pages_processed": len(page_results),
                "total_pages": len(images),
                "page_results": page_results,
            }

            logger.info(
                f"{trace}{'✅' if any_page_valid else '❌'} PDF validation: {cls_key}={any_page_valid}"
            )

        else:
            # Extraction mode - combine all items from all pages
            all_items = []
            valid_pages = 0

            for result in page_results:
                if result.get(cls_key, False):
                    valid_pages += 1
                    items = result.get(extraction_key, [])
                    all_items.extend(items)

            combined_result = {
                cls_key: len(all_items) > 0,
                extraction_key: all_items,
                "currency": "USD",
                "pages_processed": len(page_results),
                "total_pages": len(images),
                "valid_pages": valid_pages,
                "page_results": page_results,
            }

            logger.info(
                f"{trace}✅ PDF extraction complete: {len(all_items)} items from {valid_pages} pages"
            )

        # Clean up temporary file
        try:
            tmp_path.unlink()
        except Exception as e:
            logger.debug(f"Failed to unlink temporary file: {e}")

        return combined_result

    except Exception as e:
        logger.error(f"{trace}❌ PDF processing failed: {e}", exc_info=True)
        if extraction_key is None:
            return {cls_key: False}
        return {extraction_key: [], "currency": "USD", "error": str(e)}
