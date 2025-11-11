import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import uuid

async def internal_links_extraction():
    
    browser_config = BrowserConfig(headless=True)
    session_id = str(uuid.uuid4())

    config_run = CrawlerRunConfig(
        # ... (most settings are fine, kept for completeness) ...
        word_count_threshold=50,
        markdown_generator=DefaultMarkdownGenerator(),
        excluded_tags=["header","nav","footer","style","script","aside"],
        only_text=False,
        remove_forms=True,
        parser_type="lxml",
        disable_cache=False,
        no_cache_read=False,
        no_cache_write=False,
        method="GET",
        check_robots_txt=False,
        delay_before_return_html=20.0,
        mean_delay=2.0,
        max_range=6.0,
        semaphore_count=5,
        scan_full_page=False,
        scroll_delay=1.5,
        max_scroll_steps=3,
        process_iframes=True,
        remove_overlay_elements=True,
        simulate_user=True,
        exclude_social_media_domains=[],
        exclude_social_media_links=True,
        exclude_external_links=True,
        exclude_domains=[],
        # Key selector for extraction:
        css_selector="a.PhotoItem_seriesNameLink__pq1vO",
        verbose=True,
        capture_console_messages=False,
        capture_network_requests=False,
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        results = await crawler.arun(
            url="https://vn.misumi-ec.com/vona2/mech/M0800000000/M0807000000/?KWSearch=cam+follower&searchFlow=results2category",
            config=config_run
        )

        if results.success:
            internal_links = []
            # --- START OF FIX ---
            # 1. Access the links directly from the results object
            # 2. Iterate only over the 'internal' links list
            for link_data in results.links.get("internal", []):
                # 'link_data' is a dictionary like: {'href': '...', 'text': '...'}
                url = link_data.get("href")
                
                if url: # Check if href exists
                    print(f"Found Link Data: {link_data}")
                    print(f"Extracted URL: {url}")
                    internal_links.append(url)
                    
                    # Write URL to file
                    with open("misumi_camFollower.txt", "a", encoding="utf-8") as f:
                        f.write(url + "\n")
            print(f"Saved {len(internal_links)} products url")
            return internal_links
            # --- END OF FIX ---
        else:
            print("Crawler run failed or returned no results.")
        return internal_links


async def main():
    await internal_links_extraction()

if __name__ == "__main__":
    asyncio.run(main())

