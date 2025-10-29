# import asyncio
# from crawl4ai import AsyncWebCrawler,CrawlerRunConfig,CacheMode
# from crawl4ai.content_filter_strategy import PruningContentFilter#filters the less imp content using threshold
# from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator # converts HTMl into markdown applying content filter


# markdown_generator=DefaultMarkdownGenerator(content_filter=PruningContentFilter(threshold=0.3, threshold_type="fixed"))
# config=CrawlerRunConfig(cache_mode=CacheMode.BYPASS,markdown_generator=DefaultMarkdownGenerator)

# async with AsyncWebCrawler() as crawler:
#     result=await crawler.arun(url="https://hamrocsit.com",config=config
#                               )

import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def main():
    # Set up Markdown generator with content filtering
    md_generator = DefaultMarkdownGenerator(
        content_filter=PruningContentFilter(threshold=0.4, threshold_type="fixed")
    )

    # Configure crawler run
    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        markdown_generator=md_generator
    )

    # Run the crawler
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://hamrocsit.com", config=config)
        print("Raw Markdown length:", len(result.markdown.raw_markdown))#shows how much content was extracted before filtering.
        print("Fit Markdown length:", len(result.markdown.fit_markdown))#shows how much content remains after filtering

if __name__ == "__main__":
    asyncio.run(main())
