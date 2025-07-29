# 🤝 Contributing to Web Maestro

Thank you for your interest in contributing to Web Maestro! This document provides guidelines and information about how to contribute effectively.

## 📋 Current Project Status

Web Maestro is in **early development** with the following status:

### ✅ **What's Implemented**
- Core browser automation using Playwright
- Multi-provider LLM support (OpenAI, Anthropic, Portkey, Ollama)
- Basic streaming functionality for LLM responses
- DOM content extraction and capture
- Type-safe configuration and data models
- Project structure and packaging setup

### 🚧 **What Needs Work**
- **Test Suite**: Currently no comprehensive tests exist
- **Documentation**: API docs need completion and examples
- **Error Handling**: More robust error recovery needed
- **Performance**: Optimization and monitoring needed
- **CI/CD**: No automated testing or deployment pipeline
- **Examples**: More real-world usage examples needed

### 📋 **Known Issues**
- Some DOM capture configurations cause errors due to missing parameters
- WebMaestro high-level class needs better integration
- Rate limiting and caching need full implementation
- Browser resource management could be improved

## 🎯 How You Can Help

### 🔴 **High Priority Contributions**

1. **Test Suite Development**
   - Unit tests for all provider classes
   - Integration tests for browser automation
   - End-to-end tests with real websites
   - Mock services for testing without API calls

2. **Documentation Improvements**
   - Complete API documentation with examples
   - Usage tutorials and guides
   - Architecture documentation
   - Performance benchmarking guides

3. **Bug Fixes**
   - Fix DOM capture configuration issues
   - Improve error handling and recovery
   - Browser session cleanup
   - Memory leak prevention

### 🟡 **Medium Priority Contributions**

4. **Feature Development**
   - Complete rate limiting implementation
   - Advanced caching strategies
   - Performance monitoring
   - Plugin architecture

5. **Developer Experience**
   - Better debugging tools
   - Development setup automation
   - Code quality improvements
   - Type safety enhancements

### 🟢 **Good First Issues**

6. **Documentation**
   - Fix typos and improve clarity
   - Add code examples
   - Update configuration examples
   - Create troubleshooting guides

7. **Small Features**
   - Additional utility functions
   - Better error messages
   - Configuration validation
   - Logging improvements

## 🚀 Getting Started

### Development Environment Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/fede-dash/web-maestro.git
   cd web-maestro
   ```

2. **Set Up Python Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install in development mode
   pip install -e ".[dev,all-providers]"
   ```

3. **Install Browser Dependencies**
   ```bash
   playwright install
   ```

4. **Verify Installation**
   ```bash
   # Test basic functionality
   python -c "from web_maestro import LLMConfig; print('✅ Import successful')"
   ```

### Testing Your Changes

Currently, we don't have automated tests, so manual testing is required:

1. **Test Provider Functionality**
   ```bash
   # Test with your own API keys
   python test_streaming.py
   python test_chelsea_final.py
   ```

2. **Test Browser Automation**
   ```bash
   # Test DOM capture
   python -c "
   import asyncio
   from web_maestro import fetch_rendered_html, SessionContext

   async def test():
       ctx = SessionContext()
       blocks = await fetch_rendered_html('https://example.com', ctx)
       print(f'Captured {len(blocks)} blocks' if blocks else 'Failed')

   asyncio.run(test())
   "
   ```

3. **Code Quality Checks**
   ```bash
   # Format code
   black .

   # Check linting
   ruff check .

   # Type checking (will show many errors currently)
   mypy src/ --ignore-missing-imports
   ```

## 📝 Contribution Guidelines

### Code Standards

1. **Python Style**
   - Follow PEP 8 guidelines
   - Use Black for code formatting
   - Add type hints to all functions
   - Use descriptive variable names

2. **Documentation**
   - Add docstrings to all public functions and classes
   - Include examples in docstrings where helpful
   - Update README.md if adding new features
   - Keep comments clear and concise

3. **Error Handling**
   - Use structured error handling with proper exception types
   - Log errors appropriately
   - Provide helpful error messages
   - Don't suppress exceptions without good reason

### Git Workflow

1. **Branch Naming**
   ```bash
   git checkout -b feature/add-tests
   git checkout -b fix/dom-capture-config
   git checkout -b docs/api-examples
   ```

2. **Commit Messages**
   ```bash
   # Good commit messages
   git commit -m "Add unit tests for PortkeyProvider class"
   git commit -m "Fix missing configuration parameters in DOM capture"
   git commit -m "Update README with accurate project status"

   # Bad commit messages
   git commit -m "fix stuff"
   git commit -m "updates"
   ```

3. **Pull Request Process**
   - Create small, focused PRs
   - Include description of changes
   - Reference any related issues
   - Test your changes manually
   - Update documentation if needed

### Specific Areas for Contribution

#### 🧪 **Testing (High Priority)**

Help us build a comprehensive test suite:

```bash
# Example test structure we need
tests/
├── unit/
│   ├── test_providers.py         # Test all LLM providers
│   ├── test_dom_capture.py       # Test browser automation
│   ├── test_utils.py             # Test utility functions
│   └── test_models.py            # Test data models
├── integration/
│   ├── test_full_extraction.py   # End-to-end tests
│   └── test_multi_provider.py    # Provider fallback tests
└── fixtures/
    ├── mock_responses.py         # Mock LLM responses
    └── test_websites.html        # Test HTML content
```

**What we need:**
- Mock services for LLM providers
- Browser automation tests
- Configuration validation tests
- Error handling tests

#### 📚 **Documentation (Medium Priority)**

Improve documentation with:

```bash
docs/
├── api/
│   ├── providers.md              # Provider documentation
│   ├── utilities.md              # Utility class docs
│   └── examples.md               # Code examples
├── guides/
│   ├── getting-started.md        # Beginner tutorial
│   ├── advanced-usage.md         # Advanced patterns
│   └── troubleshooting.md        # Common issues
└── development/
    ├── architecture.md           # System design
    ├── contributing.md           # This file
    └── testing.md                # Testing guidelines
```

#### 🐛 **Bug Fixes (High Priority)**

Known issues to fix:

1. **DOM Capture Configuration**
   ```python
   # This currently fails with KeyError
   blocks = await fetch_rendered_html(url, ctx)
   # Fix: Add default configuration handling
   ```

2. **Browser Session Cleanup**
   ```python
   # Memory leaks when browser sessions aren't properly closed
   # Fix: Implement proper context managers
   ```

3. **Error Recovery**
   ```python
   # Better handling of network failures and timeouts
   # Fix: Add retry logic and fallback strategies
   ```

## 🔍 Code Review Process

Since this is an early-stage project, code review will be informal:

1. **Self-Review Checklist**
   - [ ] Code follows style guidelines
   - [ ] Changes are well-documented
   - [ ] Manual testing completed
   - [ ] No obvious performance issues
   - [ ] Error handling is appropriate

2. **What Reviewers Look For**
   - Code clarity and maintainability
   - Proper error handling
   - Documentation completeness
   - Adherence to project patterns

## 🎯 Priority Areas

### Immediate Needs (Next 2-4 weeks)
1. Basic test suite for core functionality
2. Fix DOM capture configuration issues
3. Improve error messages and handling
4. Complete API documentation

### Short Term (1-3 months)
1. Comprehensive test coverage
2. CI/CD pipeline setup
3. Performance optimization
4. Plugin architecture foundation

### Long Term (3+ months)
1. Advanced features (WebSocket support, proxy rotation)
2. Enterprise features (monitoring, SSO)
3. Community ecosystem (plugins, integrations)

## 📞 Getting Help

### Communication Channels

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Pull Request Comments**: For code-specific discussions

### Asking for Help

When asking for help, please include:

1. **Context**: What are you trying to do?
2. **Problem**: What's not working?
3. **Environment**: Python version, OS, dependencies
4. **Code**: Minimal example that reproduces the issue
5. **Logs**: Error messages or relevant output

**Example:**
```markdown
## Issue: DOM capture fails with missing configuration

**Context**: Trying to extract content from a dynamic website

**Problem**: Getting KeyError for 'max_tabs' when calling fetch_rendered_html

**Environment**:
- Python 3.11
- macOS 13.0
- web-maestro installed from source

**Code**:
```python
ctx = SessionContext()
blocks = await fetch_rendered_html("https://example.com", ctx)
```

**Error**:
```
KeyError: 'max_tabs'
```
```

## 🏆 Recognition

Contributors will be recognized in:

- **README.md**: Contributors section
- **Release Notes**: Major contributions highlighted
- **GitHub**: Contributor graphs and statistics

## 📄 License

By contributing to Web Maestro, you agree that your contributions will be licensed under the MIT License.

---

## 🚀 Ready to Contribute?

1. **Start Small**: Pick a good first issue or documentation improvement
2. **Ask Questions**: Don't hesitate to ask for clarification
3. **Share Ideas**: Open discussions for new features or improvements
4. **Be Patient**: This is an early project, and we're learning together

Thank you for helping make Web Maestro better! 🌟

---

**Current Maintainers:**
- Primary maintainer: [Your Name]
- Active contributors: [List active contributors]

**Last Updated:** January 2025
