import asyncio
import os
from crawl_results.save_utils import save_all
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode



# TODO; Make this a CLI argument with argparse
url = "https://cleitonleonel.github.io/pyquotex/en/"

async def main(url):
    browser_config = BrowserConfig(
        browser_type="chromium",
        verbose=True,
        )
    run_config = CrawlerRunConfig(
        # Content filtering
        word_count_threshold=10,
        excluded_tags=['form', 'header'],
        exclude_external_links=True,

        # Content processing
        process_iframes=True,
        remove_overlay_elements=True,

        # Cache control
        cache_mode=CacheMode.ENABLED,  # Use cache if available

        screenshot=True,
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url=url,
            config=run_config
        )

        import hashlib
        url_id = hashlib.md5(url.encode()).hexdigest()
        base_dir = os.path.join(os.path.dirname(__file__), "crawl_results")

        # Defensive checks for CrawlResult fields
        if hasattr(result, "success") and result.success:
            save_all(result, base_dir, url_id)
            print(f"Saved crawl results for {url} to {base_dir}")

            # Print clean content
            if result.markdown:
                if hasattr(result.markdown, "raw_markdown"):
                    print("Content:", result.markdown.raw_markdown[:500])
                else:
                    print("Content:", str(result.markdown)[:500])

            # Process images
            if result.media and "images" in result.media:
                for image in result.media["images"]:
                    print(f"Found image: {image.get('src')}")

            # Process links
            if result.links and "internal" in result.links:
                for link in result.links["internal"]:
                    print(f"Internal link: {link.get('href')}")
        else:
            error_msg = getattr(result, "error_message", "Unknown error")
            print(f"Crawl failed: {error_msg}")

if __name__ == "__main__":
    asyncio.run(main(url))
