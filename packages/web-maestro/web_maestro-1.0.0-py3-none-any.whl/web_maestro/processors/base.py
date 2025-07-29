"""Base processor classes for content extraction pipeline."""

from abc import ABC, abstractmethod
import logging
from typing import Any

from ..dom_capture.capture import CapturedBlock
from ..interfaces.base import ContentProcessor
from ..models.content import ContentItem, ContentSection, StructuredContent

logger = logging.getLogger(__name__)


class BaseProcessor(ContentProcessor, ABC):
    """Base class for all content processors."""

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize processor with optional configuration.

        Args:
            config: Optional processor-specific configuration
        """
        self.config = config or {}

    async def process(self, blocks: list[CapturedBlock]) -> StructuredContent:
        """Process captured blocks into structured content.

        Args:
            blocks: List of captured DOM blocks

        Returns:
            Structured content extracted from blocks
        """
        try:
            return await self._process_blocks(blocks)
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__}: {e}")
            return StructuredContent(
                source_name=self.__class__.__name__,
                source_url="",
                domain="error",
                sections=[],
                extraction_metadata={
                    "error": str(e),
                    "processor": self.__class__.__name__,
                },
            )

    @abstractmethod
    async def _process_blocks(self, blocks: list[CapturedBlock]) -> StructuredContent:
        """Process blocks implementation to be defined by subclasses.

        Args:
            blocks: List of captured DOM blocks

        Returns:
            Structured content
        """
        pass


class BlockFilterProcessor(BaseProcessor):
    """Processor that filters blocks based on capture type."""

    def __init__(self, capture_types: list[str] | None = None, **kwargs):
        """Initialize with capture types to filter.

        Args:
            capture_types: List of capture types to include
            **kwargs: Additional configuration
        """
        super().__init__(kwargs)
        self.capture_types = capture_types or []

    async def _process_blocks(self, blocks: list[CapturedBlock]) -> StructuredContent:
        """Filter blocks by capture type.

        Args:
            blocks: List of captured blocks

        Returns:
            Structured content with filtered blocks
        """
        filtered_blocks = [
            block
            for block in blocks
            if not self.capture_types or block.capture_type in self.capture_types
        ]

        items = [
            ContentItem(
                name=f"Block {i}",
                description=block.content[:200],
                metadata={
                    "source_id": block.source_id,
                    "capture_type": block.capture_type,
                    "full_content": block.content,
                },
            )
            for i, block in enumerate(filtered_blocks)
        ]

        return StructuredContent(
            source_name="BlockFilter",
            source_url="",
            domain="block_filtering",
            sections=[
                ContentSection(
                    name="Filtered Content",
                    items=items,
                    metadata={
                        "total_blocks": len(blocks),
                        "filtered_blocks": len(items),
                    },
                )
            ],
            extraction_metadata={"processor": "BlockFilterProcessor"},
        )


class ChainProcessor(BaseProcessor):
    """Processor that chains multiple processors together."""

    def __init__(self, processors: list[BaseProcessor], **kwargs):
        """Initialize with list of processors to chain.

        Args:
            processors: List of processors to execute in sequence
            **kwargs: Additional configuration
        """
        super().__init__(kwargs)
        self.processors = processors

    async def _process_blocks(self, blocks: list[CapturedBlock]) -> StructuredContent:
        """Process blocks through each processor in the chain.

        Args:
            blocks: List of captured blocks

        Returns:
            Combined structured content from all processors
        """
        all_sections = []

        for processor in self.processors:
            result = await processor.process(blocks)
            all_sections.extend(result.sections)

        return StructuredContent(
            source_name="ProcessorChain",
            source_url="",
            domain="multi_processor",
            sections=all_sections,
            extraction_metadata={
                "processor_chain": [p.__class__.__name__ for p in self.processors],
                "total_sections": len(all_sections),
            },
        )
