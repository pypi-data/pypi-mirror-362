from dataclasses import dataclass
from datetime import date
from pathlib import Path

import frontmatter
from dacite.config import Config
from dacite.core import from_dict
from dacite.exceptions import DaciteError
from dateutil import parser as date_parser
from yaml import YAMLError

import zona.util


@dataclass
class Metadata:
    title: str
    date: date
    description: str | None
    show_title: bool = True
    show_date: bool = True
    show_nav: bool = True
    style: str | None = "/static/style.css"
    header: bool = True
    footer: bool = True
    template: str | None = None
    post: bool | None = None
    draft: bool = False
    ignore: bool = False
    math: bool = True


def parse_date(raw_date: str | date | object) -> date:
    if isinstance(raw_date, date):
        return raw_date
    assert isinstance(raw_date, str)
    return date_parser.parse(raw_date).date()


def parse_metadata(path: Path) -> tuple[Metadata, str]:
    """
    Parses a file and returns parsed Metadata and its content. Defaults
    are applied for missing fields. If there is no metadata, a Metadata
    with default values is returned.

    Raises:
        ValueError: If the metadata block is malformed in any way.
    """
    try:
        post = frontmatter.load(str(path))
    except YAMLError as e:
        raise ValueError(f"YAML frontmatter error in {path}: {e}")
    raw_meta = post.metadata or {}
    defaults = {
        "title": zona.util.filename_to_title(path),
        "date": date.fromtimestamp(path.stat().st_ctime),
    }
    meta = {**defaults, **raw_meta}
    meta["date"] = parse_date(meta.get("date"))
    try:
        metadata = from_dict(
            data_class=Metadata,
            data=meta,
            config=Config(check_types=True, strict=True),
        )
    except DaciteError as e:
        raise ValueError(f"Malformed metadata in {path}: {e}")
    return metadata, post.content
