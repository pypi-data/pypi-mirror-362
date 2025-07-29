import xml.etree.ElementTree as etree
from collections.abc import Sequence
from logging import Logger
from pathlib import Path
from typing import Any, override

from l2m4m import LaTeX2MathMLExtension
from markdown import Markdown
from markdown.extensions.abbr import AbbrExtension
from markdown.extensions.attr_list import AttrListExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.def_list import DefListExtension
from markdown.extensions.footnotes import FootnoteExtension
from markdown.extensions.md_in_html import MarkdownInHtmlExtension
from markdown.extensions.sane_lists import SaneListExtension
from markdown.extensions.smarty import SmartyExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension
from markdown.treeprocessors import Treeprocessor
from pygments.formatters.html import HtmlFormatter
from pymdownx.betterem import BetterEmExtension
from pymdownx.caret import InsertSupExtension
from pymdownx.escapeall import EscapeAllExtension
from pymdownx.inlinehilite import InlineHiliteExtension
from pymdownx.smartsymbols import SmartSymbolsExtension
from pymdownx.superfences import SuperFencesCodeExtension
from pymdownx.tilde import DeleteSubExtension

from zona import util
from zona.config import ZonaConfig
from zona.layout import Layout
from zona.log import get_logger
from zona.metadata import Metadata
from zona.models import Item


class ZonaImageTreeprocessor(Treeprocessor):
    """Implement Zona's image caption rendering."""

    def __init__(self, md: Markdown):
        super().__init__()
        self.md: Markdown = md
        self.logger: Logger = get_logger()

    @override
    def run(self, root: etree.Element):
        for parent in root.iter():
            for idx, child in enumerate(list(parent)):
                if (
                    child.tag == "p"
                    and len(child) == 1
                    and child[0].tag == "img"
                ):
                    img = child[0]
                    div = etree.Element(
                        "div", {"class": "image-container"}
                    )
                    div.append(img)
                    title = img.attrib.get("alt", "")
                    if title:
                        raw_caption = self.md.convert(title)
                        caption_html = raw_caption.strip()
                        if caption_html.startswith(
                            "<p>"
                        ) and caption_html.endswith("</p>"):
                            caption_html = caption_html[3:-4]
                        caption = etree.Element("small")
                        caption.text = ""  # should be rendered
                        caption_html_element = etree.fromstring(
                            f"<span>{caption_html}</span>"
                        )
                        caption.append(caption_html_element)
                        div.append(caption)
                    parent[idx] = div


class ZonaLinkTreeprocessor(Treeprocessor):
    def __init__(
        self,
        config: ZonaConfig | None,
        resolve: bool = False,
        source: Path | None = None,
        layout: Layout | None = None,
        item_map: dict[Path, Item] | None = None,
    ):
        super().__init__()
        self.resolve: bool = resolve
        self.logger: Logger = get_logger()
        if self.resolve:
            assert source is not None
            assert layout is not None
            assert item_map is not None
            self.source: Path = source.resolve()
            self.layout: Layout = layout
            self.item_map: dict[Path, Item] = item_map
            self.config: ZonaConfig | None = config

    @override
    def run(self, root: etree.Element):
        for element in root.iter("a"):
            href = element.get("href")
            if not href:
                continue
            if self.resolve:
                assert self.config
                cur = Path(href)
                _href = href
                same_file = False
                resolved = Path()
                # href starting with anchor reference the current file
                if href.startswith("#"):
                    same_file = True
                elif href.startswith("/"):
                    # resolve relative to content root
                    resolved = (
                        self.layout.content / cur.relative_to("/")
                    ).resolve()
                else:
                    # treat as relative link and try to resolve
                    resolved = (self.source.parent / cur).resolve()
                # check if the link is internal
                internal = same_file
                if not same_file:
                    for suffix in {".md", ".html"}:
                        if resolved.with_suffix(suffix).exists():
                            internal = True
                            resolved = resolved.with_suffix(suffix)
                            break
                # only substitute if link points to an actual file
                # that isn't the self file
                if not same_file and internal:
                    item = self.item_map.get(resolved)
                    if item:
                        href = util.normalize_url(item.url)
                        # don't sub if it's already correct lol
                        if _href != href:
                            element.set("href", href)
                            self.logger.debug(
                                f"Link in file {self.source}: {_href} resolved to {href}"
                            )
                    else:
                        self.logger.debug(
                            f"Warning: resolved path {resolved} not found in item map"
                        )
                # open link in new tab if not self-link
                elif (
                    self.config.markdown.links.external_new_tab
                    and not same_file
                ):
                    element.set("target", "_blank")


def get_formatter(config: ZonaConfig):
    c = config.markdown.syntax_highlighting
    formatter = HtmlFormatter(
        style=c.theme, nowrap=not c.wrap, nobackground=True
    )
    return formatter


def md_to_html(
    content: str,
    config: ZonaConfig | None,
    resolve_links: bool = False,
    source: Path | None = None,
    layout: Layout | None = None,
    item_map: dict[Path, Item] | None = None,
    metadata: Metadata | None = None,
) -> str:
    extensions: Sequence[Any] = [
        BetterEmExtension(),
        SuperFencesCodeExtension(
            disable_indented_code_blocks=True,
            css_class="codehilite",
        ),
        FootnoteExtension(),
        AttrListExtension(),
        DefListExtension(),
        TocExtension(
            anchorlink=True,
        ),
        TableExtension(),
        AbbrExtension(),
        SmartyExtension(),
        InsertSupExtension(),
        DeleteSubExtension(),
        SmartSymbolsExtension(),
        SaneListExtension(),
        MarkdownInHtmlExtension(),
        EscapeAllExtension(hardbreak=True),
    ]
    kwargs: dict[str, Any] = {
        "extensions": extensions,
        "tab_length": 2,
    }
    if metadata and metadata.math:
        kwargs["extensions"].append(LaTeX2MathMLExtension())
    if config:
        kwargs["extensions"].extend(
            [
                CodeHiliteExtension(
                    linenums=False,
                    noclasses=False,
                    pygments_style=config.markdown.syntax_highlighting.theme,
                ),
                InlineHiliteExtension(css_class="codehilite"),
            ]
        )
        kwargs["tab_length"] = config.markdown.tab_length
    md = Markdown(**kwargs)
    if resolve_links:
        if source is None or layout is None or item_map is None:
            raise TypeError(
                "md_to_html() missing source and ctx when resolve_links is true"
            )
        md.treeprocessors.register(
            item=ZonaLinkTreeprocessor(
                config, resolve_links, source, layout, item_map
            ),
            name="zona_links",
            priority=15,
        )
    md.treeprocessors.register(
        item=ZonaImageTreeprocessor(md),
        name="zona_images",
        priority=17,
    )
    return md.convert(content)


def get_style_defs(config: ZonaConfig) -> str:
    formatter = get_formatter(config)
    defs = formatter.get_style_defs(".codehilite")
    assert isinstance(defs, str)
    return defs
