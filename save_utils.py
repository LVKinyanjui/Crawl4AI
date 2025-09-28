"""
Utility functions to save CrawlResult fields to the organized directory structure.
"""
import os
import json
from typing import Any

def debug_print(attr_name, value):
    print(f"[DEBUG] {attr_name}: type={type(value)}, value={repr(value)[:200]}")

def save_markdown(result, base_dir, url_id):
    """Save markdown fields from CrawlResult."""
    md_dir = os.path.join(base_dir, "markdown")
    if result.markdown:
        debug_print("markdown", result.markdown)
        if hasattr(result.markdown, "raw_markdown"):
            if isinstance(result.markdown.raw_markdown, str):
                with open(os.path.join(md_dir, f"{url_id}_raw.md"), "w", encoding="utf-8") as f:
                    f.write(result.markdown.raw_markdown)
            debug_print("raw_markdown", result.markdown.raw_markdown)
            if isinstance(result.markdown.markdown_with_citations, str):
                with open(os.path.join(md_dir, f"{url_id}_citations.md"), "w", encoding="utf-8") as f:
                    f.write(result.markdown.markdown_with_citations)
            debug_print("markdown_with_citations", result.markdown.markdown_with_citations)
            if isinstance(result.markdown.references_markdown, str):
                with open(os.path.join(md_dir, f"{url_id}_references.md"), "w", encoding="utf-8") as f:
                    f.write(result.markdown.references_markdown)
            debug_print("references_markdown", result.markdown.references_markdown)
            if isinstance(getattr(result.markdown, "fit_markdown", None), str):
                with open(os.path.join(md_dir, f"{url_id}_fit.md"), "w", encoding="utf-8") as f:
                    f.write(result.markdown.fit_markdown)
            debug_print("fit_markdown", getattr(result.markdown, "fit_markdown", None))
        else:
            if isinstance(result.markdown, str):
                with open(os.path.join(md_dir, f"{url_id}.md"), "w", encoding="utf-8") as f:
                    f.write(result.markdown)
            debug_print("markdown (str)", result.markdown)

def save_html(result, base_dir, url_id):
    """Save HTML variants."""
    if isinstance(result.html, str):        
        with open(os.path.join(base_dir, "html/raw", f"{url_id}.html"), "w", encoding="utf-8") as f:
            f.write(result.html)
    debug_print("html", result.html)
    if isinstance(result.cleaned_html, str):
        with open(os.path.join(base_dir, "html/cleaned", f"{url_id}.html"), "w", encoding="utf-8") as f:
            f.write(result.cleaned_html)
    debug_print("cleaned_html", result.cleaned_html)
    fit_html = getattr(result, "fit_html", None)
    if isinstance(fit_html, str):
        with open(os.path.join(base_dir, "html/fit", f"{url_id}.html"), "w", encoding="utf-8") as f:
            f.write(fit_html)
    debug_print("fit_html", fit_html)

def save_links(result, base_dir, url_id):
    """Save links as JSON."""
    debug_print("links", result.links)
    if isinstance(result.links, dict):
        with open(os.path.join(base_dir, "links", f"{url_id}.json"), "w", encoding="utf-8") as f:
            json.dump(result.links, f, ensure_ascii=False, indent=2)

def save_media(result, base_dir, url_id):
    """Save media metadata and files."""
    debug_print("media", result.media)
    if isinstance(result.media, dict):
        with open(os.path.join(base_dir, "media", f"{url_id}_media.json"), "w", encoding="utf-8") as f:
            json.dump(result.media, f, ensure_ascii=False, indent=2)
        # Optionally download images/audio/video if src is a URL
        # ...

def save_tables(result, base_dir, url_id):
    """Save tables as JSON."""
    debug_print("tables", result.tables)
    if isinstance(result.tables, list):
        with open(os.path.join(base_dir, "tables", f"{url_id}.json"), "w", encoding="utf-8") as f:
            json.dump(result.tables, f, ensure_ascii=False, indent=2)

def save_extracted_content(result, base_dir, url_id):
    """Save extracted content as JSON or text."""
    debug_print("extracted_content", result.extracted_content)
    if isinstance(result.extracted_content, str):
        with open(os.path.join(base_dir, "extracted_content", f"{url_id}.json"), "w", encoding="utf-8") as f:
            f.write(result.extracted_content)

def save_pdf(result, base_dir, url_id):
    """Save PDF file."""
    debug_print("pdf", result.pdf)
    if isinstance(result.pdf, (bytes, bytearray)):
        with open(os.path.join(base_dir, "pdf", f"{url_id}.pdf"), "wb") as f:
            f.write(result.pdf)

def save_mhtml(result, base_dir, url_id):
    """Save MHTML file."""
    debug_print("mhtml", result.mhtml)
    if isinstance(result.mhtml, str):
        with open(os.path.join(base_dir, "mhtml", f"{url_id}.mhtml"), "w", encoding="utf-8") as f:
            f.write(result.mhtml)

def save_screenshot(result, base_dir, url_id):
    """Save screenshot as PNG (base64-decoded)."""
    import base64
    debug_print("screenshot", result.screenshot)
    if isinstance(result.screenshot, str):
        try:
            img_bytes = base64.b64decode(result.screenshot)
            with open(os.path.join(base_dir, "screenshots", f"{url_id}.png"), "wb") as f:
                f.write(img_bytes)
        except Exception as e:
            print(f"[DEBUG] Error decoding screenshot: {e}")

def save_metadata(result, base_dir, url_id):
    """Save metadata, response headers, SSL info, etc."""
    meta = {}
    debug_print("metadata", result.metadata)
    debug_print("response_headers", result.response_headers)
    debug_print("ssl_certificate", result.ssl_certificate)
    debug_print("status_code", result.status_code)
    if result.metadata:
        meta["metadata"] = result.metadata
    if result.response_headers:
        meta["response_headers"] = result.response_headers
    if result.ssl_certificate:
        meta["ssl_certificate"] = str(result.ssl_certificate)
    if result.status_code:
        meta["status_code"] = result.status_code
    if meta:
        with open(os.path.join(base_dir, "metadata", f"{url_id}.json"), "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

def save_all(result, base_dir, url_id):
    """Save all fields from CrawlResult."""
    save_markdown(result, base_dir, url_id)
    save_html(result, base_dir, url_id)
    save_links(result, base_dir, url_id)
    save_media(result, base_dir, url_id)
    save_tables(result, base_dir, url_id)
    save_extracted_content(result, base_dir, url_id)
    save_pdf(result, base_dir, url_id)
    save_mhtml(result, base_dir, url_id)
    save_screenshot(result, base_dir, url_id)
    save_metadata(result, base_dir, url_id)
