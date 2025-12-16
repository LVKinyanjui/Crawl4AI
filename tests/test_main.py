import os
import base64
import asyncio
from types import SimpleNamespace

import pytest

from save_utils import save_filtered
from async_save_utils import async_save_filtered


def make_dummy_result():
    # Build a simple object that mimics the CrawlResult attributes used by save utilities
    r = SimpleNamespace()
    r.markdown = "# Title\ncontent"
    r.html = "<html></html>"
    r.cleaned_html = None
    r.fit_html = None
    r.links = {"a": "b"}
    r.media = {"img": "1"}
    r.tables = [[1, 2], [3, 4]]
    r.extracted_content = "{}"
    r.pdf = b"PDFBYTES"
    r.mhtml = "MHTML"
    r.screenshot = base64.b64encode(b"PNGDATA").decode()
    r.metadata = {"k": "v"}
    r.response_headers = {"h": "v"}
    r.ssl_certificate = None
    r.status_code = 200
    return r


def test_save_filtered_sync(tmp_path):
    result = make_dummy_result()
    base_dir = str(tmp_path / "crawl_results")
    save_filtered(result, base_dir, "testpage", selected={"markdown", "screenshots"})

    # Markdown written
    assert os.path.exists(os.path.join(base_dir, "markdown", "testpage.md"))
    # Screenshot written
    assert os.path.exists(os.path.join(base_dir, "screenshots", "testpage.png"))
    # HTML should NOT be saved
    assert not os.path.exists(os.path.join(base_dir, "html"))


def test_save_filtered_async(tmp_path):
    result = make_dummy_result()
    base_dir = str(tmp_path / "crawl_results")

    asyncio.run(async_save_filtered(result, base_dir, "testpage", {"html", "links"}))

    assert os.path.exists(os.path.join(base_dir, "html", "raw", "testpage.html"))
    assert os.path.exists(os.path.join(base_dir, "links", "testpage.json"))
    # Markdown should NOT be saved
    assert not os.path.exists(os.path.join(base_dir, "markdown"))


def test_save_filtered_default_saves_all(tmp_path):
    result = make_dummy_result()
    base_dir = str(tmp_path / "crawl_results")
    # selected=None should save everything (same as save_all)
    save_filtered(result, base_dir, "testpage", selected=None)

    expected = [
        os.path.join(base_dir, "markdown", "testpage.md"),
        os.path.join(base_dir, "html", "raw", "testpage.html"),
        os.path.join(base_dir, "links", "testpage.json"),
        os.path.join(base_dir, "screenshots", "testpage.png"),
        os.path.join(base_dir, "metadata", "testpage.json"),
    ]

    for p in expected:
        assert os.path.exists(p), f"Expected {p} to exist"
