# Setup Scripts

This directory contains setup scripts for web-maestro development and deployment.

## setup-system-deps.py

Automatically installs system dependencies required by web-maestro:

- **Poppler** - Required for PDF processing functionality

### Supported Platforms

- **macOS**: Uses Homebrew (`brew install poppler`)
- **Ubuntu/Debian**: Uses apt-get (`sudo apt-get install poppler-utils`)  
- **CentOS/RHEL**: Uses yum (`sudo yum install poppler-utils`)
- **Fedora**: Uses dnf (`sudo dnf install poppler-utils`)
- **Arch Linux**: Uses pacman (`sudo pacman -S poppler`)
- **Windows**: Manual installation required

### Usage

```bash
# Direct execution
python scripts/setup-system-deps.py

# Via hatch
hatch run setup-system

# Full development setup
hatch run setup-dev
```

### Manual Installation

If the script fails or you prefer manual installation:

**macOS (Homebrew):**
```bash
brew install poppler
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install poppler-utils
```

**Windows:**
1. Download from: https://blog.alivate.com.au/poppler-windows/
2. Extract to a folder (e.g., `C:\poppler`)
3. Add `C:\poppler\bin` to your PATH environment variable
4. Restart your terminal/IDE

### Verification

The script automatically verifies installation by checking for:
- `pdftoppm` command (primary)
- `pdftocairo` command (fallback)

You can manually verify with:
```bash
pdftoppm -h
```