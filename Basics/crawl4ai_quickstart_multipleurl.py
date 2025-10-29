import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig,CacheMode

async def multiple_url_crawler():
    urls=[
        "https://hamrocsit.com",
        "https://example.com/page1",
        "https://example.com/page2"

    ]
    run_config=CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        stream=True # enable streaming mode=>the crawler will yield results as soon as each page finishes, without waiting for the others.

    )
    async with AsyncWebCrawler() as crawler:
        async for result in await crawler.arun_many(urls,config=run_config):
            if result.success:
                print(f"OK {result.url}, length:{len(result.markdown.raw_markdown)}")
            else:
                print(f"[ERROR]{result.url}=>{result.error_message}")
            print(result.markdown)

if __name__=="__main__":
    asyncio.run(multiple_url_crawler())