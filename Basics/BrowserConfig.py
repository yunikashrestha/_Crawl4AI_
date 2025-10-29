import asyncio 
from crawl4ai import AsyncWebCrawler,BrowserConfig,CrawlerRunConfig,CacheMode

async def main():
    browser_config=BrowserConfig(
        # headless=True,
        # verbose=True,
        browser_type="Chromium",
        proxy_config=None, #the crawler connects directly to websites using your machine’s IP address.
        viewport_height=1080,#defines the width of the browser window (in pixels) when the crawler loads a webpage.
        viewport_width=600, #defines the height of the browser viewport (visible area of the web page)
        use_persistent_context=None,
        
    )
