import asyncio,json
from crawl4ai import AsyncWebCrawler, BrowserConfig,CrawlerRunConfig,CacheMode
from crawl4ai import JsonCssExtractionStrategy

async def extract_data_using_cssextractor():
    schema={
        "name":"Kidocourse",
        "baseSelector":"section.charge-methodology .w-tab-content > div",
        "fields":[
            {
                "name":"Title",
                "selector":"h3.heading-50",
                "type":"text",
            },
            {
                "name":"Description",
                "selector":".charge-content",
                "type":"text",

            },
            {
                "name":"Image",
                "selector":".image-92",
                "type":"attribute",
                "attribute":"src"
            },

        ],
    }

    browser_config=BrowserConfig(headless=True,java_script_enabled=True)

    js_click_tabs = """
    (async () => {
        const tabs = document.querySelectorAll("section.charge-methodology .tabs-menu-3 > div");
        for(let tab of tabs) {
            tab.scrollIntoView();
            tab.click();
            await new Promise(r => setTimeout(r, 500));
        }
    })();
    """

    crawler_config=CrawlerRunConfig(cache_mode=CacheMode.BYPASS,extraction_strategy=JsonCssExtractionStrategy(schema),js_code=[js_click_tabs],)

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result=await crawler.arun(url="https://www.kidocode.com/degrees/technology",config=crawler_config)
    companies=json.loads(result.extracted_content)
    print(f"Successfully extracted {len(companies)} companies")
    print(json.dumps(companies[1], indent=2))
    

async def main():
    await extract_data_using_cssextractor()

if __name__ == "__main__":
    asyncio.run(main())




