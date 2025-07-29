"""ESPN Sports News Extractor - Main Module

This allows running the extractor with: python -m examples.sportsnews
"""

import asyncio
from pathlib import Path
import sys

# Add the examples directory to the path so we can import modules
sys.path.insert(0, str(Path(__file__).parent))

from baseball_espn_extractor import main as run_baseball_extractor
from enhanced_espn_extractor import main as run_enhanced_extractor


def main():
    """Main entry point for the module."""
    print("🚀 ESPN Sports News Extractor - Module Mode")
    print("=" * 60)

    # Check if user wants baseball-specific extraction
    if len(sys.argv) > 1 and sys.argv[1].lower() in ["baseball", "mlb", "b"]:
        print("⚾ Running Baseball-Focused Extraction")
        extractor = run_baseball_extractor
    else:
        print("🏈 Running General Sports Extraction")
        print(
            "💡 Tip: Use 'python -m examples.sportsnews baseball' for baseball-focused extraction"
        )
        extractor = run_enhanced_extractor

    try:
        asyncio.run(extractor())
    except KeyboardInterrupt:
        print("\n⏹️  Extraction cancelled by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
