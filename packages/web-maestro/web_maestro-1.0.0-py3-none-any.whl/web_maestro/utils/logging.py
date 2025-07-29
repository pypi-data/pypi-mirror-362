"""Internal logging utilities for web_maestro.

This module contains logging utilities used internally by web_maestro,
avoiding external dependencies for better portability.
"""

import logging
import textwrap
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models.types import CapturedBlock


def log_block_group(
    block_logger: logging.Logger,
    block_type: str,
    blocks: list["CapturedBlock"],
    max_items: int = 100,
    max_chars: int = 300,
    align_width: int = 22,
    wrap_width: int = 120,
) -> None:
    """Logs a compact, aligned group of blocks with a per-type emoji header and footer.

    Each block appears as:
        * <source_id> - <truncated content>

    Group format:
        📦 BEGIN BLOCK_TYPE
        * id          - content
        ...
        ✅ END BLOCK_TYPE

    Args:
        block_logger: The logger to emit messages through.
        block_type: The logical type of blocks (e.g., 'visible_dom').
        blocks: List of CapturedBlock.
        max_items: Max number of blocks to log.
        max_chars: Max content characters per line.
        align_width: Source ID alignment width.
        wrap_width (int): Width for text wrapping.
    """
    if not block_type or not blocks:
        return

    emoji = "📦"
    footer = "✅"

    block_logger.debug(f"{emoji} BEGIN {block_type.upper()}")

    for i, block in enumerate(blocks[:max_items]):
        source = block.source_id or f"{block_type}[{i}]"
        content = " ".join(block.content.strip().split())
        if len(content) > max_chars:
            content = content[:max_chars] + "..."

        prefix = f"* {source.ljust(align_width)} - "
        full_line = prefix + content

        wrapped_lines = textwrap.wrap(full_line, width=wrap_width)
        for j, line in enumerate(wrapped_lines):
            block_logger.debug(("    " if j > 0 else "") + line)

    if len(blocks) > max_items:
        block_logger.debug(f"... (and {len(blocks) - max_items} more)")

    block_logger.debug(f"{footer} END {block_type.upper()}")
