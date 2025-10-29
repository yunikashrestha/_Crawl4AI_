# import asyncio #asynchronous I/O library
# from crawl4ai import AsyncWebCrawler #lass handles both crawling and scraping

import asyncio
from crawl4ai import AsyncWebCrawler
async def main():
    async with AsyncWebCrawler() as crawler:
        result=await crawler.arun(url="https://hamrocsit.com")
        print (result.markdown[:300])
     
# The result is an object containing:
# result.markdown → clean, readable text.
# result.links → all links found.
# result.html → raw HTML if you need it.
# result.metadata → title, meta description, etc.

asyncio.run(main())

