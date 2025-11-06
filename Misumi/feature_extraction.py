# import asyncio
# from crawl4ai import AsyncWebCrawler,BrowserConfig,CrawlerRunConfig,CacheMode
# from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
# import random
# import uuid
# async def scrape_multiple_urls():
#     brows_config=BrowserConfig(headless=False,verbose=True,browser_type="chromium")
#     MIN_DELAY = 5.0
#     MAX_DELAY = 10.0
#     session_id=str(uuid.uuid4())

#     run_config=CrawlerRunConfig(
#         cache_mode=CacheMode.BYPASS,
#         markdown_generator=DefaultMarkdownGenerator(),
#         word_count_threshold=20,
#         exclude_all_images=[],
#         exclude_external_links=True,
#         only_text=False,
#         css_selector="div.PartNumberList_main__klm4X",
#         excluded_tags=["header","footer","nav","style","script","aside","form"],
#         js_code = """
#         const tab = document.querySelector('a[href="#codeList"]');
#         if (tab) {
#         tab.scrollIntoView({ behavior: 'smooth', block: 'center' });
#         setTimeout(() => {
#         tab.click();
#         }, 500);
#         return new Promise(resolve => setTimeout(resolve, 6000));
#         }
#         return false;
#         """,

#         js_only=False,
#         scan_full_page=False,
#         simulate_user=True,
#         scroll_delay=15.0,
#         delay_before_return_html=60.0,
#         max_scroll_steps=10,
#         process_iframes=True,
#         remove_overlay_elements=True,
#         method="GET",
#         check_robots_txt="False",
#         session_id=session_id,
#         wait_until="load"

       
#         )
    
#     with open("misumi_camFollower.txt","r",encoding="utf-8") as f:
#         urls=[line.strip() for line in f if line.strip()]
#     async with AsyncWebCrawler(config=brows_config) as crawler:
#         for idx,url in enumerate(urls):
#             print(f"Scraping URL{idx}/{len(urls)}:{url}")
#             # sleep_time = random.uniform(MIN_DELAY, MAX_DELAY) 
#             # print(f"Sleeping for {sleep_time:.2f} seconds to mimic human behavior...")
#             # await asyncio.sleep(sleep_time)
#             result=await crawler.arun(url=url,config=run_config)

#             if result.success:
#                 print("**Crawled successfully**")
#                 print(result.markdown)

#                 with open("part_number_table.md","a",encoding="utf-8")as f:
#                     f.write(result.markdown +"\n")
#                     f.write("===END=="+ "/n")
#                     print(f"***Saved product{idx} description***")
#             else:
#                 print("***Failed to fetch***")
# async def main():
#     await scrape_multiple_urls()

# if __name__=="__main__":
#     asyncio.run(main())
import asyncio
from crawl4ai import AsyncWebCrawler,BrowserConfig,CrawlerRunConfig,CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
import random
import uuid

async def scrape_multiple_urls():
    brows_config = BrowserConfig(headless=False, verbose=True,browser_type="chromium")
    
    MIN_DELAY = 5.0
    MAX_DELAY = 10.0
    session_id = str(uuid.uuid4())

    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        markdown_generator=DefaultMarkdownGenerator(),
        word_count_threshold=5,   
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

        js_only=False,
        scan_full_page=True,
        simulate_user=True,
        scroll_delay=15.0,
        delay_before_return_html=60.0,
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
        
    async with AsyncWebCrawler(config=brows_config) as crawler:
        for idx,url in enumerate(urls):
            print(f"Scraping URL {idx+1}/{len(urls)}: {url}")
            
            sleep_time = random.uniform(MIN_DELAY, MAX_DELAY) 
            print(f"Sleeping for {sleep_time:.2f} seconds to mimic human behavior...")
            await asyncio.sleep(sleep_time)
            
            result = await crawler.arun(url=url, config=run_config)

            if result.success:
                print("Crawled successfully")
                print(result.markdown) 

                with open("part_number_table.md", "a", encoding="utf-8") as f:
                    # Write the successful markdown output
                    f.write(result.markdown + "\n")
                    f.write("===END===\n") # Changed '/n' to '\n' for correct newline
                    print(f"Saved product {idx+1} description to part_number_table.md")
            else:
                print(f"Failed to fetch content for URL {idx+1}: {url}")

async def main():
    await scrape_multiple_urls()


if __name__ == "__main__":
    asyncio.run(main())