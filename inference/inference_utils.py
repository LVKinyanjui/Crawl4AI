"""Inference helpers for screenshots in `crawl_results/screenshots`.

This module finds screenshots whose filenames match a regex pattern (configurable
via the `FILE_NAME_PATTERN` constant), runs OCR on them (if `pytesseract` is
available), and sends the extracted text to Google Gemini (via `google-genai`) for
analysis.

Usage:
    python -m inference.screenshots_inference --pattern "www_kessbet_com"

Dependencies:
    pip install pillow pytesseract google-genai
"""

from __future__ import annotations

import json
import os
import re
from typing import List, Optional

SCREENSHOT_DIR = os.path.join("crawl_results", "screenshots")
# Matches filenames containing the domain name; can be overridden by CLI
FILE_NAME_PATTERN = r"www_kessbet_com"


def list_matching_images(pattern: str = FILE_NAME_PATTERN, base_dir: str = SCREENSHOT_DIR) -> List[str]:
    """Return absolute paths of screenshots whose filenames match `pattern` (regex)."""
    if not os.path.isdir(base_dir):
        return []
    regex = re.compile(pattern)
    matches = []
    for fn in os.listdir(base_dir):
        if regex.search(fn):
            matches.append(os.path.join(base_dir, fn))
    return sorted(matches)


def extract_text_from_image(path: str) -> str:
    """Run OCR on `path` and return extracted text.

    If OCR dependencies are missing, returns an empty string.
    """
    try:
        from PIL import Image
        import pytesseract
    except Exception:
        # OCR not available
        return ""

    try:
        img = Image.open(path)
        text = pytesseract.image_to_string(img)
        return (text or "").strip()
    except Exception:
        return ""


def analyze_text_with_gemini(text: str, model: Optional[str] = None) -> str:
    """Send `text` to Google Gemini (google-genai) and return the generated analysis.

    Raises ValueError if GOOGLE_API_KEY is not set so that callers/tests can detect missing creds.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")

    # Import locally so the module can still be imported when deps aren't installed
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    model = model or os.environ.get("GENAI_MODEL", "gemini-3-pro-preview")

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=(
                    "Please analyze the following extracted text from a screenshot. "
                    "Extract any odds, statistics, tables, or notable information and summarize them in JSON.\n\n" + text
                )),
            ],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="HIGH"),
        response_mime_type="application/json",
    )

    result_chunks = []
    for chunk in client.models.generate_content_stream(
        model=model, contents=contents, config=generate_content_config
    ):
        # `chunk.text` contains incremental text
        result_chunks.append(chunk.text)

    return "".join(result_chunks)


def analyze_matching_screenshots(pattern: str = FILE_NAME_PATTERN, save: bool = True) -> List[dict]:
    """Find screenshots that match pattern, OCR them and run analysis.

    Returns a list of dicts with keys: path, ocr_text, analysis (the model output).
    If `save` is True, results are written to `crawl_results/analysis/<filename>.json`.
    """
    matches = list_matching_images(pattern)
    out = []
    save_dir = os.path.join("crawl_results", "analysis")
    if save and not os.path.isdir(save_dir):
        os.makedirs(save_dir, exist_ok=True)

    for path in matches:
        ocr_text = extract_text_from_image(path)
        try:
            analysis = analyze_text_with_gemini(ocr_text)
        except ValueError as e:
            # Propagate missing API key as a clear error
            raise

        record = {"path": path, "ocr_text": ocr_text, "analysis": analysis}
        out.append(record)

        if save:
            fn = os.path.basename(path)
            out_path = os.path.join(save_dir, f"{fn}.json")
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(record, f, indent=2, ensure_ascii=False)

    return out

