import asyncio
import json 
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig,CacheMode
from crawl4ai import JsonCssExtractionStrategy

async def main():
    schema={
        "name":"Example Items",
        "baseSelector":"div.item",
        "fields":[
            {"name":"title","selector":"h2","type":"text"},
           {"name":"link","selector":"a","type":"attribute","attribute":"href"},
           {"name":"para","selector":"p","type":"text"}
        ]

    }

    raw_html="<div class='item'><h2>Item this is heading</h2><a href="'https://example.com/item1'">Click here</a><p>Hello</p></div>"
    async with AsyncWebCrawler() as crawler:
        result=await crawler.arun("raw://"+raw_html,config=CrawlerRunConfig(cache_mode=CacheMode.BYPASS,extraction_strategy=JsonCssExtractionStrategy(schema)))
    
    data=json.loads(result.extracted_content)
    print(data)

if __name__=="__main__":
    asyncio.run(main())

