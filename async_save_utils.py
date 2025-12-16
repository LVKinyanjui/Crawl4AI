"""
Asynchronous utility functions to save CrawlResult fields using aiofiles.
"""
import os
import json
import re
import aiofiles
from typing import Any

def _ensure_dir(path: str) -> None:
    """Create a directory (and parents) if it doesn't exist.

    This helper is synchronous but cheap and safe to call from async code.
    """
    os.makedirs(path, exist_ok=True)

async def async_save_markdown(result, base_dir, url_id, types_to_save: set | None = None):
    md_dir = os.path.join(base_dir, "markdown")
    _ensure_dir(md_dir)
    if result.markdown:
        if hasattr(result.markdown, "raw_markdown"):
            # raw
            if (types_to_save is None) or ("raw" in types_to_save):
                if isinstance(result.markdown.raw_markdown, str):
                    async with aiofiles.open(os.path.join(md_dir, f"{url_id}_raw.md"), "w", encoding="utf-8") as f:
                        await f.write(result.markdown.raw_markdown)
            # citations
            if (types_to_save is None) or ("citations" in types_to_save):
                if isinstance(result.markdown.markdown_with_citations, str):
                    async with aiofiles.open(os.path.join(md_dir, f"{url_id}_citations.md"), "w", encoding="utf-8") as f:
                        await f.write(result.markdown.markdown_with_citations)
            # references
            if (types_to_save is None) or ("references" in types_to_save):
                if isinstance(result.markdown.references_markdown, str):
                    async with aiofiles.open(os.path.join(md_dir, f"{url_id}_references.md"), "w", encoding="utf-8") as f:
                        await f.write(result.markdown.references_markdown)
            # fit
            if (types_to_save is None) or ("fit" in types_to_save):
                if isinstance(getattr(result.markdown, "fit_markdown", None), str):
                    async with aiofiles.open(os.path.join(md_dir, f"{url_id}_fit.md"), "w", encoding="utf-8") as f:
                        await f.write(result.markdown.fit_markdown)
        else:
            # default single string markdown
            if (types_to_save is None) or ("default" in types_to_save):
                if isinstance(result.markdown, str):
                    async with aiofiles.open(os.path.join(md_dir, f"{url_id}.md"), "w", encoding="utf-8") as f:
                        await f.write(result.markdown)

async def async_save_html(result, base_dir, url_id):
    raw_dir = os.path.join(base_dir, "html", "raw")
    cleaned_dir = os.path.join(base_dir, "html", "cleaned")
    fit_dir = os.path.join(base_dir, "html", "fit")
    for _d in (raw_dir, cleaned_dir, fit_dir):
        _ensure_dir(_d)
    if isinstance(result.html, str):
        async with aiofiles.open(os.path.join(raw_dir, f"{url_id}.html"), "w", encoding="utf-8") as f:
            await f.write(result.html)
    if isinstance(result.cleaned_html, str):
        async with aiofiles.open(os.path.join(cleaned_dir, f"{url_id}.html"), "w", encoding="utf-8") as f:
            await f.write(result.cleaned_html)
    fit_html = getattr(result, "fit_html", None)
    if isinstance(fit_html, str):
        async with aiofiles.open(os.path.join(fit_dir, f"{url_id}.html"), "w", encoding="utf-8") as f:
            await f.write(fit_html) 

async def async_save_links(result, base_dir, url_id):
    links_dir = os.path.join(base_dir, "links")
    _ensure_dir(links_dir)
    if isinstance(result.links, dict):
        async with aiofiles.open(os.path.join(links_dir, f"{url_id}.json"), "w", encoding="utf-8") as f:
            await f.write(json.dumps(result.links, ensure_ascii=False, indent=2))

async def async_save_media(result, base_dir, url_id):
    media_dir = os.path.join(base_dir, "media")
    _ensure_dir(media_dir)
    if isinstance(result.media, dict):
        async with aiofiles.open(os.path.join(media_dir, f"{url_id}_media.json"), "w", encoding="utf-8") as f:
            await f.write(json.dumps(result.media, ensure_ascii=False, indent=2))

async def async_save_tables(result, base_dir, url_id):
    tables_dir = os.path.join(base_dir, "tables")
    _ensure_dir(tables_dir)
    if isinstance(result.tables, list):
        async with aiofiles.open(os.path.join(tables_dir, f"{url_id}.json"), "w", encoding="utf-8") as f:
            await f.write(json.dumps(result.tables, ensure_ascii=False, indent=2))

async def async_save_extracted_content(result, base_dir, url_id):
    extracted_dir = os.path.join(base_dir, "extracted_content")
    _ensure_dir(extracted_dir)
    if isinstance(result.extracted_content, str):
        async with aiofiles.open(os.path.join(extracted_dir, f"{url_id}.json"), "w", encoding="utf-8") as f:
            await f.write(result.extracted_content) 

async def async_save_pdf(result, base_dir, url_id):
    pdf_dir = os.path.join(base_dir, "pdf")
    _ensure_dir(pdf_dir)
    if isinstance(result.pdf, (bytes, bytearray)):
        async with aiofiles.open(os.path.join(pdf_dir, f"{url_id}.pdf"), "wb") as f:
            await f.write(result.pdf) 

async def async_save_mhtml(result, base_dir, url_id):
    mhtml_dir = os.path.join(base_dir, "mhtml")
    _ensure_dir(mhtml_dir)
    if isinstance(result.mhtml, str):
        async with aiofiles.open(os.path.join(mhtml_dir, f"{url_id}.mhtml"), "w", encoding="utf-8") as f:
            await f.write(result.mhtml) 

async def async_save_screenshot(result, base_dir, url_id):
    import base64
    screenshots_dir = os.path.join(base_dir, "screenshots")
    _ensure_dir(screenshots_dir)
    if isinstance(result.screenshot, str):
        try:
            img_bytes = base64.b64decode(result.screenshot)
            async with aiofiles.open(os.path.join(screenshots_dir, f"{url_id}.png"), "wb") as f:
                await f.write(img_bytes)
        except Exception as e:
            print(f"[DEBUG] Error decoding screenshot: {e}")

async def async_save_metadata(result, base_dir, url_id):
    meta = {}
    if result.metadata:
        meta["metadata"] = result.metadata
    if result.response_headers:
        meta["response_headers"] = result.response_headers
    if result.ssl_certificate:
        meta["ssl_certificate"] = str(result.ssl_certificate)
    if result.status_code:
        meta["status_code"] = result.status_code
    if meta:
        metadata_dir = os.path.join(base_dir, "metadata")
        _ensure_dir(metadata_dir)
        async with aiofiles.open(os.path.join(metadata_dir, f"{url_id}.json"), "w", encoding="utf-8") as f:
            await f.write(json.dumps(meta, ensure_ascii=False, indent=2))

async def async_save_all(result, base_dir, url_id):
    await async_save_markdown(result, base_dir, url_id)
    await async_save_html(result, base_dir, url_id)
    await async_save_links(result, base_dir, url_id)
    await async_save_media(result, base_dir, url_id)
    await async_save_tables(result, base_dir, url_id)
    await async_save_extracted_content(result, base_dir, url_id)
    await async_save_pdf(result, base_dir, url_id)
    await async_save_mhtml(result, base_dir, url_id)
    await async_save_screenshot(result, base_dir, url_id)
    await async_save_metadata(result, base_dir, url_id)


async def async_save_filtered(result, base_dir, url_id, selected: set | None):
    """Save only selected sections. If `selected` is falsy, save everything.

    `selected` is a set of strings matching the short names: 'markdown', 'html',
    'links', 'media', 'tables', 'extracted', 'pdf', 'mhtml', 'screenshots', 'metadata'
    """
    if not selected:
        await async_save_all(result, base_dir, url_id)
        return

    if "markdown" in selected:
        await async_save_markdown(result, base_dir, url_id)
    if "html" in selected:
        await async_save_html(result, base_dir, url_id)
    if "links" in selected:
        await async_save_links(result, base_dir, url_id)
    if "media" in selected:
        await async_save_media(result, base_dir, url_id)
    if "tables" in selected:
        await async_save_tables(result, base_dir, url_id)
    if "extracted" in selected:
        await async_save_extracted_content(result, base_dir, url_id)
    if "pdf" in selected:
        await async_save_pdf(result, base_dir, url_id)
    if "mhtml" in selected:
        await async_save_mhtml(result, base_dir, url_id)
    if "screenshots" in selected:
        await async_save_screenshot(result, base_dir, url_id)
    if "metadata" in selected:
        await async_save_metadata(result, base_dir, url_id)

