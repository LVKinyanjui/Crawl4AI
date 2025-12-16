import os
import tempfile
from inference import inference_utils as si


def test_list_matching_images(tmp_path):
    d = tmp_path / "screenshots"
    d.mkdir()
    (d / "www_example_com.png").write_text("x")
    (d / "other.png").write_text("x")

    matches = si.list_matching_images(pattern=r"www_example_com", base_dir=str(d))
    assert len(matches) == 1
    assert matches[0].endswith("www_example_com.png")


def test_analyze_text_with_gemini_requires_api_key():
    # Ensure no GOOGLE_API_KEY is set
    env = dict(os.environ)
    if "GOOGLE_API_KEY" in env:
        del os.environ["GOOGLE_API_KEY"]

    try:
        try:
            si.analyze_text_with_gemini("some text")
            assert False, "Expected ValueError when GOOGLE_API_KEY is missing"
        except ValueError:
            pass
    finally:
        os.environ.clear()
        os.environ.update(env)


def test_no_screenshots_returns_empty(tmp_path):
    d = tmp_path / "empty"
    d.mkdir()
    matches = si.list_matching_images(pattern=r"nothing_here", base_dir=str(d))
    assert matches == []
