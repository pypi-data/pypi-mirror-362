from zona.markdown import md_to_html


def test_render():
    content = "# Hello World!"
    out = md_to_html(content)
    assert out.strip() == "<h1>Hello World!</h1>"
