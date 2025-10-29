import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

async def main():
    browser_config=BrowserConfig(headless=True)# browser is not seen
    run_config=CrawlerRunConfig(cache_mode=CacheMode.BYPASS) #BYPASS= not to use any cached pages — it will always fetch fresh content

    async with AsyncWebCrawler() as crawler:
        result=await crawler.arun(url="https://hamrocsit.com")
        print(result.markdown)

if __name__=="__main__":
    asyncio.run(main())


