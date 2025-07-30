import shutil
from datetime import date
from pathlib import Path

from zona import markdown as zmd
from zona import util
from zona.config import ZonaConfig
from zona.layout import Layout, discover_layout
from zona.log import get_logger
from zona.metadata import parse_metadata
from zona.models import Item, ItemType
from zona.templates import Templater

logger = get_logger()


class ZonaBuilder:
    def __init__(
        self,
        cli_root: Path | None = None,
        cli_output: Path | None = None,
        draft: bool = False,
    ):
        logger.debug("Initializing ZonaBuilder.")
        self.layout: Layout = discover_layout(cli_root, cli_output)
        self.config: ZonaConfig = ZonaConfig.from_file(
            self.layout.root / "config.yml"
        )
        if draft:
            self.config.build.include_drafts = True
        self.items: list[Item] = []
        self.item_map: dict[Path, Item] = {}
        self.fresh: bool = True

    def _discover(self):
        layout = self.layout
        items: list[Item] = []

        base = layout.root / layout.content
        logger.debug(f"Discovering content in {base}.")
        for path in base.rglob("*"):
            if path.is_file() and not util.should_ignore(
                path, patterns=self.config.ignore, base=base
            ):
                # we only parse markdown files not in static/
                destination = layout.output / path.relative_to(base)
                item = Item(
                    source=path,
                    destination=destination,
                    url=str(destination.relative_to(layout.output)),
                )
                if path.name.endswith(
                    ".md"
                ) and not path.is_relative_to(
                    layout.root / "content" / "static"
                ):
                    logger.debug(f"Parsing {path.name}.")
                    item.metadata, item.content = parse_metadata(path)
                    if item.metadata.ignore or (
                        item.metadata.draft
                        and not self.config.build.include_drafts
                    ):
                        continue
                    if item.metadata.post:
                        item.post = True
                    elif item.metadata.post is None:
                        # check if in posts dir?
                        blog_dir = base / Path(self.config.blog.dir)
                        if item.source.is_relative_to(blog_dir):
                            item.post = True
                    item.type = ItemType.MARKDOWN
                    item.copy = False
                    name = destination.stem
                    if name == "index":
                        item.destination = (
                            item.destination.with_suffix(".html")
                        )
                    else:
                        relative = path.relative_to(base).with_suffix(
                            ""
                        )
                        name = relative.stem
                        item.destination = (
                            layout.output
                            / relative.parent
                            / name
                            / "index.html"
                        )
                    rel_url = item.destination.parent.relative_to(
                        layout.output
                    )
                    item.url = (
                        ""
                        if rel_url == Path(".")
                        else rel_url.as_posix()
                    )
                items.append(item)
        self.items = items

    def _build(self):
        assert self.items
        # sort according to date
        # descending order
        post_list: list[Item] = sorted(
            [item for item in self.items if item.post],
            key=lambda item: item.metadata.date
            if item.metadata
            else date.min,
            reverse=True,
        )
        # number of posts
        posts = len(post_list)
        # link post chronology
        for i, item in enumerate(post_list):
            # prev: older post
            older = post_list[i + 1] if i + 1 < posts else None
            # next: newer post
            newer = post_list[i - 1] if i > 0 else None
            item.older = older
            item.newer = newer

        templater = Templater(
            config=self.config,
            template_dir=self.layout.templates,
            post_list=post_list,
        )
        self.item_map = {
            item.source.resolve(): item for item in self.items
        }

        # write code highlighting stylesheet
        if self.config.markdown.syntax_highlighting.enabled:
            pygments_style = zmd.get_style_defs(self.config)
            pygments_path = (
                self.layout.output / "static" / "pygments.css"
            )
            util.ensure_parents(pygments_path)
            pygments_path.write_text(pygments_style)
        for item in self.item_map.values():
            dst = item.destination
            # print(item)
            # create parent dirs if needed
            if item.type == ItemType.MARKDOWN:
                assert item.content is not None
                # parse markdown and render as html
                raw_html = zmd.md_to_html(
                    config=self.config,
                    content=item.content,
                    resolve_links=True,
                    source=item.source,
                    layout=self.layout,
                    item_map=self.item_map,
                    metadata=item.metadata,
                )
                # TODO: test this
                rendered = templater.render_item(item, raw_html)
                util.ensure_parents(dst)
                dst.write_text(rendered, encoding="utf-8")
            else:
                if item.copy:
                    util.copy_static_file(item.source, dst)

    def build(self):
        # clean output if applicable
        if (
            self.config.build.clean_output_dir
            and self.layout.output.is_dir()
        ):
            logger.debug("Removing stale output...")
            # only remove output dir's children
            # to avoid breaking live preview
            for child in self.layout.output.iterdir():
                if child.is_file() or child.is_symlink():
                    child.unlink()
                elif child.is_dir():
                    shutil.rmtree(child)
        if not self.fresh:
            self.layout = self.layout.refresh()
        logger.debug("Discovering...")
        self._discover()
        logger.debug("Building...")
        self._build()
        self.fresh = False
