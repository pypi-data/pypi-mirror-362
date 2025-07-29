"""Web content processing modules.

This package contains processors for various web content types:
- PDF processing with multimodal vision support
- HTML cleaning and text extraction
- Multimodal content extraction
"""

from .adapters import HTMLCleanerProcessor, JSONExtractorProcessor, MultimodalProcessor

# PDF processor may not be available if dependencies are missing
try:
    from .adapters import PDFProcessor
    from .pdf_processor import (
        convert_pdf_to_images,
        extract_text_from_pdf_file,
        extract_text_from_pdf_url_chunked,
        extract_text_from_pdf_url_chunked_streaming,
        extract_text_from_pdf_url_multimodal,
        image_to_base64,
        process_pdf_page_with_vision,
        process_pdf_page_with_vision_chunked,
    )

    PDF_PROCESSOR_AVAILABLE = True
except ImportError:
    PDFProcessor = None
    convert_pdf_to_images = None
    extract_text_from_pdf_file = None
    extract_text_from_pdf_url_chunked = None
    extract_text_from_pdf_url_chunked_streaming = None
    extract_text_from_pdf_url_multimodal = None
    image_to_base64 = None
    process_pdf_page_with_vision = None
    process_pdf_page_with_vision_chunked = None
    PDF_PROCESSOR_AVAILABLE = False

from .base import BaseProcessor, BlockFilterProcessor, ChainProcessor
from .html_cleaner import HTMLCleaner, create_html_cleaner
from .multimodal_extractor import (
    extract_content_from_image_url_multimodal,
    extract_document_from_image_url,
    extract_menu_from_image_url,
    extract_product_from_image_url,
)

# Build __all__ list conditionally based on available dependencies
__all__ = [
    # Base processors
    "BaseProcessor",
    "BlockFilterProcessor",
    "ChainProcessor",
    # Processor adapters
    "HTMLCleanerProcessor",
    "MultimodalProcessor",
    "JSONExtractorProcessor",
    # HTML cleaning
    "HTMLCleaner",
    "create_html_cleaner",
    # Multimodal extraction
    "extract_content_from_image_url_multimodal",
    "extract_menu_from_image_url",
    "extract_product_from_image_url",
    "extract_document_from_image_url",
]

# Add PDF-related exports only if dependencies are available
if PDF_PROCESSOR_AVAILABLE:
    __all__.extend(
        [
            "PDFProcessor",
            # PDF processing functions
            "extract_text_from_pdf_file",
            "extract_text_from_pdf_url_chunked",
            "extract_text_from_pdf_url_chunked_streaming",
            "extract_text_from_pdf_url_multimodal",
            "convert_pdf_to_images",
            "image_to_base64",
            "process_pdf_page_with_vision",
            "process_pdf_page_with_vision_chunked",
        ]
    )
