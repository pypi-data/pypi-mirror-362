"""Portkey configuration for ESPN baseball crawler."""

PORTKEY_CONFIG = {
    "provider": "portkey",
    "model": "gpt-4o",
    "api_key": "9tE30As65QsH7TTIuaQzfpFyFMg8",
    "base_url": "http://cybertron-service-gateway.service.prod.ddsd:8080/v1",
    # Generous token limits for detailed content extraction
    "max_tokens": 4000,  # Much higher limit for longer responses
    "temperature": 0.3,  # Lower temperature for more focused extraction
    "extra_params": {"virtual_key": "openai-merchant-53367b"},
}
