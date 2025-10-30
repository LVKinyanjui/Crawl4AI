"""
Asynchronous utility functions to save CrawlResult fields using aiofiles.
"""
import os
import json
import re
import aiofiles
from typing import Any

async def async_save_markdown(result, base_dir, url_id):
    md_dir = os.path.join(base_dir, "markdown")
    if result.markdown:
        if hasattr(result.markdown, "raw_markdown"):
            if isinstance(result.markdown.raw_markdown, str):
                async with aiofiles.open(os.path.join(md_dir, f"{url_id}_raw.md"), "w", encoding="utf-8") as f:
                    await f.write(result.markdown.raw_markdown)
            if isinstance(result.markdown.markdown_with_citations, str):
                async with aiofiles.open(os.path.join(md_dir, f"{url_id}_citations.md"), "w", encoding="utf-8") as f:
                    await f.write(result.markdown.markdown_with_citations)
            if isinstance(result.markdown.references_markdown, str):
                async with aiofiles.open(os.path.join(md_dir, f"{url_id}_references.md"), "w", encoding="utf-8") as f:
                    await f.write(result.markdown.references_markdown)
            if isinstance(getattr(result.markdown, "fit_markdown", None), str):
                async with aiofiles.open(os.path.join(md_dir, f"{url_id}_fit.md"), "w", encoding="utf-8") as f:
                    await f.write(result.markdown.fit_markdown)
        else:
            if isinstance(result.markdown, str):
                async with aiofiles.open(os.path.join(md_dir, f"{url_id}.md"), "w", encoding="utf-8") as f:
                    await f.write(result.markdown)

async def async_save_html(result, base_dir, url_id):
    if isinstance(result.html, str):
        async with aiofiles.open(os.path.join(base_dir, "html/raw", f"{url_id}.html"), "w", encoding="utf-8") as f:
            await f.write(result.html)
    if isinstance(result.cleaned_html, str):
        async with aiofiles.open(os.path.join(base_dir, "html/cleaned", f"{url_id}.html"), "w", encoding="utf-8") as f:
            await f.write(result.cleaned_html)
    fit_html = getattr(result, "fit_html", None)
    if isinstance(fit_html, str):
        async with aiofiles.open(os.path.join(base_dir, "html/fit", f"{url_id}.html"), "w", encoding="utf-8") as f:
            await f.write(fit_html)

async def async_save_links(result, base_dir, url_id):
    if isinstance(result.links, dict):
        async with aiofiles.open(os.path.join(base_dir, "links", f"{url_id}.json"), "w", encoding="utf-8") as f:
            await f.write(json.dumps(result.links, ensure_ascii=False, indent=2))

async def async_save_media(result, base_dir, url_id):
    if isinstance(result.media, dict):
        async with aiofiles.open(os.path.join(base_dir, "media", f"{url_id}_media.json"), "w", encoding="utf-8") as f:
            await f.write(json.dumps(result.media, ensure_ascii=False, indent=2))

async def async_save_tables(result, base_dir, url_id):
    if isinstance(result.tables, list):
        async with aiofiles.open(os.path.join(base_dir, "tables", f"{url_id}.json"), "w", encoding="utf-8") as f:
            await f.write(json.dumps(result.tables, ensure_ascii=False, indent=2))

async def async_save_extracted_content(result, base_dir, url_id):
    if isinstance(result.extracted_content, str):
        async with aiofiles.open(os.path.join(base_dir, "extracted_content", f"{url_id}.json"), "w", encoding="utf-8") as f:
            await f.write(result.extracted_content)

async def async_save_pdf(result, base_dir, url_id):
    if isinstance(result.pdf, (bytes, bytearray)):
        async with aiofiles.open(os.path.join(base_dir, "pdf", f"{url_id}.pdf"), "wb") as f:
            await f.write(result.pdf)

async def async_save_mhtml(result, base_dir, url_id):
    if isinstance(result.mhtml, str):
        async with aiofiles.open(os.path.join(base_dir, "mhtml", f"{url_id}.mhtml"), "w", encoding="utf-8") as f:
            await f.write(result.mhtml)

async def async_save_screenshot(result, base_dir, url_id):
    import base64
    if isinstance(result.screenshot, str):
        try:
            img_bytes = base64.b64decode(result.screenshot)
            async with aiofiles.open(os.path.join(base_dir, "screenshots", f"{url_id}.png"), "wb") as f:
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
        async with aiofiles.open(os.path.join(base_dir, "metadata", f"{url_id}.json"), "w", encoding="utf-8") as f:
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

