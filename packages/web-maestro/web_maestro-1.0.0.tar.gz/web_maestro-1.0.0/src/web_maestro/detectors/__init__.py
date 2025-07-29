"""Web content detection modules.

This package contains detectors for various web content types:
- Image detection for finding images in HTML
- Link detection for identifying content-specific links
- Element detection for interactive web elements
"""

from .element_detector import (
    ContentElementDetector,
    GenericContentElementDetector,
    analyze_elements_for_content,
    create_element_detector,
)
from .image_detector import (
    extract_images_from_playwright_blocks,
    extract_images_from_static_blocks,
    find_all_images_comprehensive,
    find_background_images,
    find_images_with_javascript,
    is_likely_content_image,
    is_valid_image_url,
    should_skip_image,
)
from .link_detector import (
    ContentLinkDetector,
    GenericContentLinkDetector,
    analyze_links_for_content,
    create_link_detector,
)

__all__ = [
    # Image detection
    "extract_images_from_static_blocks",
    "extract_images_from_playwright_blocks",
    "find_all_images_comprehensive",
    "find_background_images",
    "find_images_with_javascript",
    "is_likely_content_image",
    "is_valid_image_url",
    "should_skip_image",
    # Link detection
    "ContentLinkDetector",
    "GenericContentLinkDetector",
    "create_link_detector",
    "analyze_links_for_content",
    # Element detection
    "ContentElementDetector",
    "GenericContentElementDetector",
    "create_element_detector",
    "analyze_elements_for_content",
]
