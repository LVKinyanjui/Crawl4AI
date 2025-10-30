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
from crawl4ai.deep_crawling import BestFirstCrawlingStrategy
from crawl4ai.deep_crawling.scorers import KeywordRelevanceScorer


from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(description="Crawl a website and save results.")
    # Allow base URL to be supplied either positionally or via --base-url
    parser.add_argument('base_url', nargs='?', help='Base URL to crawl (positional)')
    parser.add_argument('--base-url', dest='base_url', help='Base URL to crawl (optional flag)')
    parser.add_argument('--max-depth', type=int, default=2, help='Maximum crawl depth')
    parser.add_argument('--max-pages', type=int, default=50, help='Maximum number of pages to crawl')
    parser.add_argument('--memory', type=float, default=50.0, help='Memory threshold percent for dispatcher (0-100)')
    parser.add_argument('--keywords', nargs='+', default=[], help='List of keywords to score pages during crawling')

    parser.add_argument('--managed', action='store_true', help='Use managed browser service')
    parser.add_argument('--user-data-dir', type=str, help='Path to user data directory for the browser profile')
    args = parser.parse_args()

    # Enforce that base_url is provided either positionally or with the flag
    if not args.base_url:
        parser.error("the following arguments are required: base_url (positional or --base-url)")

    if args.user_data_dir and not args.managed:
        print("[WARNING] --user-data-dir is only used with --managed. It will be ignored.")
    print(f"[DEBUG] Parsed args: {args}")
    return args

async def main(args):
    if args.managed:
        user_data_dir = args.user_data_dir or "/home/jovian/.cache/ms-playwright/profiles/chrome_profile"
        browser_config = BrowserConfig(
            headless=True,
            use_managed_browser=True,
            user_data_dir=user_data_dir,
            browser_type="chromium"
        )
    else:
        browser_config = BrowserConfig(
            browser_type="chromium",
            verbose=True,
            )
    
    dispatcher = MemoryAdaptiveDispatcher(
        memory_threshold_percent=args.memory,
        check_interval=1.0,
        max_session_permit=5,
        monitor=CrawlerMonitor(
            # display_mode=DisplayMode.DETAILED
        )
    )

    # Create a scorer
    scorer = KeywordRelevanceScorer(
        keywords=args.keywords,
        weight=0.7
    )

    # deep_crawl_strategy=BFSDeepCrawlStrategy(
    #     max_depth=args.max_depth,
    #     include_external=False,
    # )

    # Recommended
    deep_crawl_strategy = BestFirstCrawlingStrategy(
        max_depth=args.max_depth,
        include_external=False,
        url_scorer=scorer,
        max_pages=args.max_pages,
    )

    
    run_config = CrawlerRunConfig(
        # Deep crawling
        deep_crawl_strategy=deep_crawl_strategy,
        
        scraping_strategy=LXMLWebScrapingStrategy(),

        # Content filtering
        # TODO: Investigatte what this is
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
        # # NON-STREAMING MODE
        # # Treats results as batches
        # # For when time is not a crucial factor
        # for result in await crawler.arun(
        #     url=args.base_url,
        #     config=run_config,
        #     dispatcher=dispatcher,
        # ):
        #    # CrawlResult
        #    single_result = result._results[0] if len(result._results) == 1 else "None or Multiple Results"
        #    base_dir = os.path.join(os.path.dirname(__file__), "crawl_results")
           
        #    file_name = str()
        #    if single_result.url:
        #       file_name = url_to_filename(single_result.url)
        #    else:
        #       file_name = str(uuid4())

        #    save_all(single_result, base_dir, file_name)

        # STREAMING MODE
        # TODO: This is monkey patching. Need to enable stream at config init with constructor
        run_config.stream = True
        async for result in await crawler.arun(
            url=args.base_url,
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
    asyncio.run(main(args))
