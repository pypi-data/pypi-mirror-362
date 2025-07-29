from dataclasses import dataclass, field
from pathlib import Path

import yaml
from dacite import from_dict

from zona.log import get_logger

logger = get_logger()


def find_config(start: Path | None = None) -> Path | None:
    logger.debug("Searching for config file...")
    current = (start or Path.cwd()).resolve()

    for parent in [current, *current.parents]:
        candidate = parent / "config.yml"
        if candidate.is_file():
            logger.debug(f"Config file {candidate} found.")
            return candidate
    logger.debug("Couldn't find config file.")
    return None


SitemapConfig = dict[str, str]


@dataclass
class BlogConfig:
    dir: str = "blog"


@dataclass
class HighlightingConfig:
    enabled: bool = True
    theme: str = "ashen"
    wrap: bool = False


@dataclass
class LinksConfig:
    external_new_tab: bool = True


@dataclass
class MarkdownConfig:
    image_labels: bool = True
    tab_length: int = 2
    syntax_highlighting: HighlightingConfig = field(
        default_factory=HighlightingConfig
    )
    links: LinksConfig = field(default_factory=LinksConfig)


@dataclass
class BuildConfig:
    clean_output_dir: bool = True
    include_drafts: bool = False


@dataclass
class ReloadConfig:
    enabled: bool = True
    scroll_tolerance: int = 100


@dataclass
class ServerConfig:
    reload: ReloadConfig = field(default_factory=ReloadConfig)


IGNORELIST = [".marksman.toml"]


@dataclass
class ZonaConfig:
    base_url: str = "/"
    # dictionary where key is name, value is url
    sitemap: SitemapConfig = field(
        default_factory=lambda: {"Home": "/"}
    )
    # list of globs relative to content that should be ignored
    ignore: list[str] = field(default_factory=lambda: IGNORELIST)
    markdown: MarkdownConfig = field(default_factory=MarkdownConfig)
    build: BuildConfig = field(default_factory=BuildConfig)
    blog: BlogConfig = field(default_factory=BlogConfig)
    server: ServerConfig = field(default_factory=ServerConfig)

    @classmethod
    def from_file(cls, path: Path) -> "ZonaConfig":
        with open(path, "r") as f:
            raw = yaml.safe_load(f)
        return from_dict(data_class=cls, data=raw)
