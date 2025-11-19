"""
Utility functions to save CrawlResult fields to the organized directory structure.
"""
import os
import json
import re
from typing import Any

def debug_print(attr_name, value):
    print(f"[DEBUG] {attr_name}: type={type(value)}, value={repr(value)[:200]}")

def ensure_dir_exists(directory: str):
    """Ensure a directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_markdown(result, base_dir, url_id):
    """Save markdown fields from CrawlResult."""
    md_dir = os.path.join(base_dir, "markdown")
    ensure_dir_exists(md_dir)
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
    raw_html_dir = os.path.join(base_dir, "html/raw")
    cleaned_html_dir = os.path.join(base_dir, "html/cleaned")
    fit_html_dir = os.path.join(base_dir, "html/fit")
    ensure_dir_exists(raw_html_dir)
    ensure_dir_exists(cleaned_html_dir)
    ensure_dir_exists(fit_html_dir)
    if isinstance(result.html, str):        
        with open(os.path.join(raw_html_dir, f"{url_id}.html"), "w", encoding="utf-8") as f:
            f.write(result.html)
    debug_print("html", result.html)
    if isinstance(result.cleaned_html, str):
        with open(os.path.join(cleaned_html_dir, f"{url_id}.html"), "w", encoding="utf-8") as f:
            f.write(result.cleaned_html)
    debug_print("cleaned_html", result.cleaned_html)
    fit_html = getattr(result, "fit_html", None)
    if isinstance(fit_html, str):
        with open(os.path.join(fit_html_dir, f"{url_id}.html"), "w", encoding="utf-8") as f:
            f.write(fit_html)
    debug_print("fit_html", fit_html)

def save_links(result, base_dir, url_id):
    """Save links as JSON."""
    links_dir = os.path.join(base_dir, "links")
    ensure_dir_exists(links_dir)
    debug_print("links", result.links)
    if isinstance(result.links, dict):
        with open(os.path.join(links_dir, f"{url_id}.json"), "w", encoding="utf-8") as f:
            json.dump(result.links, f, ensure_ascii=False, indent=2)

def save_media(result, base_dir, url_id):
    """Save media metadata and files."""
    media_dir = os.path.join(base_dir, "media")
    ensure_dir_exists(media_dir)
    debug_print("media", result.media)
    if isinstance(result.media, dict):
        with open(os.path.join(media_dir, f"{url_id}_media.json"), "w", encoding="utf-8") as f:
            json.dump(result.media, f, ensure_ascii=False, indent=2)
        # Optionally download images/audio/video if src is a URL
        # ...

def save_tables(result, base_dir, url_id):
    """Save tables as JSON."""
    tables_dir = os.path.join(base_dir, "tables")
    ensure_dir_exists(tables_dir)
    debug_print("tables", result.tables)
    if isinstance(result.tables, list):
        with open(os.path.join(tables_dir, f"{url_id}.json"), "w", encoding="utf-8") as f:
            json.dump(result.tables, f, ensure_ascii=False, indent=2)

def save_extracted_content(result, base_dir, url_id):
    """Save extracted content as JSON or text."""
    extracted_content_dir = os.path.join(base_dir, "extracted_content")
    ensure_dir_exists(extracted_content_dir)
    debug_print("extracted_content", result.extracted_content)
    if isinstance(result.extracted_content, str):
        with open(os.path.join(extracted_content_dir, f"{url_id}.json"), "w", encoding="utf-8") as f:
            f.write(result.extracted_content)

def save_pdf(result, base_dir, url_id):
    """Save PDF file."""
    pdf_dir = os.path.join(base_dir, "pdf")
    ensure_dir_exists(pdf_dir)
    debug_print("pdf", result.pdf)
    if isinstance(result.pdf, (bytes, bytearray)):
        with open(os.path.join(pdf_dir, f"{url_id}.pdf"), "wb") as f:
            f.write(result.pdf)

def save_mhtml(result, base_dir, url_id):
    """Save MHTML file."""
    mhtml_dir = os.path.join(base_dir, "mhtml")
    ensure_dir_exists(mhtml_dir)
    debug_print("mhtml", result.mhtml)
    if isinstance(result.mhtml, str):
        with open(os.path.join(mhtml_dir, f"{url_id}.mhtml"), "w", encoding="utf-8") as f:
            f.write(result.mhtml)

def save_screenshot(result, base_dir, url_id):
    """Save screenshot as PNG (base64-decoded)."""
    import base64
    screenshots_dir = os.path.join(base_dir, "screenshots")
    ensure_dir_exists(screenshots_dir)
    debug_print("screenshot", result.screenshot)
    if isinstance(result.screenshot, str):
        try:
            img_bytes = base64.b64decode(result.screenshot)
            with open(os.path.join(screenshots_dir, f"{url_id}.png"), "wb") as f:
                f.write(img_bytes)
        except Exception as e:
            print(f"[DEBUG] Error decoding screenshot: {e}")

def save_metadata(result, base_dir, url_id):
    """Save metadata, response headers, SSL info, etc."""
    metadata_dir = os.path.join(base_dir, "metadata")
    ensure_dir_exists(metadata_dir)
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
        with open(os.path.join(metadata_dir, f"{url_id}.json"), "w", encoding="utf-8") as f:
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

def url_to_filename(url: str) -> str:
    """Convert a URL to a safe filename: example_com_login"""
    # Remove protocol
    url = re.sub(r'^https?://', '', url)
    # Remove query params and fragments
    url = re.sub(r'[?#].*$', '', url)
    # Replace non-alphanum (except / and .) with nothing
    url = re.sub(r'[^\w./-]', '', url)
    # Replace dots and slashes with underscores
    url = url.replace('.', '_').replace('/', '_')
    # Remove leading/trailing underscores
    url = url.strip('_')
    return url
