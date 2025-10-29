import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter

async def main():
    brows_config=BrowserConfig(headless=True)
    run_config=CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        markdown_generator=DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(threshold=0.6),
            options={"ignore_links":True}
        )
    )
    async with AsyncWebCrawler(config=brows_config) as crawler:
        result=await crawler.arun(url="https://example.com",config=run_config)
        # Different content formats
    print(result.html)    
    print("****Cleaned HTML*******")     # Raw HTML
    print(result.cleaned_html) # Cleaned HTML
    print("****RAW MARKDOWN*******")   
    print(result.markdown.raw_markdown) # Raw markdown from cleaned html
    print("****FIT MARKDOWN*******")  
    print(result.markdown.fit_markdown) # Most relevant content in markdown

    # Check success status
    print(result.success)      # True if crawl succeeded
    print(result.status_code)  # HTTP status code (e.g., 200, 404)

    # Access extracted media and links
    print(result.media)        # Dictionary of found media (images, videos, audio)
    print(result.links)        # Dictionary of internal and external links

if __name__=="__main__":
    asyncio.run(main())



