"""Image detection utilities for finding embedded images in HTML content.

This module provides functionality to detect and extract image URLs from HTML
content, focusing on web-specific image detection that could be processed with vision APIs.
"""

import logging
from typing import Any, Union
from urllib.parse import urljoin, urlparse
import warnings

from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

from ..models.types import CapturedBlock

logger = logging.getLogger(__name__)

# Common image file extensions
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".tiff"}

# Default content keywords (can be overridden by caller)
DEFAULT_CONTENT_KEYWORDS = set()


def is_likely_content_image(
    img_tag: Any, img_url: str, keywords: Union[set[str], None] = None
) -> bool:
    """Determine if an image is likely to contain target content based on context clues.

    Args:
        img_tag: BeautifulSoup img tag object
        img_url: The resolved image URL
        keywords: Optional set of keywords to match against

    Returns:
        True if the image is likely to contain target content
    """
    if not keywords:
        return True  # If no keywords provided, all images are potentially relevant

    # Check alt text
    alt_text = (img_tag.get("alt") or "").lower()
    if any(keyword in alt_text for keyword in keywords):
        return True

    # Check src attribute
    src_text = (img_tag.get("src") or "").lower()
    if any(keyword in src_text for keyword in keywords):
        return True

    # Check title attribute
    title_text = (img_tag.get("title") or "").lower()
    if any(keyword in title_text for keyword in keywords):
        return True

    # Check CSS classes
    css_classes = " ".join(img_tag.get("class", [])).lower()
    if any(keyword in css_classes for keyword in keywords):
        return True

    # Check parent element context
    parent = img_tag.parent
    if parent:
        parent_text = parent.get_text().lower()
        if any(keyword in parent_text for keyword in keywords):
            return True

    return False


def is_valid_image_url(url: str) -> bool:
    """Check if a URL is a valid image URL.

    Args:
        url: The URL to validate

    Returns:
        True if the URL appears to be a valid image
    """
    if not url:
        return False

    parsed = urlparse(url)

    # Must have a valid scheme
    if parsed.scheme not in {"http", "https"}:
        return False

    # Must have a domain
    if not parsed.netloc:
        return False

    # Check if it has an image extension
    path_lower = parsed.path.lower()
    if any(path_lower.endswith(ext) for ext in IMAGE_EXTENSIONS):
        return True

    # Data URLs for base64 images
    if url.startswith("data:image/"):
        return True

    return False


def should_skip_image(img_tag: Any, img_url: str) -> tuple[bool, str]:
    """Determine if an image should be skipped based on optimization rules.

    Args:
        img_tag: BeautifulSoup img tag object
        img_url: The resolved image URL

    Returns:
        Tuple of (should_skip, reason)
    """
    # Skip tracking pixels and tiny images
    width = img_tag.get("width")
    height = img_tag.get("height")

    if width and height:
        try:
            w = int(str(width).rstrip("px"))
            h = int(str(height).rstrip("px"))
            if w < 50 or h < 50:
                return True, f"Image too small: {w}x{h}"
        except (ValueError, TypeError):
            pass

    # Skip common non-content images
    url_lower = img_url.lower()
    skip_patterns = [
        "pixel",
        "tracking",
        "analytics",
        "spacer",
        "blank",
        "clear.gif",
        "1x1",
        "placeholder",
        "loading",
    ]

    if any(pattern in url_lower for pattern in skip_patterns):
        return True, "Tracking/placeholder image"

    return False, ""


async def extract_images_from_static_blocks(
    blocks: list[CapturedBlock],
    base_url: str,
    max_images: int = 10,
    filter_by_keywords: bool = False,
    keywords: Union[set[str], None] = None,
    exclude_patterns: Union[list[str], None] = None,
) -> list[CapturedBlock]:
    """Extract image URLs from captured static HTML blocks.

    Args:
        blocks: Input HTML content blocks
        base_url: Used to resolve relative image URLs
        max_images: Maximum number of images to return
        filter_by_keywords: If True, only return images that match keywords
        keywords: Optional set of keywords to filter images
        exclude_patterns: Optional list of URL patterns to exclude

    Returns:
        List of image blocks with metadata
    """
    seen: set[str] = set()
    collected: list[CapturedBlock] = []

    for block_idx, block in enumerate(blocks):
        try:
            warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
            soup = BeautifulSoup(block.content, "html.parser")

            # Find all img tags with src attribute
            for img_idx, img_tag in enumerate(soup.find_all("img", src=True)):
                try:
                    src = img_tag.get("src", "").strip()
                    if not src:
                        continue

                    # Resolve relative URLs
                    full_url = urljoin(base_url, src)

                    # Skip if we've already seen this image
                    if full_url in seen:
                        continue

                    # Validate the image URL
                    if not is_valid_image_url(full_url):
                        continue

                    # Apply image optimization rules
                    should_skip, skip_reason = should_skip_image(img_tag, full_url)
                    if should_skip:
                        logger.debug(f"Skipping image {full_url}: {skip_reason}")
                        continue

                    # Apply filtering if requested
                    if filter_by_keywords:
                        # Apply keyword filtering
                        if keywords and not is_likely_content_image(
                            img_tag, full_url, keywords
                        ):
                            continue

                    # Apply exclusion patterns
                    if exclude_patterns:
                        if any(
                            pattern in full_url.lower() for pattern in exclude_patterns
                        ):
                            continue

                    seen.add(full_url)

                    # Create source ID
                    source_id = (
                        img_tag.get("id")
                        or f"img[{img_idx}]"
                        or f"block_{block_idx}_img_{img_idx}"
                    )

                    collected.append(
                        CapturedBlock(
                            content=full_url, source_id=source_id, capture_type="image"
                        )
                    )

                    if len(collected) >= max_images:
                        logger.info(f"🖼️ Reached max images limit ({max_images})")
                        return collected

                except Exception as e:
                    logger.debug(
                        f"🖼️ Failed to process image {img_idx} in block {block_idx}: {type(e).__name__}: {e}"
                    )
                    continue

        except Exception as e:
            logger.warning(
                f"🚨 Failed to parse HTML in block {block_idx}: {type(e).__name__}: {e}"
            )
            continue

    logger.info(
        f"🖼️ Extracted {len(collected)} <img> tag images from {len(blocks)} blocks"
    )

    # Also look for CSS background images
    try:
        background_images = find_background_images(blocks, base_url)
        logger.info(f"🎨 Found {len(background_images)} CSS background images")

        for bg_url in background_images:
            if len(collected) >= max_images:
                break

            # Create a block for the background image
            collected.append(
                CapturedBlock(
                    content=bg_url,
                    source_id="css_background",
                    capture_type="background_image",
                )
            )
    except Exception as e:
        logger.warning(f"Error finding background images: {e}")

    logger.info(f"🖼️ Total extracted: {len(collected)} images from {len(blocks)} blocks")
    return collected


def extract_images_from_playwright_blocks(
    blocks: list[CapturedBlock],
    base_url: str,
    max_images: int = 10,
    filter_by_keywords: bool = False,
    keywords: Union[set[str], None] = None,
) -> list[dict[str, Any]]:
    """Extract image URLs from Playwright-rendered HTML blocks.

    Args:
        blocks: List of captured blocks from Playwright rendering
        base_url: Base URL for resolving relative links
        max_images: Maximum number of images to return
        filter_by_keywords: If True, only return images that match keywords
        keywords: Optional set of keywords to filter images

    Returns:
        List of image dictionaries with metadata
    """
    seen: set[str] = set()
    collected: list[dict[str, Any]] = []

    for block in blocks:
        try:
            warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
            soup = BeautifulSoup(block.content, "html.parser")

            for img_tag in soup.find_all("img", src=True):
                src = img_tag.get("src")
                if not src:
                    continue

                full_url = urljoin(base_url, str(src))

                if full_url in seen or not is_valid_image_url(full_url):
                    continue

                seen.add(full_url)

                collected.append(
                    {
                        "url": full_url,
                        "alt": img_tag.get("alt", ""),
                        "title": img_tag.get("title", ""),
                        "css_classes": " ".join(img_tag.get("class", [])),
                        "matches_keywords": (
                            is_likely_content_image(img_tag, full_url, keywords)
                            if keywords
                            else False
                        ),
                    }
                )

                if len(collected) >= max_images:
                    break

        except Exception as e:
            logger.debug(f"Error processing block: {e}")
            continue

    return collected


def find_background_images(blocks: list[CapturedBlock], base_url: str) -> list[str]:
    """Find CSS background images in HTML blocks.

    Args:
        blocks: HTML content blocks
        base_url: Base URL for resolving relative URLs

    Returns:
        List of background image URLs
    """
    background_images = []

    for block in blocks:
        try:
            warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
            soup = BeautifulSoup(block.content, "html.parser")

            # Look for elements with style attributes containing background-image
            for element in soup.find_all(style=True):
                style = element.get("style", "")
                if "background-image" in style:
                    # Simple regex to extract URL from background-image: url(...)
                    import re

                    matches = re.findall(
                        r'background-image:\s*url\(["\']?([^"\']+)["\']?\)', style
                    )
                    for match in matches:
                        full_url = urljoin(base_url, match)
                        if is_valid_image_url(full_url):
                            background_images.append(full_url)

        except Exception as e:
            logger.debug(f"Error extracting background images: {e}")
            continue

    return background_images


async def find_images_with_javascript(page, base_url: str) -> list[str]:
    """Find all images on a page using JavaScript execution in Playwright.

    This function runs after the page is fully loaded and can find images
    that were added dynamically by JavaScript frameworks.

    Args:
        page: Playwright page object
        base_url: Base URL for resolving relative URLs

    Returns:
        List of image URLs found via JavaScript
    """
    try:
        # JavaScript to find all images including background images and lazy-loaded content
        js_code = """
        () => {
            const images = [];

            // 1. Find all <img> elements (including hidden ones)
            document.querySelectorAll('img').forEach(img => {
                const src = img.src || img.getAttribute('data-src') || img.getAttribute('data-lazy-src');
                if (src && src.startsWith('http')) {
                    images.push({
                        url: src,
                        type: 'img_tag',
                        alt: img.alt || '',
                        classes: img.className || ''
                    });
                }
            });

            // 2. Find CSS background images in computed styles
            document.querySelectorAll('*').forEach(element => {
                const style = window.getComputedStyle(element);
                const bgImage = style.backgroundImage;
                if (bgImage && bgImage !== 'none') {
                    const matches = bgImage.match(/url\\(["\']?([^"\']+)["\']?\\)/g);
                    if (matches) {
                        matches.forEach(match => {
                            const url = match.replace(/url\\(["\']?([^"\']+)["\']?\\)/, '$1');
                            if (url.startsWith('http')) {
                                images.push({
                                    url: url,
                                    type: 'background_image',
                                    alt: element.getAttribute('aria-label') || '',
                                    classes: element.className || ''
                                });
                            }
                        });
                    }
                }
            });

            // 3. Look for images in inline styles
            document.querySelectorAll('[style*="background-image"]').forEach(element => {
                const style = element.getAttribute('style');
                const matches = style.match(/background-image:\\s*url\\(["\']?([^"\']+)["\']?\\)/g);
                if (matches) {
                    matches.forEach(match => {
                        const url = match.replace(/background-image:\\s*url\\(["\']?([^"\']+)["\']?\\)/, '$1');
                        if (url.startsWith('http')) {
                            images.push({
                                url: url,
                                type: 'inline_background',
                                alt: element.getAttribute('aria-label') || '',
                                classes: element.className || ''
                            });
                        }
                    });
                }
            });

            // Remove duplicates and return
            const seen = new Set();
            return images.filter(img => {
                if (seen.has(img.url)) return false;
                seen.add(img.url);
                return true;
            });
        }
        """

        # Execute the JavaScript and get results
        js_images = await page.evaluate(js_code)

        # Include ALL images - no keyword filtering
        all_image_urls = [img_data["url"] for img_data in js_images]

        logger.info(f"🔍 JavaScript found {len(js_images)} total images")
        return all_image_urls

    except Exception as e:
        logger.warning(f"JavaScript image detection failed: {e}")
        return []


async def find_all_images_comprehensive(
    url: str,
    html_blocks: Union[list[CapturedBlock], None] = None,
    max_images: int = 10,
    use_playwright: bool = True,
    keywords: Union[set[str], None] = None,
    exclude_patterns: Union[list[str], None] = None,
) -> list[CapturedBlock]:
    """Comprehensive image detection using multiple methods.

    This function combines:
    1. HTML parsing for <img> tags
    2. CSS background image detection
    3. JavaScript-based dynamic image detection (if Playwright available)
    4. Data-src and lazy loading attribute detection

    Args:
        url: The URL to analyze
        html_blocks: Pre-fetched HTML blocks (optional)
        max_images: Maximum images to return
        use_playwright: Whether to use JavaScript detection with Playwright
        keywords: Optional set of keywords to filter images
        exclude_patterns: Optional list of URL patterns to exclude

    Returns:
        List of image blocks found using all methods
    """
    logger.info(f"🔍 Starting comprehensive image detection for {url}")
    all_images = []
    seen_urls = set()

    # Method 1: Parse HTML blocks if provided
    if html_blocks:
        logger.info("📄 Method 1: Parsing HTML blocks...")
        html_images = await extract_images_from_static_blocks(
            blocks=html_blocks,
            base_url=url,
            max_images=max_images,
            filter_by_keywords=bool(keywords),
            keywords=keywords,
            exclude_patterns=exclude_patterns,
        )

        for img in html_images:
            img_url = img.content
            if img_url not in seen_urls:
                seen_urls.add(img_url)
                all_images.append(img)

        logger.info(f"📄 Found {len(html_images)} images from HTML parsing")

    # Method 2: JavaScript-based detection (if Playwright available)
    if use_playwright and len(all_images) < max_images:
        logger.info("🔧 Method 2: JavaScript-based detection...")
        try:
            from ..context import SessionContext
            from ..core.browser_setup import setup_browser

            ctx = SessionContext()
            playwright, browser, context, page, _ = await setup_browser(ctx=ctx)

            if page:
                # Navigate to the page
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)

                # Wait for any dynamic content to load
                await page.wait_for_timeout(3000)

                # Run JavaScript image detection
                js_images = await find_images_with_javascript(page, url)

                # Convert JS results to CapturedBlock format
                for js_url in js_images:
                    if js_url not in seen_urls and len(all_images) < max_images:
                        seen_urls.add(js_url)
                        all_images.append(
                            CapturedBlock(
                                content=js_url,
                                source_id="js_detection",
                                capture_type="javascript_image",
                            )
                        )

                logger.info(
                    f"🔧 Found {len(js_images)} additional images from JavaScript"
                )

                # Cleanup
                await browser.close()

        except Exception as e:
            logger.warning(f"JavaScript detection failed: {e}")

    # Method 3: Static content fallback
    if not html_blocks and len(all_images) < max_images:
        logger.info("🌐 Method 3: Static content fallback...")
        try:
            from ..utils.static_fetcher import try_static_first

            static_blocks = await try_static_first(url)
            if static_blocks:
                static_images = await extract_images_from_static_blocks(
                    blocks=static_blocks,
                    base_url=url,
                    max_images=max_images - len(all_images),
                    filter_by_keywords=bool(keywords),
                    keywords=keywords,
                    exclude_patterns=exclude_patterns,
                )

                for img in static_images:
                    img_url = img.content
                    if img_url not in seen_urls:
                        seen_urls.add(img_url)
                        all_images.append(img)

                logger.info(
                    f"🌐 Found {len(static_images)} images from static fallback"
                )

        except Exception as e:
            logger.warning(f"Static fallback failed: {e}")

    logger.info(
        f"✅ Comprehensive detection complete: {len(all_images)} total images found"
    )
    return all_images[:max_images]
