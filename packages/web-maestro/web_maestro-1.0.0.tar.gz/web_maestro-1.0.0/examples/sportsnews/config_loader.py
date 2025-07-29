"""Configuration loader for the baseball crawler."""

from dataclasses import dataclass
from datetime import datetime
import os

import yaml


@dataclass
class CrawlerConfig:
    """Main crawler configuration."""

    max_depth: int = 1
    max_pages: int = 3
    max_concurrent_crawls: int = 3
    content_size_range: dict[str, int] = None
    skip_patterns: list[str] = None

    def __post_init__(self):
        if self.content_size_range is None:
            self.content_size_range = {}
        if self.skip_patterns is None:
            self.skip_patterns = []


@dataclass
class ContentFilterConfig:
    """Content filtering configuration."""

    min_chars: int = 150
    max_chars: int = 3000
    skip_patterns: list[str] = None

    def __post_init__(self):
        if self.skip_patterns is None:
            self.skip_patterns = []


@dataclass
class LLMConfig:
    """LLM processing configuration."""

    chunk_size: int = 5
    max_blocks_to_analyze: int = 20
    content_preview_length: int = 4000
    extraction_prompt: str = ""
    summary_prompt: str = ""


@dataclass
class ScoutBridgeConfig:
    """Scout bridge configuration."""

    enabled: bool = True
    baseball_keywords: list[str] = None
    link_filter_prompt: str = ""

    def __post_init__(self):
        if self.baseball_keywords is None:
            self.baseball_keywords = []


@dataclass
class OutputConfig:
    """Output configuration."""

    json_filename_template: str = "smart_baseball_news_{timestamp}.json"
    txt_filename_template: str = "smart_baseball_news_{timestamp}.txt"
    timestamp_format: str = "%Y%m%d_%H%M%S"
    min_items_for_output: int = 1

    def get_timestamp(self) -> str:
        """Get formatted timestamp."""
        return datetime.now().strftime(self.timestamp_format)

    def get_json_filename(self) -> str:
        """Get JSON output filename with timestamp."""
        return self.json_filename_template.format(timestamp=self.get_timestamp())

    def get_txt_filename(self) -> str:
        """Get TXT output filename with timestamp."""
        return self.txt_filename_template.format(timestamp=self.get_timestamp())


@dataclass
class LoggingConfig:
    """Logging configuration."""

    level: str = "DEBUG"
    detailed_log_file: str = "baseball_crawler_detailed.log"
    error_log_file: str = "baseball_crawler_errors.log"
    modules: dict[str, str] = None

    def __post_init__(self):
        if self.modules is None:
            self.modules = {}


@dataclass
class TimeoutConfig:
    """Timeout configuration."""

    page_timeout: int = 30000
    dom_timeout: int = 8000
    initial_wait: int = 2000
    stability_threshold: int = 4


@dataclass
class BrowserConfig:
    """Browser configuration."""

    headless: bool = True
    viewport: dict[str, int] = None
    args: list[str] = None

    def __post_init__(self):
        if self.viewport is None:
            self.viewport = {"width": 1920, "height": 1080}
        if self.args is None:
            self.args = []


@dataclass
class BaseballCrawlerConfig:
    """Complete baseball crawler configuration."""

    crawler: CrawlerConfig
    content_filter: ContentFilterConfig
    llm: LLMConfig
    scout_bridge: ScoutBridgeConfig
    output: OutputConfig
    logging: LoggingConfig
    timeouts: TimeoutConfig
    browser: BrowserConfig


def load_config(config_path: str = None) -> BaseballCrawlerConfig:
    """Load configuration from YAML file.

    Args:
        config_path: Path to YAML config file. If None, looks for default locations.

    Returns:
        Loaded configuration object
    """
    if config_path is None:
        # Try default locations
        script_dir = os.path.dirname(os.path.abspath(__file__))
        default_paths = [
            os.path.join(script_dir, "baseball_crawler_config.yaml"),
            os.path.join(script_dir, "config.yaml"),
            "baseball_crawler_config.yaml",
            "config.yaml",
        ]

        for path in default_paths:
            if os.path.exists(path):
                config_path = path
                break
        else:
            raise FileNotFoundError(
                f"No config file found in default locations: {default_paths}"
            )

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path) as f:
        data = yaml.safe_load(f)

    # Parse nested configuration
    crawler_data = data.get("crawler", {})
    content_size_range = crawler_data.get("content_size_range", {})

    return BaseballCrawlerConfig(
        crawler=CrawlerConfig(**crawler_data),
        content_filter=ContentFilterConfig(
            min_chars=content_size_range.get("min_chars", 150),
            max_chars=content_size_range.get("max_chars", 3000),
            skip_patterns=crawler_data.get("skip_patterns", []),
        ),
        llm=LLMConfig(**data.get("llm", {})),
        scout_bridge=ScoutBridgeConfig(**data.get("scout_bridge", {})),
        output=OutputConfig(**data.get("output", {})),
        logging=LoggingConfig(**data.get("logging", {})),
        timeouts=TimeoutConfig(**data.get("timeouts", {})),
        browser=BrowserConfig(**data.get("browser", {})),
    )


def create_default_config() -> BaseballCrawlerConfig:
    """Create default configuration when no config file is available."""
    return BaseballCrawlerConfig(
        crawler=CrawlerConfig(),
        content_filter=ContentFilterConfig(
            skip_patterns=[
                "skip to",
                "navigation",
                "menu",
                "footer",
                "header",
                "subscribe",
                "sign up",
                "log in",
                "follow us",
                "privacy policy",
                "terms of use",
                "cookie",
            ]
        ),
        llm=LLMConfig(
            extraction_prompt="""Analyze this content and extract baseball-related information.

            Content: {content}

            Return JSON format: {{"baseball_news": ["item1", "item2", ...]}}""",
            summary_prompt="""Analyze baseball news and create a summary.

            Content: {content}

            Return JSON with summary, key_topics, major_players, major_teams, major_events.""",
        ),
        scout_bridge=ScoutBridgeConfig(
            baseball_keywords=["baseball", "mlb", "major league"],
            link_filter_prompt="Is this link related to baseball? Link: {link_text} URL: {link_url} Answer YES or NO.",
        ),
        output=OutputConfig(),
        logging=LoggingConfig(),
        timeouts=TimeoutConfig(),
        browser=BrowserConfig(),
    )
