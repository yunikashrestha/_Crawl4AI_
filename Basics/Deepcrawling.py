import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from bs4 import BeautifulSoup

async def main():
    browser_config = BrowserConfig(headless=False, verbose=True)

    run_config = CrawlerRunConfig(
        word_count_threshold=20,
        markdown_generator=DefaultMarkdownGenerator(),
        excluded_tags=["nav", "header", "footer", "style"],
        remove_forms=True,
        parser_type="lxml",
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            include_external=False,
            max_pages=200,
            max_depth=2
        ),
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        results = await crawler.arun(
            url="https://hamrocsit.com/",  
            config=run_config,
            deep_crawl=True
        )

    if results:
        total = len(results)
        print(f"Total pages crawled: {total}")

        # Replace "target-class" with the class used by your website for main content
        target_classes = ["main_content"]

        # Open files for saving URLs and content
        with open("filtered_urls.txt", "w", encoding="utf-8") as f_urls, \
             open("markdown.md", "w", encoding="utf-8") as f_content:

            for i, result in enumerate(results, start=1):
                # Save URL if available
                if hasattr(result, "url") and result.url:
                    print(f"[{i}/{total}] Found: {result.url}")
                    f_urls.write(result.url + "\n")

                # Extract and save content if HTML is available
                if hasattr(result, "html") and result.html:
                    soup = BeautifulSoup(result.html, "html.parser")
                    divs = []
                    for cls in target_classes:
                        divs.extend(soup.find_all("div", class_=cls))

                    if divs:
                        content = "\n\n".join(str(div) for div in divs)
                        f_content.write(content + "\n\n---\n\n")
                    else:
                        print(f"No <div> with target class found in {getattr(result, 'url', 'Unknown URL')}")

        print(" Crawl complete. Results saved to 'filtered_urls.txt' and 'markdown.md'")

    else:
        print(" Crawl failed or returned no results.")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
