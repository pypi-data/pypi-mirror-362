"""Enhanced text processing utilities for content extraction and LLM preparation.

This module provides enhanced versions of maestro's text processing utilities with:
- Token-aware chunking with overlap
- Semantic deduplication using embeddings
- Advanced text cleaning and normalization
- Performance optimizations for large documents
"""

import asyncio
import hashlib
import logging
import re
from typing import Any, Optional

try:
    import tiktoken

    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False

logger = logging.getLogger(__name__)


def count_tokens(text: str, encoding: str = "cl100k_base") -> int:
    """Count tokens in text using tiktoken.

    Args:
        text: Text to count tokens for
        encoding: Tiktoken encoding to use

    Returns:
        Number of tokens
    """
    if not TIKTOKEN_AVAILABLE:
        # Fallback to word count approximation
        return len(text.split()) * 1.3  # Rough approximation

    try:
        enc = tiktoken.get_encoding(encoding)
        return len(enc.encode(text))
    except Exception:
        # Fallback to word count
        return len(text.split()) * 1.3


def chunk_with_overlap(
    text: str,
    max_tokens: int = 1000,
    overlap_tokens: int = 100,
    respect_sentences: bool = True,
    encoding: str = "cl100k_base",
) -> list[dict[str, Any]]:
    """Chunk text with sliding window overlap for LLM processing.

    Args:
        text: Text to chunk
        max_tokens: Maximum tokens per chunk
        overlap_tokens: Number of tokens to overlap between chunks
        respect_sentences: Whether to break at sentence boundaries
        encoding: Tiktoken encoding to use

    Returns:
        List of chunk dictionaries with metadata
    """
    if not text.strip():
        return []

    if respect_sentences:
        return _chunk_by_sentences(text, max_tokens, overlap_tokens, encoding)
    else:
        return _chunk_by_tokens(text, max_tokens, overlap_tokens, encoding)


def _chunk_by_sentences(
    text: str, max_tokens: int, overlap_tokens: int, encoding: str
) -> list[dict[str, Any]]:
    """Chunk text by sentences while respecting token limits."""
    # Split into sentences
    sentences = _split_into_sentences(text)
    if not sentences:
        return []

    chunks = []
    current_chunk = []
    current_tokens = 0
    chunk_index = 0

    for _i, sentence in enumerate(sentences):
        sentence_tokens = count_tokens(sentence, encoding)

        # If single sentence exceeds max tokens, split it further
        if sentence_tokens > max_tokens:
            # Add current chunk if it has content
            if current_chunk:
                chunks.append(
                    _create_chunk_dict(
                        " ".join(current_chunk), chunk_index, current_tokens, encoding
                    )
                )
                chunk_index += 1
                current_chunk = []
                current_tokens = 0

            # Split the long sentence
            sub_chunks = _split_long_sentence(sentence, max_tokens, encoding)
            for sub_chunk in sub_chunks:
                chunks.append(
                    _create_chunk_dict(
                        sub_chunk,
                        chunk_index,
                        count_tokens(sub_chunk, encoding),
                        encoding,
                    )
                )
                chunk_index += 1
            continue

        # Check if adding this sentence would exceed limit
        if current_tokens + sentence_tokens > max_tokens and current_chunk:
            # Save current chunk
            chunks.append(
                _create_chunk_dict(
                    " ".join(current_chunk), chunk_index, current_tokens, encoding
                )
            )
            chunk_index += 1

            # Start new chunk with overlap
            overlap_sentences = _get_overlap_sentences(
                current_chunk, overlap_tokens, encoding
            )
            current_chunk = overlap_sentences
            current_tokens = sum(count_tokens(s, encoding) for s in current_chunk)

        current_chunk.append(sentence)
        current_tokens += sentence_tokens

    # Add final chunk if it has content
    if current_chunk:
        chunks.append(
            _create_chunk_dict(
                " ".join(current_chunk), chunk_index, current_tokens, encoding
            )
        )

    return chunks


def _chunk_by_tokens(
    text: str, max_tokens: int, overlap_tokens: int, encoding: str
) -> list[dict[str, Any]]:
    """Chunk text by tokens without respecting sentence boundaries."""
    if not TIKTOKEN_AVAILABLE:
        # Fallback to word-based chunking
        return _chunk_by_words(text, max_tokens, overlap_tokens)

    try:
        enc = tiktoken.get_encoding(encoding)
        tokens = enc.encode(text)

        chunks = []
        chunk_index = 0
        start = 0

        while start < len(tokens):
            end = start + max_tokens
            chunk_tokens = tokens[start:end]

            # Decode chunk
            chunk_text = enc.decode(chunk_tokens)

            chunks.append(
                _create_chunk_dict(chunk_text, chunk_index, len(chunk_tokens), encoding)
            )

            chunk_index += 1
            start = end - overlap_tokens

        return chunks

    except Exception:
        # Fallback to word-based chunking
        return _chunk_by_words(text, max_tokens, overlap_tokens)


def _chunk_by_words(
    text: str, max_tokens: int, overlap_tokens: int
) -> list[dict[str, Any]]:
    """Fallback word-based chunking when tiktoken is not available."""
    words = text.split()
    # Approximate: 1 token ≈ 0.75 words
    max_words = int(max_tokens * 0.75)
    overlap_words = int(overlap_tokens * 0.75)

    chunks = []
    chunk_index = 0
    start = 0

    while start < len(words):
        end = start + max_words
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)

        chunks.append(
            _create_chunk_dict(
                chunk_text,
                chunk_index,
                len(chunk_words),  # Word count as approximation
                "word_count",
            )
        )

        chunk_index += 1
        start = end - overlap_words

    return chunks


def _create_chunk_dict(
    text: str, index: int, token_count: int, encoding: str
) -> dict[str, Any]:
    """Create a standardized chunk dictionary."""
    return {
        "text": text,
        "index": index,
        "token_count": token_count,
        "char_count": len(text),
        "word_count": len(text.split()),
        "encoding": encoding,
        "hash": hashlib.sha256(text.encode()).hexdigest()[:16],
        "preview": text[:100] + "..." if len(text) > 100 else text,
    }


def _split_into_sentences(text: str) -> list[str]:
    """Split text into sentences using regex patterns."""
    # Pattern for sentence boundaries
    sentence_pattern = r"(?<=[.!?])\s+(?=[A-Z])"
    sentences = re.split(sentence_pattern, text)

    # Clean and filter sentences
    cleaned_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and len(sentence) > 10:  # Filter very short "sentences"
            cleaned_sentences.append(sentence)

    return cleaned_sentences


def _split_long_sentence(sentence: str, max_tokens: int, encoding: str) -> list[str]:
    """Split a sentence that's too long into smaller parts."""
    # Try splitting by commas first
    parts = sentence.split(",")
    if len(parts) > 1:
        result = []
        current_part = ""

        for part in parts:
            part = part.strip()
            if not part:
                continue

            test_part = current_part + ", " + part if current_part else part

            if count_tokens(test_part, encoding) <= max_tokens:
                current_part = test_part
            else:
                if current_part:
                    result.append(current_part)
                current_part = part

        if current_part:
            result.append(current_part)

        return result

    # Fallback: split by words
    words = sentence.split()
    max_words = int(max_tokens * 0.75)  # Conservative estimate

    result = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i : i + max_words])
        result.append(chunk)

    return result


def _get_overlap_sentences(
    sentences: list[str], overlap_tokens: int, encoding: str
) -> list[str]:
    """Get the last few sentences for overlap."""
    overlap_sentences = []
    current_tokens = 0

    # Work backwards from the end
    for sentence in reversed(sentences):
        sentence_tokens = count_tokens(sentence, encoding)
        if current_tokens + sentence_tokens > overlap_tokens:
            break

        overlap_sentences.insert(0, sentence)
        current_tokens += sentence_tokens

    return overlap_sentences


def semantic_deduplicate(
    chunks: list[str], similarity_threshold: float = 0.9
) -> list[str]:
    """Remove semantically similar chunks.

    Note: This is a simple implementation. For production, consider using
    sentence embeddings like SentenceTransformers.

    Args:
        chunks: List of text chunks
        similarity_threshold: Similarity threshold for deduplication

    Returns:
        Deduplicated list of chunks
    """
    if not chunks:
        return []

    # For now, use a simple hash-based approach
    # In production, this should use embeddings
    unique_chunks = []
    seen_hashes = set()

    for chunk in chunks:
        # Normalize chunk for comparison
        normalized = _normalize_for_comparison(chunk)
        chunk_hash = hashlib.sha256(normalized.encode()).hexdigest()

        if chunk_hash not in seen_hashes:
            seen_hashes.add(chunk_hash)
            unique_chunks.append(chunk)

    return unique_chunks


def _normalize_for_comparison(text: str) -> str:
    """Normalize text for similarity comparison."""
    # Convert to lowercase
    text = text.lower()

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove punctuation
    text = re.sub(r"[^\w\s]", "", text)

    return text.strip()


def clean_text(
    text: str,
    remove_urls: bool = True,
    remove_emails: bool = True,
    normalize_whitespace: bool = True,
    remove_special_chars: bool = False,
    preserve_structure: bool = True,
) -> str:
    """Clean text for LLM processing.

    Args:
        text: Text to clean
        remove_urls: Remove URLs from text
        remove_emails: Remove email addresses
        normalize_whitespace: Normalize whitespace
        remove_special_chars: Remove special characters
        preserve_structure: Preserve basic structure (paragraphs)

    Returns:
        Cleaned text
    """
    if not text:
        return ""

    cleaned = text

    # Remove URLs
    if remove_urls:
        cleaned = re.sub(r"https?://\S+|www\.\S+", "", cleaned)

    # Remove emails
    if remove_emails:
        cleaned = re.sub(r"\S+@\S+\.\S+", "", cleaned)

    # Remove special characters (but preserve basic punctuation)
    if remove_special_chars:
        cleaned = re.sub(r"[^\w\s\.\!\?\,\;\:\-\(\)]", "", cleaned)

    # Normalize whitespace
    if normalize_whitespace:
        if preserve_structure:
            # Preserve paragraph breaks but normalize other whitespace
            paragraphs = cleaned.split("\n\n")
            cleaned_paragraphs = []
            for para in paragraphs:
                para = re.sub(r"\s+", " ", para.strip())
                if para:
                    cleaned_paragraphs.append(para)
            cleaned = "\n\n".join(cleaned_paragraphs)
        else:
            # Normalize all whitespace
            cleaned = " ".join(cleaned.split())

    return cleaned.strip()


def get_content_hash(text: str) -> str:
    """Get a hash for content deduplication."""
    normalized = _normalize_for_comparison(text)
    return hashlib.sha256(normalized.encode()).hexdigest()


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format."""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.0f}s"
    else:
        hours = int(seconds // 3600)
        remaining_minutes = int((seconds % 3600) // 60)
        return f"{hours}h {remaining_minutes}m"


def truncate_text(text: str, max_length: int = 1000, suffix: str = "...") -> str:
    """Truncate text to maximum length."""
    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix


class TextProcessor:
    """Enhanced text processor with caching and optimization."""

    def __init__(self, encoding: str = "cl100k_base"):
        self.encoding = encoding
        self._token_cache: dict[str, int] = {}
        self._chunk_cache: dict[str, list[dict[str, Any]]] = {}

    def count_tokens_cached(self, text: str) -> int:
        """Count tokens with caching."""
        text_hash = hashlib.sha256(text.encode()).hexdigest()

        if text_hash in self._token_cache:
            return self._token_cache[text_hash]

        token_count = count_tokens(text, self.encoding)
        self._token_cache[text_hash] = token_count

        return token_count

    def chunk_text_cached(
        self,
        text: str,
        max_tokens: int = 1000,
        overlap_tokens: int = 100,
        respect_sentences: bool = True,
    ) -> list[dict[str, Any]]:
        """Chunk text with caching."""
        cache_key = hashlib.sha256(
            f"{text}:{max_tokens}:{overlap_tokens}:{respect_sentences}:{self.encoding}".encode()
        ).hexdigest()

        if cache_key in self._chunk_cache:
            return self._chunk_cache[cache_key]

        chunks = chunk_with_overlap(
            text, max_tokens, overlap_tokens, respect_sentences, self.encoding
        )

        self._chunk_cache[cache_key] = chunks
        return chunks

    async def process_large_text(
        self,
        text: str,
        max_tokens: int = 1000,
        overlap_tokens: int = 100,
        callback: Optional[callable] = None,
    ) -> list[dict[str, Any]]:
        """Process large text asynchronously with progress callback."""
        # Split into smaller parts for processing
        if len(text) > 100000:  # 100k characters
            parts = [
                text[i : i + 50000] for i in range(0, len(text), 45000)
            ]  # 5k overlap
            all_chunks = []

            for i, part in enumerate(parts):
                chunks = await asyncio.to_thread(
                    self.chunk_text_cached, part, max_tokens, overlap_tokens
                )
                all_chunks.extend(chunks)

                if callback:
                    await callback(i + 1, len(parts))

                # Yield control
                await asyncio.sleep(0)

            return all_chunks
        else:
            return await asyncio.to_thread(
                self.chunk_text_cached, text, max_tokens, overlap_tokens
            )

    def clear_cache(self):
        """Clear processing caches."""
        self._token_cache.clear()
        self._chunk_cache.clear()

    def get_cache_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        return {
            "token_cache_size": len(self._token_cache),
            "chunk_cache_size": len(self._chunk_cache),
            "encoding": self.encoding,
        }
