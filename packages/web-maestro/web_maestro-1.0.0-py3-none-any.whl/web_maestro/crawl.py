"""Link crawling functionality for web_maestro.

This module provides depth-based link crawling capabilities, allowing
recursive exploration of websites by following links to a specified depth.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Callable
from urllib.parse import urljoin, urlparse

from .context import SessionContext
from .fetch import fetch_rendered_html
from .models.types import CapturedBlock

logger = logging.getLogger(__name__)


def normalize_url(url: str) -> str:
    """Normalize URL by ensuring it has a scheme and removing fragments."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # Parse and rebuild without fragment
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}" + (
        f"?{parsed.query}" if parsed.query else ""
    )


def is_same_domain(url1: str, url2: str) -> bool:
    """Check if two URLs belong to the same domain."""
    domain1 = urlparse(url1).netloc.lower()
    domain2 = urlparse(url2).netloc.lower()

    # Remove www. prefix for comparison
    domain1 = domain1.replace("www.", "")
    domain2 = domain2.replace("www.", "")

    return domain1 == domain2


def extract_links_from_blocks(blocks: list[CapturedBlock], base_url: str) -> set[str]:
    """Extract all links from captured blocks.

    Args:
        blocks: List of captured content blocks
        base_url: Base URL for resolving relative links

    Returns:
        Set of absolute URLs found in the blocks
    """
    links = set()

    for block in blocks:
        # Look for hyperlink blocks
        if hasattr(block, "capture_type") and block.capture_type == "hyperlinks":
            # Extract URLs from hyperlink content
            content = block.content
            if isinstance(content, str):
                # Simple extraction - look for URLs in the text
                import re

                url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+|/[^\s<>"{}|\\^`\[\]]+'
                found_urls = re.findall(url_pattern, content)

                for url in found_urls:
                    if url.startswith("/"):
                        # Relative URL
                        absolute_url = urljoin(base_url, url)
                    else:
                        absolute_url = url

                    # Normalize and add
                    normalized = normalize_url(absolute_url)
                    links.add(normalized)

        # Also check text blocks for URLs
        elif hasattr(block, "capture_type") and block.capture_type == "text":
            import re

            # Look for href patterns in text content
            href_pattern = r'href=["\']([^"\']+)["\']'
            matches = re.findall(href_pattern, block.content)

            for url in matches:
                if url.startswith(("http://", "https://")):
                    links.add(normalize_url(url))
                elif url.startswith("/"):
                    absolute_url = urljoin(base_url, url)
                    links.add(normalize_url(absolute_url))

    return links


async def crawl_with_depth(
    url: str,
    max_depth: int = 0,
    ctx: SessionContext | None = None,
    config: dict[str, Any] | None = None,
    content_processor: Callable[[str, list[CapturedBlock]], Any] | None = None,
    link_filter: Callable[[str, str], bool] | None = None,
    visited: set[str] | None = None,
    current_depth: int = 0,
    same_domain_only: bool = True,
    max_pages: int = 50,
) -> dict[str, Any]:
    """Crawl a website to a specified depth, following links recursively.

    Args:
        url: Starting URL to crawl
        max_depth: Maximum depth to crawl (0 = current page only)
        ctx: Session context
        config: Configuration for fetch_rendered_html
        content_processor: Optional function to process content from each page
        link_filter: Optional function to filter links (returns True to follow)
        visited: Set of already visited URLs (used internally for recursion)
        current_depth: Current recursion depth (used internally)
        same_domain_only: If True, only follow links on the same domain
        max_pages: Maximum number of pages to crawl (safety limit)

    Returns:
        Dict containing:
            - url: The crawled URL
            - depth: The depth at which this URL was found
            - content: Captured blocks from the page
            - links: Links found on the page
            - processed_result: Result from content_processor if provided
            - children: List of child page results (recursive)
    """
    if visited is None:
        visited = set()

    # Normalize URL
    normalized_url = normalize_url(url)

    # Check if already visited or exceeded limits
    if normalized_url in visited:
        logger.debug(f"Skipping already visited URL: {normalized_url}")
        return None

    if len(visited) >= max_pages:
        logger.warning(
            f"Reached maximum page limit ({max_pages}), skipping: {normalized_url}"
        )
        return None

    # Mark as visited
    visited.add(normalized_url)

    logger.info(f"🕷️ Crawling URL at depth {current_depth}: {normalized_url}")

    # Create context if not provided
    if ctx is None:
        ctx = SessionContext()

    # Fetch the page content
    blocks = await fetch_rendered_html(normalized_url, ctx, config)

    if not blocks:
        logger.warning(f"Failed to fetch content from: {normalized_url}")
        return {
            "url": normalized_url,
            "depth": current_depth,
            "content": [],
            "links": [],
            "processed_result": None,
            "children": [],
        }

    # Extract links from the page
    found_links = extract_links_from_blocks(blocks, normalized_url)

    # Filter links if needed
    if same_domain_only:
        found_links = {
            link for link in found_links if is_same_domain(normalized_url, link)
        }

    if link_filter:
        found_links = {
            link for link in found_links if link_filter(normalized_url, link)
        }

    logger.info(f"Found {len(found_links)} links on {normalized_url}")

    # Process content if processor provided
    processed_result = None
    if content_processor:
        try:
            processed_result = await content_processor(normalized_url, blocks)
        except Exception as e:
            logger.error(f"Error processing content for {normalized_url}: {e}")

    # Prepare result
    result = {
        "url": normalized_url,
        "depth": current_depth,
        "content": blocks,
        "links": list(found_links),
        "processed_result": processed_result,
        "children": [],
    }

    # Recursively crawl child pages if not at max depth
    if current_depth < max_depth and found_links:
        logger.info(f"Following {len(found_links)} links from {normalized_url}")

        # Crawl child pages concurrently but with some limit
        max_concurrent = config.get("max_concurrent_crawls", 5) if config else 5

        async def crawl_child(child_url: str):
            return await crawl_with_depth(
                url=child_url,
                max_depth=max_depth,
                ctx=ctx,
                config=config,
                content_processor=content_processor,
                link_filter=link_filter,
                visited=visited,
                current_depth=current_depth + 1,
                same_domain_only=same_domain_only,
                max_pages=max_pages,
            )

        # Process in batches to avoid overwhelming the server
        children_results = []
        link_list = list(found_links)

        for i in range(0, len(link_list), max_concurrent):
            batch = link_list[i : i + max_concurrent]
            batch_tasks = [crawl_child(child_url) for child_url in batch]
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)

            for res in batch_results:
                if isinstance(res, Exception):
                    logger.error(f"Error crawling child page: {res}")
                elif res is not None:
                    children_results.append(res)

        result["children"] = children_results

    return result


def flatten_crawl_results(crawl_result: dict[str, Any]) -> list[dict[str, Any]]:
    """Flatten hierarchical crawl results into a flat list.

    Args:
        crawl_result: Hierarchical crawl result from crawl_with_depth

    Returns:
        List of all pages crawled, flattened
    """
    if not crawl_result:
        return []

    pages = []

    # Add current page
    page_info = {
        "url": crawl_result["url"],
        "depth": crawl_result["depth"],
        "links_found": len(crawl_result.get("links", [])),
        "blocks_captured": len(crawl_result.get("content", [])),
        "processed_result": crawl_result.get("processed_result"),
    }
    pages.append(page_info)

    # Recursively add children
    for child in crawl_result.get("children", []):
        pages.extend(flatten_crawl_results(child))

    return pages
