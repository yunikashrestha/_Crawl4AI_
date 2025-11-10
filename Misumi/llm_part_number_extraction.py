import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode, BrowserConfig, CrawlerRunConfig, LLMConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from bs4 import BeautifulSoup
import uuid
import json
import pandas as pd
from dotenv import load_dotenv
import os
import re

async def extract_product_details(url: str, api_key: str, browser_config: BrowserConfig, session_id: str):
    """Extract product details from a single Misumi product URL using JSON-CSS extraction."""
    
    #Step 1: Merge JS and prepare structure ---
    merge_js = """
        setTimeout(()=>{
            const langButton = document.querySelector('a[lang="en"]');
            if (langButton) langButton.click();
        }, 3000);

        setTimeout(() => {
            const partTab = document.querySelector('a#codeList');
            if (partTab) partTab.click();

            setTimeout(()=>{
                const partRows = document.querySelectorAll('tr.PartNumberColumn_dataRow__43D6Y');
                const priceRows = document.querySelectorAll('tr.PartNumberAsideColumns_dataRow__OUw8N');
                const specRows = document.querySelectorAll('tr.PartNumberSpecColumns_dataRow__M4B4a');
                
                const mainContainer = document.querySelector('div.PartNumberList_mainOuter__d74Qg');
                const mergedContainer = document.createElement('div');
                mergedContainer.classList.add('mergedRowContainer');
                
                const numRows = Math.min(partRows.length, priceRows.length, specRows.length);
                for (let i = 0; i < numRows; i++) {
                    const row = document.createElement('div');
                    row.classList.add('mergedRow');
                    row.appendChild(partRows[i]);
                    row.appendChild(priceRows[i]);
                    row.appendChild(specRows[i]);
                    mainContainer.appendChild(row);
                }
            }, 8000);
        }, 8000);
    """

    # Step 2: Generate schema dynamically from page content ---
    async with AsyncWebCrawler(config=browser_config) as crawler:
        initial_config = CrawlerRunConfig(
            delay_before_return_html=20.0,
            js_code=merge_js,
            wait_for="css:div.PartNumberList_mainOuter__d74Qg"
        )
        
        print(f"Generating schema for {url}")
        initial_result = await crawler.arun(url=url, config=initial_config)
        soup = BeautifulSoup(initial_result.html, "html.parser")

        title_element = soup.select_one("h1.PageHeading_wrap__K1c1n")
        sub_category = title_element.get_text(strip=True) if title_element else "unknown_product"

        container = soup.select_one("div.PartNumberList_mainOuter__d74Qg")
        if not container:
            print(f"No container found for {url}")
            return None, sub_category

        cleaned_html = str(container)

        query = (
            "Generate a schema to extract product details. "
            "The column names from the tables MUST be exact. "
            "Only use the table column names as key_fields in the JSON schema. "
            "Split the 'Part Number' header into two keys - Part Number Name and Part Number URL. "
            "You MUST use CSS selectors, not XPath. The base selector should be 'div.mergedRow'."
        )

        css_schema = JsonCssExtractionStrategy.generate_schema(
            html=cleaned_html,
            schema_type="css",
            query=query,
            llm_config=LLMConfig(provider="gemini/gemini-2.5-flash", api_token=api_key)
        )

        #Step 3: Actual JSON extraction with the generated schema ---
        run_config = CrawlerRunConfig(
            extraction_strategy=JsonCssExtractionStrategy(schema=css_schema),
            markdown_generator=DefaultMarkdownGenerator(),
            js_code=merge_js,
            css_selector="div.mergedRow",
            word_count_threshold=10,
            process_iframes=True,
            cache_mode=CacheMode.DISABLED,
            delay_before_return_html=30.0,
            wait_for="css:div.PartNumberList_mainOuter__d74Qg",
            session_id=session_id,
            remove_overlay_elements=True
        )

        print(f"Extracting data for {url}")
        result = await crawler.arun(url=url, config=run_config)

        if not result.success:
            print(f"Extraction failed for {url}")
            return None, sub_category

        try:
            data = json.loads(result.extracted_content)
            print(f"Extracted {len(data)} rows for {sub_category}")
            return data, sub_category
        except json.JSONDecodeError:
            print(f"JSON decode error for {url}")
            return None, sub_category


async def json_css_product_extraction():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    session_id = str(uuid.uuid4())
    browser_config = BrowserConfig(headless=True, verbose=True)

    # --- Read product URLs from file ---
    input_file = "misumi_camFollower.txt"
    if not os.path.exists(input_file):
        print("No misumi_camFollower.txt found. Run link extractor first.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        urls = [u.strip() for u in f if u.strip()]

    print(f"Found {len(urls)} product URLs to scrape.\n")

    all_data = []
    for idx, url in enumerate(urls, 1):
        print(f"\n============================")
        print(f"Scraping ({idx}/{len(urls)}): {url}")
        print("============================\n")

        try:
            data, sub_category = await extract_product_details(url, api_key, browser_config, session_id)
            if data:
                for item in data:
                    item["Source_URL"] = url
                all_data.extend(data)
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    if all_data:
        df = pd.DataFrame(all_data)
        file_name = f"camfollower_all_products.xlsx"
        df.to_excel(file_name, index=False)
        print(f"\nAll data saved to {file_name}")
    else:
        print("\nNo data extracted from any URL.")


if __name__ == "__main__":
    asyncio.run(json_css_product_extraction())
