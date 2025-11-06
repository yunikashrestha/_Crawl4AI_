# import asyncio
# from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
# from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
# import random
# import uuid

# async def scrape_multiple_urls():
#     # Set headless=False for visual debugging, set to True for production speed
#     # Increasing global timeout to 90 seconds (90000ms) for stability
#     brows_config = BrowserConfig(headless=False, verbose=True, browser_type="chromium", timeout=90000)
    
#     MIN_DELAY = 5.0
#     MAX_DELAY = 10.0
#     session_id = str(uuid.uuid4())

#     run_config = CrawlerRunConfig(
#         cache_mode=CacheMode.BYPASS,
#         markdown_generator=DefaultMarkdownGenerator(),
#         word_count_threshold=5, 
#         exclude_all_images=[],
#         exclude_external_links=True,
#         only_text=False,
        
#         # FINAL SELECTOR: Targeting the actual table class
#         css_selector="table.PartNumberColumn_tableBase__DK2Le",
        
#         excluded_tags=["header","footer","nav","style","script","aside","form"],
        
#         # --- FINAL FIX: Corrected JavaScript Structure and Timing ---
#         js_code = """
#             // 1. ATTEMPT TO CLICK COOKIE BANNER (Assuming selector works)
#             const cookieButton = document.querySelector('button[aria-label="Accept cookies"]'); 
#             if (cookieButton) {
#                 cookieButton.click();
#             }

#             // 2. SCROLL & CLICK MAIN TAB
#             const tab = document.querySelector('a[href="#codeList"]');
#             if (tab) {
#                 // Scroll the tab into view
#                 tab.scrollIntoView({ behavior: 'smooth', block: 'center' });
                
#                 // Use a short timeout to wait for the scroll to complete before clicking
#                 setTimeout(() => {
#                     tab.click();
#                 }, 500); 
                
#                 // Return a Promise that holds the scraper for 10 seconds (10000ms) 
#                 // to let the dynamic table content fully load after the click.
#                 return new Promise(resolve => setTimeout(resolve, 10000));
#             }
#             return false;
#         """,
#         # --- END FINAL FIX ---

#         js_only=False,
#         scan_full_page=False,
#         simulate_user=True,
#         scroll_delay=1.0, # Reduced scroll delay for responsiveness
#         delay_before_return_html=10.0, # Initial page load wait
#         max_scroll_steps=10,
#         process_iframes=True,
#         remove_overlay_elements=True,
#         method="GET",
#         check_robots_txt="False",
#         session_id=session_id,
#         # Using 'load' is generally safer than 'networkidle' for dynamic sites
#         wait_until="load" 
#     )
    
#     # Assuming "misumi_camFollower.txt" exists and contains one URL per line
#     try:
#         with open("misumi_camFollower.txt","r",encoding="utf-8") as f:
#             urls=[line.strip() for line in f if line.strip()]
#     except FileNotFoundError:
#         print("❌ Error: 'misumi_camFollower.txt' not found. Please run link extraction first.")
#         return
        
#     async with AsyncWebCrawler(config=brows_config) as crawler:
#         for idx,url in enumerate(urls):
#             print(f"\n--- Scraping URL {idx+1}/{len(urls)}: {url} ---")
            
#             # Re-introducing randomized delay for rate limit prevention
#             sleep_time = random.uniform(MIN_DELAY, MAX_DELAY) 
#             print(f"⏳ Inter-request sleep: {sleep_time:.2f} seconds...")
#             await asyncio.sleep(sleep_time)
            
#             result = await crawler.arun(url=url, config=run_config)

#             if result.success:
#                 print("✅ Crawled successfully. Checking content...")
                
#                 # Check for empty content (a final check for debugging)
#                 if not result.markdown.strip():
#                     print("⚠️ WARNING: Markdown output is empty despite successful crawl.")
                
#                 with open("part_number_table.md", "a", encoding="utf-8") as f:
#                     f.write(f"\n\n## Data for URL: {url}\n")
#                     f.write(result.markdown + "\n")
#                     f.write("===END===\n") 
#                     print(f"✨ Saved product {idx+1} data.")
#             else:
#                 print(f"❌ Failed to fetch content for URL {idx+1}: {url}")
#                 if result.error_message:
#                     print(f"   Error: {result.error_message}")


# async def main():
#     await scrape_multiple_urls()


# if __name__ == "__main__":
#     # Wrap the entire execution in a high-level try/except block for stability
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print("\n\nOperation cancelled by user.")
#     except Exception as e:
#         print(f"\n\nAn unexpected error occurred: {e}")



import asyncio
from crawl4ai import AsyncWebCrawler,BrowserConfig,CrawlerRunConfig,CacheMode
from crawl4ai import JsonCssExtractionStrategy
import random
import uuid
import json

part_number_schema={
    "name":"Cam Follower Part_numbers",
    "baseSelector":"div.PartNumberList_mainOuter__d74Qg",
    "fields":[
        {
            "name":"part_number_rows",
            "type":"list",

    "fields":[
        {
            "name":"Part Number",
            "selector":"td.PartNumberColumn_dataCellBase__v1_jf",
            "type":"text",
        },
        {
            "name":"Price",
            "selector":"table.PartNumberAsideColumns_table__6fKVE tr td:nth-child(1)",
            "type":"text",
        },
        {
            "name":"Days to Ship",
            "selector":"table.PartNumberAsideColumns_table__6fKVE tr td:nth-child(2)",
            "type":"text",
        },
        {
            "name":"Minimum order Qty",
            "selector":"table.PartNumberSpecColumns_tableBase__VK5Nd tr>td:nth-child(1)",
            "type":"text",
        },
        {
            "name":"Volumn Discount",
            "selector":"table.PartNumberSpecColumns_tableBase__VK5Nd tr>td:nth-child(2)",
            "type":"text",
        },
        {
            "name":"RoHS",
            "selector":"table.PartNumberSpecColumns_tableBase__VK5Nd tr>td:nth-child(3)",
            "type":"text",
        },
        {
            "name":"Outer Dia. D(mm)",
            "selector":"table.PartNumberSpecColumns_tableBase__VK5Nd tr>td:nth-child(4)",
            "type":"text",
        },
        {
            "name":"Width B(mm)",
            "selector":"table.PartNumberSpecColumns_tableBase__VK5Nd tr>td:nth-child(5)",
            "type":"text",
        },
        {
            "name":"Stud Screw Nominal(M) (mm)",
            "selector":"table.PartNumberSpecColumns_tableBase__VK5Nd tr>td:nth-child(6)",
            "type":"text",
        },
        {
            "name":"Roller Guiding Method",
            "selector":"table.PartNumberSpecColumns_tableBase__VK5Nd tr>td:nth-child(7)",
            "type":"text",
        },
        {
            "name":"Cam Follower: Stud Screw (Fine Thread) (mm)",
            "selector":"table.PartNumberSpecColumns_tableBase__VK5Nd tr>td:nth-child(8)",
            "type":"text",
        },
        {
            "name":"Basic Loading Cr(Dynamic)",
            "selector":"table.PartNumberSpecColumns_tableBase__VK5Nd tr>td:nth-child(9)",
            "type":"text",
        },
        {
            "name":"Basic Loading Cor(Static) (kN)",
            "selector":"table.PartNumberSpecColumns_tableBase__VK5Nd tr>td:nth-child(10)",
            "type":"text",
        },
        {
            "name":"Allowable Rotational Speed (rpm)",
            "selector":"table.PartNumberSpecColumns_tableBase__VK5Nd tr>td:nth-child(11)",
            "type":"text",
        },
        {
            "name":"Seal",
            "selector":"table.PartNumberSpecColumns_tableBase__VK5Nd tr>td:nth-child(12)",
            "type":"text",
        },
        {
            "name":"Application",
            "selector":"table.PartNumberSpecColumns_tableBase__VK5Nd tr>td:nth-child(13)",
            "type":"text",
        },


    ]
        }
    ]

}

async def scrape_multiple_urls():
    brows_config = BrowserConfig(headless=True, verbose=True,browser_type="chromium")
    session_id = str(uuid.uuid4())
    merge_js = """
    (() => {
      try {
        const partTable = document.querySelector("table.PartNumberColumn_tableBase__DK2Le");
        const asideDiv = document.querySelector("table.PartNumberAsideColumns_table__6fKVE");
        const specDiv = document.querySelector("table.PartNumberSpecColumns_tableBase__VK5Nd");

        if (!partTable || !asideDiv || !specDiv) {
          console.log("One or more containers not found");
          return;
        }

        // Get row-level nodes from each section
        const partRows = Array.from(partTable.querySelectorAll("tbody tr"));
        const asideRows = Array.from(asideDiv.querySelectorAll("tr, div"));
        const specRows = Array.from(specDiv.querySelectorAll("tr, div"));

        // Create merged container
        const mergedContainer = document.createElement("div");
        mergedContainer.className = "merged-partnumber-rows";

        const maxLen = Math.max(partRows.length, asideRows.length, specRows.length);

        for (let i = 0; i < maxLen; i++) {
          const mergedRow = document.createElement("div");
          mergedRow.className = "merged-row";

          const p = partRows[i]?.innerText?.trim() || "";
          const a = asideRows[i]?.innerText?.trim() || "";
          const s = specRows[i]?.innerText?.trim() || "";

          mergedRow.innerHTML = `
            <div class='col part'>${p}</div>
            <div class='col aside'>${a}</div>
            <div class='col spec'>${s}</div>
          `;

          mergedContainer.appendChild(mergedRow);
        }

        document.body.appendChild(mergedContainer);
        console.log(" Merged part number rows created successfully");
      } catch (err) {
        console.error(" Merge script error:", err);
      }
    })();
    """

    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=JsonCssExtractionStrategy(part_number_schema),
        exclude_all_images=[],
        exclude_external_links=True,
        only_text=False,
        css_selector="div.PartNumberList_mainOuter__d74Qg",  
        excluded_tags=["header","footer","nav","style","script","aside","form"],
        js_code = """
            console.log('DEBUG: Attempting to find and click Part No. tab...');
             window.scrollTo(0,document.body.scrollHeight);

            const tab = document.querySelector('a[href="#codeList"]');
            
            if (tab) {
                console.log('DEBUG: Part No. tab element found!');
                tab.scrollIntoView({ behavior: 'smooth', block: 'center' });
                
                // Wait for scroll before click
                setTimeout(() => {
                    tab.click();
                    console.log('DEBUG: Part No. tab CLICKED!');
                }, 900); 
                
                // Wait for content to load
                return new Promise(resolve => setTimeout(resolve, 60000)); 
                return True;
            }
            console.log('DEBUG: Part No. tab element NOT FOUND!');
            return false;
        
        """,
        word_count_threshold=5,
        js_only=False,
        scan_full_page=True,
        simulate_user=True,
        scroll_delay=15.0,
        delay_before_return_html=20.0,
        max_scroll_steps=10,
        process_iframes=True,
        remove_overlay_elements=True,
        method="GET",
        check_robots_txt="False",
        session_id=session_id,
        wait_until="load",
        wait_for=None,
    )
    
    with open("misumi_camFollower.txt","r",encoding="utf-8") as f:
        urls=[line.strip() for line in f if line.strip()]

    all_extracted_data=[]  
    async with AsyncWebCrawler(config=brows_config) as crawler:
        for idx,url in enumerate(urls):
            print(f"Scraping URL {idx+1}/{len(urls)}: {url}")
            
            result = await crawler.arun(url=url, config=run_config)

            if result.success:
                print("Crawled successfully")
                try:
                    data=json.loads(result.extracted_content)
                    print(json.dumps(data, indent=2))
                    all_extracted_data.append(data)
                    print(f"Successfully extracted JSON data for {url}")

                except json.JSONDecodeError as e:
                    print("Failed to decode JSON")
            else:
                print(f"Failed to fetch content for URL {idx+1}: {url}")

    print("Scraping completed")
    print(result.extracted_content)
    with open("part_number.json","w",encoding="utf-8") as f:
        json.dump(all_extracted_data,f,indent=4,ensure_ascii=False)

async def main():
    await scrape_multiple_urls()


if __name__ == "__main__":
    asyncio.run(main())