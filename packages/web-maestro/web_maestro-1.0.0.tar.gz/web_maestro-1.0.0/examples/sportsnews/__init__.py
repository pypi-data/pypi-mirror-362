"""ESPN Sports News Extractor Module

Extract sports news from ESPN.com using web-maestro's browser automation and AI analysis.
"""

from .enhanced_espn_extractor import main as extract_espn_news

__version__ = "1.0.0"
__all__ = ["extract_espn_news"]
