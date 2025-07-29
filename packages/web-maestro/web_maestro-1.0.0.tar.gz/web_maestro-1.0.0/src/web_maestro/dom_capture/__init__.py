"""dom_capture module within web_maestro.

This module provides functionality related to DOM capture.
"""

from playwright.sync_api import sync_playwright


def capture_dom(html_content: str) -> str:
    """Captures the DOM from given HTML content.

    Args:
        html_content: A string representing the HTML content.

    Returns:
        A string containing the captured DOM.

    Raises:
        Exception: If an error occurs during the Playwright operation.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_content(html_content)
            captured_dom = page.content()
            browser.close()
    except Exception as e:
        raise Exception(f"An error occurred during DOM capture: {e}") from e

    return captured_dom
