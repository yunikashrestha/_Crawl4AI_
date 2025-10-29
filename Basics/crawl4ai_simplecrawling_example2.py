import asyncio
from crawl4ai import AsyncWebCrawler,BrowserConfig,CrawlerRunConfig,CacheMode

async def main():
    brow_config=BrowserConfig(headless=True,verbose=True)#verbose=> print information about what the browser is doing — such as which pages it’s loading, errors encountered, JavaScript execution logs, etc.

    run_config=CrawlerRunConfig(
        word_count_threshold=10, #minimum number of words a text block must have to be considered useful.
        exclude_external_links=True, #crawler not to follow or include links
        remove_overlay_elements=True,#Removes popups, modals, cookie banners, and overlay elements
        cache_mode=CacheMode.ENABLED
        #the crawler stores pages (HTML, processed results, etc.) in its local cache.
        #The next time you crawl the same URL, it will reuse the cached content instead of fetching it again from the internet — unless the cache expires or is cleared.
          

    )

    async with AsyncWebCrawler(config=brow_config) as crawler:
        result=await crawler.arun(url="https://hamrocsit.com/semester/eight/",config=run_config)
    
    if result.success:
       #Print clean content
        print("**********Content************:" ,result.markdown)

        #For images in page 
        for image in result.media["images"]:
            print(f"******Images:{image['src']}")

        #For links
        for link in result.links["internal"]:
            print(f"************Links: {link['href']}")

    
    else:
        print(f"Crawl Failed {result.error_message}")
        print(f"Status code {result.status_code}")

if __name__=="__main__":
    asyncio.run(main())


