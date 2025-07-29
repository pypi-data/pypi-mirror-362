"""Generic data models for structured content."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class ContentType(Enum):
    """Generic content types - can be extended per domain."""

    ITEM = "item"
    CATEGORY = "category"
    SECTION = "section"
    METADATA = "metadata"
    UNKNOWN = "unknown"


@dataclass
class ContentItem:
    """Generic content item - domain-agnostic."""

    name: str
    content_type: ContentType = ContentType.ITEM
    metadata: dict[str, Any] = field(default_factory=dict)
    raw_text: str = ""
    confidence: float = 1.0
    source_element_id: str | None = None

    # Common fields that many domains use
    price: float | str | None = None
    description: str | None = None
    category: str | None = None
    tags: list[str] = field(default_factory=list)
    attributes: dict[str, str] = field(default_factory=dict)

    def get_field(self, field_name: str, default: Any = None) -> Any:
        """Get a field value, checking both direct attributes and metadata."""
        # Check direct attributes first
        if hasattr(self, field_name):
            value = getattr(self, field_name)
            if value is not None:
                return value

        # Check metadata
        return self.metadata.get(field_name, default)

    def set_field(self, field_name: str, value: Any) -> None:
        """Set a field value, using metadata for dynamic fields."""
        if hasattr(self, field_name):
            setattr(self, field_name, value)
        else:
            self.metadata[field_name] = value

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "name": self.name,
            "content_type": self.content_type.value,
            "metadata": self.metadata,
            "raw_text": self.raw_text,
            "confidence": self.confidence,
            "source_element_id": self.source_element_id,
            "price": self.price,
            "description": self.description,
            "category": self.category,
            "tags": self.tags,
            "attributes": self.attributes,
        }
        return {k: v for k, v in result.items() if v is not None}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ContentItem:
        """Create from dictionary."""
        content_type = data.get("content_type", "item")
        if isinstance(content_type, str):
            try:
                content_type = ContentType(content_type)
            except ValueError:
                content_type = ContentType.UNKNOWN

        return cls(
            name=data["name"],
            content_type=content_type,
            metadata=data.get("metadata", {}),
            raw_text=data.get("raw_text", ""),
            confidence=data.get("confidence", 1.0),
            source_element_id=data.get("source_element_id"),
            price=data.get("price"),
            description=data.get("description"),
            category=data.get("category"),
            tags=data.get("tags", []),
            attributes=data.get("attributes", {}),
        )


@dataclass
class ContentSection:
    """Generic content section."""

    name: str
    section_type: str = "default"
    items: list[ContentItem] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    description: str | None = None
    source_url: str | None = None
    extracted_at: datetime | None = None

    def add_item(self, item: ContentItem) -> None:
        """Add an item to this section."""
        self.items.append(item)

    def get_items_by_type(self, content_type: ContentType) -> list[ContentItem]:
        """Get items of a specific type."""
        return [item for item in self.items if item.content_type == content_type]

    def get_items_by_category(self, category: str) -> list[ContentItem]:
        """Get items in a specific category."""
        return [item for item in self.items if item.category == category]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "section_type": self.section_type,
            "items": [item.to_dict() for item in self.items],
            "metadata": self.metadata,
            "description": self.description,
            "source_url": self.source_url,
            "extracted_at": (
                self.extracted_at.isoformat() if self.extracted_at else None
            ),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ContentSection:
        """Create from dictionary."""
        return cls(
            name=data["name"],
            section_type=data.get("section_type", "default"),
            items=[ContentItem.from_dict(item) for item in data.get("items", [])],
            metadata=data.get("metadata", {}),
            description=data.get("description"),
            source_url=data.get("source_url"),
            extracted_at=(
                datetime.fromisoformat(data["extracted_at"])
                if data.get("extracted_at")
                else None
            ),
        )


@dataclass
class StructuredContent:
    """Generic structured content container."""

    source_name: str
    source_url: str
    domain: str  # e.g., "restaurant_menu", "ecommerce_catalog", "news_articles"
    sections: list[ContentSection] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.now)
    extraction_metadata: dict[str, Any] = field(default_factory=dict)
    validation_status: str | None = None
    total_items: int = field(init=False)

    def __post_init__(self):
        """Calculate total items after initialization."""
        self.total_items = sum(len(section.items) for section in self.sections)

    def add_section(self, section: ContentSection) -> None:
        """Add a section to the content."""
        self.sections.append(section)
        self.total_items = sum(len(section.items) for section in self.sections)

    def get_all_items(self) -> list[ContentItem]:
        """Get all items across all sections."""
        items = []
        for section in self.sections:
            items.extend(section.items)
        return items

    def get_items_by_type(self, content_type: ContentType) -> list[ContentItem]:
        """Get all items of a specific type."""
        items = []
        for section in self.sections:
            items.extend(section.get_items_by_type(content_type))
        return items

    def get_sections_by_type(self, section_type: str) -> list[ContentSection]:
        """Get sections of a specific type."""
        return [
            section for section in self.sections if section.section_type == section_type
        ]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "source_name": self.source_name,
            "source_url": self.source_url,
            "domain": self.domain,
            "sections": [section.to_dict() for section in self.sections],
            "last_updated": self.last_updated.isoformat(),
            "extraction_metadata": self.extraction_metadata,
            "validation_status": self.validation_status,
            "total_items": self.total_items,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StructuredContent:
        """Create from dictionary."""
        content = cls(
            source_name=data["source_name"],
            source_url=data["source_url"],
            domain=data["domain"],
            sections=[
                ContentSection.from_dict(section)
                for section in data.get("sections", [])
            ],
            last_updated=datetime.fromisoformat(data["last_updated"]),
            extraction_metadata=data.get("extraction_metadata", {}),
            validation_status=data.get("validation_status"),
        )
        return content


# Domain-specific helper functions
def create_menu_item(
    name: str,
    price: float | None = None,
    description: str | None = None,
    **kwargs,
) -> ContentItem:
    """Helper to create a menu item."""
    return ContentItem(
        name=name,
        price=price,
        description=description,
        content_type=ContentType.ITEM,
        category=kwargs.get("category", "menu_item"),
        metadata=kwargs,
    )


def create_product_item(name: str, price: float | None = None, **kwargs) -> ContentItem:
    """Helper to create a product item."""
    return ContentItem(
        name=name,
        price=price,
        content_type=ContentType.ITEM,
        category=kwargs.get("category", "product"),
        metadata=kwargs,
    )


def create_article_item(
    title: str, content: str | None = None, **kwargs
) -> ContentItem:
    """Helper to create an article item."""
    return ContentItem(
        name=title,
        description=content,
        content_type=ContentType.ITEM,
        category=kwargs.get("category", "article"),
        metadata=kwargs,
    )


ExtractedContent = StructuredContent
