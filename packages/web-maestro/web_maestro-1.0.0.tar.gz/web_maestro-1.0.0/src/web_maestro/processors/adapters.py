"""Adapters to integrate existing processors with the ContentProcessor protocol."""

import json
import logging
from typing import Union

from ..dom_capture.capture import CapturedBlock
from ..models.content import ContentItem, ContentSection, StructuredContent
from .base import BaseProcessor
from .html_cleaner import HTMLCleaner
from .multimodal_extractor import (
    extract_content_from_image_url_multimodal,
    extract_menu_from_image_url,
    extract_product_from_image_url,
)

# PDF processor imports - may not be available if dependencies missing
try:
    from .pdf_processor import (
        PDF_DEPS_AVAILABLE,
        extract_text_from_pdf_url_chunked,
        extract_text_from_pdf_url_multimodal,
    )
except ImportError:
    PDF_DEPS_AVAILABLE = False
    extract_text_from_pdf_url_multimodal = None
    extract_text_from_pdf_url_chunked = None

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..providers.base import BaseProvider

logger = logging.getLogger(__name__)


class HTMLCleanerProcessor(BaseProcessor):
    """Adapter for HTMLCleaner to work as a ContentProcessor."""

    def __init__(self, **kwargs):
        """Initialize with HTMLCleaner configuration."""
        super().__init__(kwargs)
        self.cleaner = HTMLCleaner(self.config)

    async def _process_blocks(self, blocks: list[CapturedBlock]) -> StructuredContent:
        """Clean HTML content from blocks.

        Args:
            blocks: List of captured blocks

        Returns:
            Structured content with cleaned text
        """
        cleaned_items = []

        for block in blocks:
            if block.capture_type == "visible_text" and "<" in block.content:
                try:
                    cleaned_text = self.cleaner.clean_html(block.content)
                    if cleaned_text.strip():
                        cleaned_items.append(
                            ContentItem(
                                name="Cleaned Block",
                                description=cleaned_text[:500],
                                metadata={
                                    "source_id": block.source_id,
                                    "original_length": len(block.content),
                                    "cleaned_length": len(cleaned_text),
                                    "full_text": cleaned_text,
                                },
                            )
                        )
                except Exception as e:
                    logger.debug(f"Failed to clean block {block.source_id}: {e}")

        return StructuredContent(
            source_name="HTMLCleaner",
            source_url="",
            domain="html_cleaning",
            sections=[
                ContentSection(
                    name="Cleaned HTML Content",
                    items=cleaned_items,
                    metadata={"total_cleaned": len(cleaned_items)},
                )
            ],
            extraction_metadata={"processor": "HTMLCleanerProcessor"},
        )


class PDFProcessor(BaseProcessor):
    """Adapter for PDF processing capabilities."""

    def __init__(self, provider: Union["BaseProvider", None] = None, **kwargs):
        """Initialize with provider for vision-based extraction.

        Args:
            provider: Optional provider for vision API calls
            **kwargs: Additional configuration including:
                - method: "vision" or "text" (default: "vision")
                - chunk_size: Size of text chunks (default: 4000)
        """
        super().__init__(kwargs)
        self.provider = provider
        self.method = self.config.get("method", "vision")
        self.chunk_size = self.config.get("chunk_size", 4000)

    async def _process_blocks(self, blocks: list[CapturedBlock]) -> StructuredContent:
        """Extract PDF content from URL references in blocks.

        Args:
            blocks: List of captured blocks

        Returns:
            Structured content from PDFs
        """
        from string import Template

        pdf_items = []

        # Look for PDF URLs in blocks
        for block in blocks:
            if ".pdf" in block.content.lower():
                # Try to extract URLs from the block
                import re

                url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+\.pdf'
                urls = re.findall(url_pattern, block.content, re.IGNORECASE)

                for url in urls:
                    try:
                        if not PDF_DEPS_AVAILABLE:
                            content = "PDF processing not available - install dependencies: pip install pdf2image pillow"
                        elif (
                            self.method == "vision"
                            and self.provider
                            and extract_text_from_pdf_url_multimodal
                        ):
                            # Use multimodal extraction with default parameters
                            from string import Template

                            result = await extract_text_from_pdf_url_multimodal(
                                url,
                                self.provider,
                                cls_key="has_content",
                                extraction_key="content",
                                prompt=Template(
                                    "Extract all text from this PDF document."
                                ),
                                use_vision_api=True,
                            )
                            content = result.get("content", "") if result else ""
                        elif (
                            self.method == "text" and extract_text_from_pdf_url_chunked
                        ):
                            # Use chunked text extraction
                            result = await extract_text_from_pdf_url_chunked(
                                url, chunk_size=self.chunk_size
                            )
                            content = result if result else ""
                        else:
                            # PDF processing not available or method not supported
                            content = f"PDF text extraction from {url} (method: {self.method}) - limited functionality without vision dependencies"

                        pdf_items.append(
                            ContentItem(
                                name=f"PDF: {url.split('/')[-1]}",
                                description=content[:500] if content else "Empty PDF",
                                metadata={
                                    "url": url,
                                    "method": self.method,
                                    "content_length": len(content) if content else 0,
                                    "full_content": content,
                                },
                            )
                        )
                    except Exception as e:
                        logger.error(f"Failed to process PDF {url}: {e}")

        return StructuredContent(
            source_name="PDFProcessor",
            source_url="",
            domain="pdf_extraction",
            sections=[
                ContentSection(
                    name="PDF Content",
                    items=pdf_items,
                    metadata={"pdfs_processed": len(pdf_items)},
                )
            ],
            extraction_metadata={"processor": "PDFProcessor"},
        )


class MultimodalProcessor(BaseProcessor):
    """Adapter for multimodal image extraction."""

    def __init__(self, provider: "BaseProvider", content_type: str = "auto", **kwargs):
        """Initialize with provider for vision API.

        Args:
            provider: Provider for vision API calls
            content_type: Type of content to extract ("menu", "product", "document", "auto")
            **kwargs: Additional configuration
        """
        super().__init__(kwargs)
        self.provider = provider
        self.content_type = content_type

    async def _process_blocks(self, blocks: list[CapturedBlock]) -> StructuredContent:
        """Extract content from image URLs in blocks.

        Args:
            blocks: List of captured blocks

        Returns:
            Structured content from images
        """
        image_items = []

        # Look for image URLs in blocks
        for block in blocks:
            import re

            # Match common image extensions
            img_pattern = (
                r'https?://[^\s<>"{}|\\^`\[\]]+\.(?:jpg|jpeg|png|gif|webp|bmp)'
            )
            urls = re.findall(img_pattern, block.content, re.IGNORECASE)

            for url in urls:
                try:
                    if self.content_type == "menu":
                        result = await extract_menu_from_image_url(url, self.provider)
                    elif self.content_type == "product":
                        result = await extract_product_from_image_url(
                            url, self.provider
                        )
                    else:
                        # Auto-detect or generic extraction
                        result = await extract_content_from_image_url_multimodal(
                            url,
                            self.provider,
                            content_type="document",
                            classification_key="has_content",
                            extraction_key="content",
                        )

                    if result and isinstance(result, dict):
                        # Convert extracted data to ContentItem
                        name = result.get("name", f"Image: {url.split('/')[-1]}")
                        description = result.get("description", "")

                        # Handle different result formats
                        if "menu_items" in result:
                            description = f"Menu with {len(result['menu_items'])} items"
                        elif "products" in result:
                            description = (
                                f"Product catalog with {len(result['products'])} items"
                            )

                        image_items.append(
                            ContentItem(
                                name=name,
                                description=description[:500],
                                metadata={
                                    "url": url,
                                    "content_type": self.content_type,
                                    "extracted_data": result,
                                },
                            )
                        )
                except Exception as e:
                    logger.error(f"Failed to process image {url}: {e}")

        return StructuredContent(
            source_name="MultimodalProcessor",
            source_url="",
            domain="multimodal_extraction",
            sections=[
                ContentSection(
                    name="Image Content",
                    items=image_items,
                    metadata={"images_processed": len(image_items)},
                )
            ],
            extraction_metadata={"processor": "MultimodalProcessor"},
        )


class JSONExtractorProcessor(BaseProcessor):
    """Extract and structure JSON data from blocks."""

    async def _process_blocks(self, blocks: list[CapturedBlock]) -> StructuredContent:
        """Extract JSON data from blocks.

        Args:
            blocks: List of captured blocks

        Returns:
            Structured content from JSON data
        """
        json_items = []

        for block in blocks:
            if block.capture_type in ["json_script", "structured_blob"]:
                try:
                    # Try to parse the content as JSON
                    if "{" in block.content or "[" in block.content:
                        # Extract JSON-like content
                        import re

                        json_match = re.search(
                            r"(\{[^{}]*\}|\[[^\[\]]*\])", block.content
                        )
                        if json_match:
                            try:
                                data = json.loads(json_match.group(1))
                                json_items.append(
                                    ContentItem(
                                        name=f"JSON Data from {block.source_id}",
                                        description=str(data)[:200],
                                        metadata={
                                            "source_id": block.source_id,
                                            "data": data,
                                            "data_type": type(data).__name__,
                                        },
                                    )
                                )
                            except json.JSONDecodeError:
                                pass
                except Exception as e:
                    logger.debug(
                        f"Failed to extract JSON from block {block.source_id}: {e}"
                    )

        return StructuredContent(
            source_name="JSONExtractor",
            source_url="",
            domain="json_extraction",
            sections=[
                ContentSection(
                    name="Extracted JSON Data",
                    items=json_items,
                    metadata={"json_blocks_found": len(json_items)},
                )
            ],
            extraction_metadata={"processor": "JSONExtractorProcessor"},
        )
