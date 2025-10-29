# Adaptive crawling =>It is the advanced and intelligent crawling which automatically determines when the sufficient inforamtion is gathered 
import asyncio
from crawl4ai import AsyncWebCrawler, AdaptiveCrawler

async def adaptive_example():

    async with AsyncWebCrawler() as crawler:
        adaptive=AdaptiveCrawler(crawler)

        result=await adaptive.digest(
            start_url="https://hamrocsit.com/semester/eight/",
            query=" BSc CSIT course 8th  semester and number of subjects in this semester",
            
        )
        adaptive.print_stats()
        
        print(f"Crawled {len(result.crawled_urls)} pages")
        print(f"Achieved {adaptive.confidence:.0%} confidence")

if __name__=="__main__":
    asyncio.run(adaptive_example())

