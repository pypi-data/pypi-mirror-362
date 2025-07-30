from pathlib import Path
from typing import Literal

from jinja2 import Environment, FileSystemLoader, select_autoescape

from zona import util
from zona.config import ZonaConfig
from zona.markdown import md_to_html
from zona.models import Item


def get_header(template_dir: Path) -> str | None:
    md_header = template_dir / "header.md"
    html_header = template_dir / "header.html"
    if md_header.exists():
        return md_to_html(md_header.read_text(), None)
    elif html_header.exists():
        return html_header.read_text()


def get_footer(template_dir: Path) -> str | None:
    md_footer = template_dir / "footer.md"
    html_footer = template_dir / "footer.html"
    if md_footer.exists():
        return md_to_html(md_footer.read_text(), None)
    elif html_footer.exists():
        return html_footer.read_text()


# TODO: add a recent posts element that can be included elsewhere?
class Templater:
    def __init__(
        self,
        config: ZonaConfig,
        template_dir: Path,
        post_list: list[Item],
    ):
        # build temporary template dir
        self.env: Environment = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )
        self.config: ZonaConfig = config
        self.template_dir: Path = template_dir
        self.footer: str | None = get_footer(template_dir)
        self.post_list: list[Item] = post_list

    def render_header(self):
        template = self.env.get_template("header.html")
        return template.render(site_map=self.config.sitemap)

    def render_item(self, item: Item, content: str) -> str:
        env = self.env
        meta = item.metadata
        assert meta is not None
        if meta.template is None:
            if item.post:
                template_name = "page.html"
            else:
                template_name = "basic.html"
        else:
            template_name = (
                meta.template
                if meta.template.endswith(".html")
                else meta.template + ".html"
            )
        template = env.get_template(template_name)
        header: str | Literal[False] = (
            self.render_header() if meta.header else False
        )
        footer: str | Literal[False] = (
            self.footer if self.footer and meta.footer else False
        )
        return template.render(
            content=content,
            url=item.url,
            metadata=meta,
            header=header,
            footer=footer,
            is_post=item.post,
            newer=util.normalize_url(item.newer.url)
            if item.newer
            else None,
            older=util.normalize_url(item.older.url)
            if item.older
            else None,
            post_list=self.post_list,
        )
