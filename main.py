import asyncio
import os
from save_utils import save_all, url_to_filename
from crawl4ai import AsyncWebCrawler
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode 
from crawl4ai.async_dispatcher import MemoryAdaptiveDispatcher
from crawl4ai import CrawlerMonitor, DisplayMode
from crawl4ai import RateLimiter

from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(description="Crawl a website and save results.")
    parser.add_argument('--base-url', required=True, help='Base URL to crawl')
    args = parser.parse_args()
    print(f"[DEBUG] Parsed base_url: {args.base_url}")  # Test parsing
    return args


async def main(url):
    browser_config = BrowserConfig(
        browser_type="chromium",
        verbose=True,
        )
    
    dispatcher = MemoryAdaptiveDispatcher(
        memory_threshold_percent=70.0,
        check_interval=1.0,
        max_session_permit=10,
        monitor=CrawlerMonitor(
            # display_mode=DisplayMode.DETAILED
        )
    )
    
    run_config = CrawlerRunConfig(
        # Deep crawling
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=2,
            include_external=False,
        ),
        
        scraping_strategy=LXMLWebScrapingStrategy(),

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

    from uuid import uuid4

    async with AsyncWebCrawler(config=browser_config) as crawler:
        for result in await crawler.arun(
            url=url,
            config=run_config,
            dispatcher=dispatcher,
        ):
           # CrawlResult
           single_result = result._results[0] if len(result._results) == 1 else "None or Multiple Results"
           base_dir = os.path.join(os.path.dirname(__file__), "crawl_results")
           
           file_name = str()
           if single_result.url:
              file_name = url_to_filename(single_result.url)
           else:
              file_name = str(uuid4())

           save_all(single_result, base_dir, file_name)

if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(args.base_url))
