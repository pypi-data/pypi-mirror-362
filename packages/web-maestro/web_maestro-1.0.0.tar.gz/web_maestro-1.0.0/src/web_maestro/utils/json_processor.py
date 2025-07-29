"""Enhanced JSON processing utilities for LLM responses and structured data.

This module provides enhanced versions of maestro's JSON utilities with:
- Better LLM response parsing (handles markdown code blocks)
- Streaming JSON parsing for large responses
- Safe JSON operations with fallbacks
- Schema validation support
"""

import asyncio
from collections.abc import Iterator
import json
import logging
import re
from typing import Any, Optional, Union

logger = logging.getLogger(__name__)


def safe_json_parse(text: str, fallback: Any = None) -> Any:
    """Safely parse JSON from text with fallback handling.

    This function handles common LLM response patterns like:
    - JSON wrapped in markdown code blocks
    - Mixed text with JSON content
    - Malformed JSON with trailing commas
    - Comments in JSON

    Args:
        text: Text that may contain JSON
        fallback: Value to return if parsing fails

    Returns:
        Parsed JSON data or fallback value
    """
    if not text or not isinstance(text, str):
        return fallback

    # Try direct parsing first
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass

    # Try to extract JSON from markdown code blocks
    json_match = re.search(
        r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE
    )
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    # Try to find JSON-like content
    json_pattern = r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}"
    matches = re.findall(json_pattern, text, re.DOTALL)

    for match in matches:
        try:
            # Clean up common issues
            cleaned = _clean_json_string(match)
            return json.loads(cleaned)
        except json.JSONDecodeError:
            continue

    # Try line-by-line for partial JSON
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.strip().startswith("{"):
            # Try to parse from this line onwards
            remaining_text = "\n".join(lines[i:])
            try:
                return json.loads(remaining_text)
            except json.JSONDecodeError:
                continue

    logger.warning(f"Failed to parse JSON from text: {text[:200]}...")
    return fallback


def _clean_json_string(text: str) -> str:
    """Clean JSON string by removing common issues."""
    # Remove trailing commas
    text = re.sub(r",(\s*[}\]])", r"\1", text)

    # Remove comments
    text = re.sub(r"//.*?$", "", text, flags=re.MULTILINE)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)

    # Fix single quotes
    text = re.sub(r"'([^']*)':", r'"\1":', text)

    return text


def extract_json_from_text(
    text: str, multiple: bool = False
) -> Union[dict[str, Any], list[dict[str, Any]], None]:
    """Extract JSON objects from mixed text content.

    Args:
        text: Text containing JSON objects
        multiple: Whether to extract multiple JSON objects

    Returns:
        Single JSON object, list of JSON objects, or None
    """
    if not text:
        return None

    # Pattern to match JSON objects
    json_pattern = r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}"
    matches = re.findall(json_pattern, text, re.DOTALL)

    valid_objects = []

    for match in matches:
        try:
            cleaned = _clean_json_string(match)
            obj = json.loads(cleaned)
            valid_objects.append(obj)
        except json.JSONDecodeError:
            continue

    if not valid_objects:
        return None

    if multiple:
        return valid_objects
    else:
        return valid_objects[0]


def merge_json_safely(obj1: dict[str, Any], obj2: dict[str, Any]) -> dict[str, Any]:
    """Safely merge two JSON objects with conflict resolution.

    Args:
        obj1: First JSON object
        obj2: Second JSON object (takes precedence)

    Returns:
        Merged JSON object
    """
    if not isinstance(obj1, dict) or not isinstance(obj2, dict):
        return obj2 if obj2 is not None else obj1

    result = obj1.copy()

    for key, value in obj2.items():
        if key in result:
            if isinstance(result[key], dict) and isinstance(value, dict):
                # Recursively merge nested dictionaries
                result[key] = merge_json_safely(result[key], value)
            elif isinstance(result[key], list) and isinstance(value, list):
                # Merge lists by extending
                result[key] = result[key] + value
            else:
                # obj2 takes precedence
                result[key] = value
        else:
            result[key] = value

    return result


def validate_json_fields(
    obj: dict[str, Any],
    required_fields: list[str],
    optional_fields: Optional[list[str]] = None,
) -> dict[str, Any]:
    """Validate JSON object has required fields.

    Args:
        obj: JSON object to validate
        required_fields: List of required field names
        optional_fields: List of optional field names

    Returns:
        Validation result with errors and warnings
    """
    result = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "missing_required": [],
        "unexpected_fields": [],
    }

    if not isinstance(obj, dict):
        result["valid"] = False
        result["errors"].append("Object is not a dictionary")
        return result

    # Check required fields
    for field in required_fields:
        if field not in obj:
            result["missing_required"].append(field)
            result["errors"].append(f"Missing required field: {field}")
            result["valid"] = False

    # Check for unexpected fields
    expected_fields = set(required_fields)
    if optional_fields:
        expected_fields.update(optional_fields)

    for field in obj.keys():
        if field not in expected_fields:
            result["unexpected_fields"].append(field)
            result["warnings"].append(f"Unexpected field: {field}")

    return result


def create_json_fallback(
    template: dict[str, Any], error_message: str = "JSON parsing failed"
) -> dict[str, Any]:
    """Create a fallback JSON object based on a template.

    Args:
        template: Template object with default values
        error_message: Error message to include

    Returns:
        Fallback JSON object
    """
    fallback = template.copy()
    fallback["_error"] = error_message
    fallback["_fallback"] = True
    return fallback


class JSONStreamParser:
    """Parser for streaming JSON responses from LLMs."""

    def __init__(self, buffer_size: int = 8192):
        self.buffer_size = buffer_size
        self.buffer = ""
        self.depth = 0
        self.in_string = False
        self.escape_next = False
        self.objects = []

    def feed(self, chunk: str) -> list[dict[str, Any]]:
        """Feed a chunk of text to the parser.

        Args:
            chunk: Text chunk to parse

        Returns:
            List of complete JSON objects found
        """
        self.buffer += chunk
        return self._parse_buffer()

    def _parse_buffer(self) -> list[dict[str, Any]]:
        """Parse the current buffer for complete JSON objects."""
        complete_objects = []
        start_pos = 0

        for i, char in enumerate(self.buffer):
            if self.escape_next:
                self.escape_next = False
                continue

            if char == "\\":
                self.escape_next = True
                continue

            if char == '"' and not self.escape_next:
                self.in_string = not self.in_string
                continue

            if self.in_string:
                continue

            if char == "{":
                if self.depth == 0:
                    start_pos = i
                self.depth += 1
            elif char == "}":
                self.depth -= 1
                if self.depth == 0:
                    # Found complete object
                    obj_str = self.buffer[start_pos : i + 1]
                    try:
                        obj = json.loads(obj_str)
                        complete_objects.append(obj)
                    except json.JSONDecodeError:
                        # Try cleaning the JSON
                        try:
                            cleaned = _clean_json_string(obj_str)
                            obj = json.loads(cleaned)
                            complete_objects.append(obj)
                        except json.JSONDecodeError:
                            logger.warning(
                                f"Failed to parse JSON object: {obj_str[:100]}..."
                            )

        # Remove processed content from buffer
        if complete_objects and start_pos >= 0:
            last_obj_end = self.buffer.rfind("}") + 1
            self.buffer = self.buffer[last_obj_end:].lstrip()
            self.depth = 0
            self.in_string = False
            self.escape_next = False

        return complete_objects

    def finalize(self) -> list[dict[str, Any]]:
        """Finalize parsing and return any remaining objects.

        Returns:
            List of any remaining JSON objects
        """
        if self.buffer.strip():
            # Try to parse remaining buffer
            try:
                remaining = safe_json_parse(self.buffer)
                if remaining:
                    return [remaining]
            except Exception as e:
                logger.debug(f"JSON line parsing failed: {e}")

        return []


class JSONProcessor:
    """Enhanced JSON processor with LLM response handling."""

    def __init__(self):
        self.stream_parser = JSONStreamParser()

    async def process_llm_response(self, response_text: str) -> dict[str, Any]:
        """Process an LLM response and extract JSON.

        Args:
            response_text: Raw LLM response text

        Returns:
            Dictionary with parsed JSON and metadata
        """
        result = {
            "success": False,
            "data": None,
            "error": None,
            "parsing_method": None,
            "raw_text": response_text[:1000],  # Store first 1000 chars
        }

        try:
            # Try direct parsing first
            data = safe_json_parse(response_text)
            if data is not None:
                result["success"] = True
                result["data"] = data
                result["parsing_method"] = "direct"
                return result

            # Try extraction from mixed text
            data = extract_json_from_text(response_text)
            if data is not None:
                result["success"] = True
                result["data"] = data
                result["parsing_method"] = "extraction"
                return result

            # Failed to parse
            result["error"] = "No valid JSON found in response"

        except Exception as e:
            result["error"] = str(e)

        return result

    async def process_stream_async(self, stream: Iterator[str]) -> list[dict[str, Any]]:
        """Process a streaming response asynchronously.

        Args:
            stream: Iterator of text chunks

        Returns:
            List of parsed JSON objects
        """
        all_objects = []

        async for chunk in stream:
            objects = self.stream_parser.feed(chunk)
            all_objects.extend(objects)

            # Yield control periodically
            if len(all_objects) % 10 == 0:
                await asyncio.sleep(0)

        # Finalize and get any remaining objects
        remaining = self.stream_parser.finalize()
        all_objects.extend(remaining)

        return all_objects

    def validate_response_schema(
        self, response: dict[str, Any], schema: dict[str, Any]
    ) -> bool:
        """Validate response against a schema.

        Args:
            response: Response to validate
            schema: Schema definition

        Returns:
            True if valid, False otherwise
        """
        try:
            # Simple schema validation (can be enhanced with jsonschema library)
            required = schema.get("required", [])
            properties = schema.get("properties", {})

            # Check required fields
            for field in required:
                if field not in response:
                    return False

            # Check field types
            for field, value in response.items():
                if field in properties:
                    expected_type = properties[field].get("type")
                    if expected_type and not self._check_type(value, expected_type):
                        return False

            return True

        except Exception:
            return False

    def _check_type(self, value: Any, expected_type: str) -> bool:
        """Check if value matches expected type."""
        type_map = {
            "string": str,
            "number": (int, float),
            "integer": int,
            "boolean": bool,
            "array": list,
            "object": dict,
        }

        expected_python_type = type_map.get(expected_type)
        if expected_python_type:
            return isinstance(value, expected_python_type)

        return True
