from datetime import date
from pathlib import Path

import pytest

from zona.builder import build, discover, split_metadata
from zona.metadata import Metadata


def test_split_metadata(tmp_path: Path):
    content = """---
title: Test Post
date: 2025-06-03
description: This is a test.
---

# Hello World
    """
    test_file = tmp_path / "test.md"
    test_file.write_text(content)
    meta, content = split_metadata(test_file)

    assert isinstance(meta, Metadata)
    assert meta.title == "Test Post"
    assert meta.description == "This is a test."
    assert meta.date == date(2025, 6, 3)
    assert content == "# Hello World"


def test_no_metadata(tmp_path: Path):
    content = "# Hello World"
    test_file = tmp_path / "hello-world.md"
    test_file.write_text(content)
    meta, content = split_metadata(test_file)

    assert isinstance(meta, Metadata)
    assert meta.title == "Hello World"
    assert meta.description is None
    assert meta.date == date.today()
    assert content == "# Hello World"


def test_malformed_metadata(tmp_path: Path):
    with pytest.raises(ValueError):
        tests = {
            """
---
title: Test Post
date: not a date!!!
description: This is a test.
---
        """,
            """
---
title: Test Post
foobar:
    something: what???
description: This is a test.
---
        """,
            """
---
title Test Post
description: This is a test.
---
        """,
        }
        for i, content in enumerate(tests):
            test_file = tmp_path / str(i)
            test_file.write_text(content)
            split_metadata(test_file)


def test_discover(tmp_path: Path):
    contentd = tmp_path / "content"
    staticd = contentd / "static"
    templatesd = tmp_path / "templates"
    outd = tmp_path / "out"

    for d in [contentd, staticd, templatesd, outd]:
        d.mkdir()
    md_file = contentd / "post.md"
    md_file.write_text("""---
title: Test Post
date: 2025-06-03
description: This is a test.
---

# Hello World
    """)

    style = staticd / "style.css"
    style_content = """
p {
  color: red;
  text-align: center;
}
"""
    style.write_text(style_content)

    items = discover(tmp_path, outd)

    assert len(items) == 2

    md_item = items[0]
    assert md_item.source == md_file
    assert md_item.destination.name == "index.html"
    assert md_item.destination.is_relative_to(outd)
    assert md_item.url == "post.md"
    assert isinstance(md_item.metadata, Metadata)
    assert md_item.metadata.title == "Test Post"
    assert md_item.content is not None
    assert md_item.content.strip() == "# Hello World"

    st_item = items[1]
    assert st_item.source == style
    assert st_item.destination.name == "style.css"
    assert st_item.destination.is_relative_to(outd)
    assert st_item.url == "static/style.css"
    assert st_item.metadata is None


def test_build(tmp_path: Path):
    contentd = tmp_path / "content"
    staticd = contentd / "static"
    templatesd = tmp_path / "templates"
    outd = tmp_path / "out"

    for d in [contentd, staticd, templatesd, outd]:
        d.mkdir()
    md_file = contentd / "post.md"
    md_content = """---
title: Test Post
date: 2025-06-03
description: This is a test.
---

# Hello World
    """
    md_file.write_text(md_content)

    style = staticd / "style.css"
    style_content = """
p {
  color: red;
  text-align: center;
}
"""
    style.write_text(style_content)

    items = discover(tmp_path, outd)
    build(tmp_path, items)
    html = (outd / "post" / "index.html").read_text()
    assert html.strip() == "<h1>Hello World</h1>"
    s = (outd / "static" / "style.css").read_text()
    assert s.strip() == style_content.strip()
