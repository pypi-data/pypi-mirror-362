# 🔄 Web Maestro Migration Guide

This guide helps you migrate existing maestro code to use the new enhanced web_maestro utilities while maintaining backward compatibility.

## 🎯 Overview

The enhanced web_maestro provides:
- **Multi-provider LLM support** (OpenAI, Anthropic, Portkey, Ollama)
- **Enhanced utilities** with caching, rate limiting, and better error handling
- **Backward compatibility** - existing code continues to work unchanged
- **Optional upgrades** - enable enhanced features as needed

## 🚀 Quick Start

### Option 1: Keep Existing Code (Zero Changes)
Your existing code continues to work without any changes:

```python
# This still works exactly as before
from maestro.src.web_maestro import fetch_rendered_html, CapturedBlock
from maestro.src.utils.url_utils import normalize_url

blocks = await fetch_rendered_html(url)
normalized = normalize_url(url)
```

### Option 2: Enable Enhanced Utilities (Optional)
Get better performance and features by enabling enhanced utilities:

```python
from maestro.src.web_maestro import enable_enhanced_utilities

# Enable enhanced utilities once in your application
if enable_enhanced_utilities():
    print("Enhanced utilities enabled!")
else:
    print("Using legacy utilities")
```

### Option 3: Use Enhanced API Directly
Access new functionality directly:

```python
from maestro.src.web_maestro import (
    try_static_first,           # Enhanced static-first fetching
    normalize_url_enhanced,     # Cached URL normalization
    chunk_text_enhanced,        # Smart text chunking
    WebMaestro                  # Multi-provider LLM support
)

# Enhanced fetching with static-first strategy
blocks = await try_static_first(url)

# Multi-provider LLM support
maestro = WebMaestro(provider="openai", api_key="sk-...")
result = await maestro.extract_content(url)
```

## 🔧 Migration Strategies

### 1. Gradual Migration (Recommended)

Start by enabling enhanced utilities in your main application:

```python
# In your main application startup
from maestro.src.web_maestro import auto_enable_enhanced

# Automatically enable if available
enhanced_enabled = auto_enable_enhanced()
print(f"Enhanced utilities: {'enabled' if enhanced_enabled else 'legacy'}")
```

This gives you enhanced performance without changing any existing code.

### 2. Utility-by-Utility Migration

Replace specific utility calls as needed:

#### URL Processing
```python
# Before
from maestro.src.utils.url_utils import normalize_url
normalized = normalize_url(url)

# After (with fallback)
from maestro.src.web_maestro import normalize_url_enhanced
normalized = normalize_url_enhanced(url)  # Uses enhanced if available, falls back otherwise
```

#### Text Processing
```python
# Before
from maestro.src.utils.text_processing import chunk_by_tokens_with_overlap
chunks = chunk_by_tokens_with_overlap(text, max_tokens, overlap)

# After (enhanced with metadata)
from maestro.src.web_maestro import chunk_text_enhanced
chunks = chunk_text_enhanced(text, max_tokens, overlap)
# Returns: [{"text": "...", "token_count": 150, "chunk_index": 0, ...}]
```

#### Content Fetching
```python
# Before
from maestro.src.utils.fetch import try_static_request_first
content = await try_static_request_first(url)

# After (enhanced with content blocks)
from maestro.src.web_maestro import try_static_first
blocks = await try_static_first(url)
# Returns: [ContentBlock(content="...", content_type="text", token_count=150)]
```

### 3. Full Migration to New API

For new code, use the enhanced API directly:

```python
from maestro.src.web_maestro import WebMaestro, LLMConfig
from maestro.src.web_maestro.utils import (
    EnhancedFetcher,
    JSONProcessor,
    TextProcessor,
    URLProcessor,
    RateLimiter
)

# Create processors
fetcher = EnhancedFetcher()
text_processor = TextProcessor()
url_processor = URLProcessor()

# Multi-provider LLM
config = LLMConfig(
    provider="openai",
    api_key="sk-...",
    model="gpt-4",
    temperature=0.1
)
maestro = WebMaestro(config)

# Enhanced workflow
async def process_url(url):
    # Validate and normalize
    if not url_processor.validate_cached(url):
        return None

    normalized_url = url_processor.normalize_cached(url)

    # Fetch with static-first strategy
    blocks = await fetcher.try_static_first(normalized_url)

    # Process with LLM
    for block in blocks:
        if block.content_type == "text":
            chunks = text_processor.chunk_text_cached(
                block.content,
                max_tokens=1000
            )

            for chunk in chunks:
                result = await maestro.extract_content(
                    chunk["text"],
                    schema={"type": "menu_item"}
                )
                yield result
```

## 🎛️ Configuration Options

### Enhanced Utilities Configuration

```python
from maestro.src.web_maestro import enable_enhanced_utilities
from maestro.src.web_maestro.utils import EnhancedFetcher

# Enable with custom configuration
if enable_enhanced_utilities():
    # Configure enhanced fetcher
    fetcher = EnhancedFetcher(
        timeout=30.0,
        max_retries=3,
        cache_enabled=True
    )
```

### Multi-Provider Configuration

```python
from maestro.src.web_maestro import WebMaestro, LLMConfig

# OpenAI
openai_config = LLMConfig(
    provider="openai",
    api_key="sk-...",
    model="gpt-4"
)

# Anthropic
anthropic_config = LLMConfig(
    provider="anthropic",
    api_key="sk-ant-...",
    model="claude-3-sonnet-20240229"
)

# Portkey (legacy compatibility)
portkey_maestro = WebMaestro.from_portkey_config("path/to/config.json")

# Ollama (local)
ollama_config = LLMConfig(
    provider="ollama",
    base_url="http://localhost:11434",
    model="llama2"
)
```

## 🔍 Compatibility Matrix

| Feature | Legacy API | Enhanced API | Auto-Fallback |
|---------|------------|--------------|---------------|
| URL Normalization | ✅ | ✅ (cached) | ✅ |
| Text Chunking | ✅ | ✅ (metadata) | ✅ |
| Content Fetching | ✅ | ✅ (blocks) | ✅ |
| JSON Processing | ❌ | ✅ | ✅ |
| Rate Limiting | ❌ | ✅ | ❌ |
| Multi-Provider LLM | ❌ | ✅ | ❌ |
| Caching | ❌ | ✅ | ❌ |

## 🧪 Testing Your Migration

### Test Enhanced Utilities
```python
from maestro.src.web_maestro import is_enhanced_enabled

# Check if enhanced utilities are working
if is_enhanced_enabled():
    print("✅ Enhanced utilities are active")
else:
    print("⚠️ Using legacy utilities")
```

### Test Multi-Provider Support
```python
from maestro.src.web_maestro import WebMaestro

try:
    maestro = WebMaestro(provider="openai", api_key="sk-test")
    print("✅ Multi-provider support working")
except Exception as e:
    print(f"❌ Multi-provider error: {e}")
```

### Performance Comparison
```python
import time
from maestro.src.web_maestro import (
    normalize_url_enhanced,
    chunk_text_enhanced
)
from maestro.src.utils.url_utils import normalize_url

# Test URL normalization performance
urls = ["https://example.com"] * 100

# Legacy
start = time.time()
for url in urls:
    normalize_url(url)
legacy_time = time.time() - start

# Enhanced (with caching)
start = time.time()
for url in urls:
    normalize_url_enhanced(url)
enhanced_time = time.time() - start

print(f"Legacy: {legacy_time:.3f}s, Enhanced: {enhanced_time:.3f}s")
print(f"Speedup: {legacy_time/enhanced_time:.1f}x")
```

## 🚨 Breaking Changes (None!)

The enhanced web_maestro is designed for **zero breaking changes**:

- ✅ All existing imports continue to work
- ✅ All existing function signatures unchanged
- ✅ All existing return types preserved
- ✅ Enhanced features are strictly additive

## 🛠️ Troubleshooting

### Enhanced Utilities Not Available
```python
from maestro.src.web_maestro import enable_enhanced_utilities

if not enable_enhanced_utilities():
    print("Enhanced utilities failed to load - using legacy")
    # This is expected and safe - your code will still work
```

### Import Errors
```python
# Safe import pattern
try:
    from maestro.src.web_maestro import try_static_first
    enhanced_available = True
except ImportError:
    from maestro.src.utils.fetch import try_static_request_first as try_static_first
    enhanced_available = False
```

### Performance Issues
```python
from maestro.src.web_maestro import disable_enhanced_utilities

# If enhanced utilities cause issues, disable them
disable_enhanced_utilities()
print("Switched back to legacy utilities")
```

## 📈 Migration Roadmap

### Phase 1: Enable Enhanced Utilities (Week 1)
- Add `auto_enable_enhanced()` to application startup
- Monitor performance improvements
- No code changes required

### Phase 2: Gradual API Migration (Weeks 2-4)
- Replace utility calls with enhanced versions
- Use enhanced error handling and caching
- Maintain full backward compatibility

### Phase 3: Multi-Provider Integration (Weeks 4-8)
- Integrate multi-provider LLM support
- Replace Portkey-specific code with provider abstraction
- Add new provider options (OpenAI, Anthropic, Ollama)

### Phase 4: Package Extraction (Future)
- Extract web_maestro as standalone package
- Publish to PyPI for pip installation
- Maintain maestro integration via dependency

## 🎯 Next Steps

1. **Start Simple**: Add `auto_enable_enhanced()` to your startup code
2. **Test Performance**: Measure improvement in your workflows
3. **Gradual Migration**: Replace utilities one at a time
4. **Multi-Provider**: Experiment with different LLM providers
5. **Feedback**: Report issues or performance improvements

---

*Migration support: The enhanced web_maestro maintains 100% backward compatibility while providing opt-in performance and feature improvements.*
