from __future__ import annotations

from collections.abc import Mapping
from typing import Optional
from unittest import mock

import pytest

from pdoc.render_helpers import (edit_url, qualname_candidates, relative_link, render_docstring, split_identifier)


@pytest.mark.parametrize(
    "current,target,relative",
    [
        ("foo", "foo", ""),
        ("foo", "bar", "bar.html"),
        ("foo.foo", "foo", "../foo.html"),
        ("foo.foo", "bar", "../bar.html"),
        ("foo.bar", "foo.bar.baz", "bar/baz.html"),
        ("foo.bar.baz", "foo.qux.quux", "../qux/quux.html"),
    ],
)
def test_relative_link(current, target, relative):
    assert relative_link(current, target) == relative


@pytest.mark.parametrize("context,candidates", [
    ("", ["qux"]),
    ("foo", ["foo.qux", "qux"]),
    ("foo.bar", ["foo.bar.qux", "foo.qux", "qux"])
])
def test_qualname_candidates(context, candidates):
    assert qualname_candidates("qux", context) == candidates


@pytest.mark.parametrize(
    "modulename,is_package,mapping,result",
    [
        ["demo", False, {"dem": "abc"}, None],
        [
            "demo",
            False,
            {"demo": "https://github.com/mhils/pdoc/blob/master/test/testdata/demo"},
            "https://github.com/mhils/pdoc/blob/master/test/testdata/demo.py",
        ],
        [
            "demo",
            True,
            {"demo": "https://github.com/mhils/pdoc/blob/master/test/testdata/demo/"},
            "https://github.com/mhils/pdoc/blob/master/test/testdata/demo/__init__.py",
        ],
    ],
)
def test_edit_url(
    modulename: str, is_package: bool, mapping: Mapping[str, str], result: Optional[str]
):
    assert edit_url(modulename, is_package, mapping) == result


@pytest.mark.parametrize(
    "all_modules,fullname,result",
    [
        [["a", "a.b", "c"], "a.b.c.d", ("a.b", "c.d")],
        [["a", "a.b", "c"], "a.c.b.d", ("a", "c.b.d")],
    ],
)
def test_split_identifier(all_modules, fullname, result):
    assert split_identifier(all_modules, fullname) == result


def test_markdown_toc():
    """
    markdown2 has this weird property that it return a str-like object with a hidden `toc_html` attr.

    It's easy to introduce a `.strip()` in there and this gets washed away, so let's test that it works properly.
    """
    assert render_docstring(mock.MagicMock(), "#foo\n#bar").toc_html  # type: ignore
