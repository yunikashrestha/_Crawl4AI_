# import os
# import asyncio
# from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
# from bs4 import BeautifulSoup
# import time
# import uuid

# async def pagination_misumi_usa(url):
#     session_id=str(uuid.uuid4())
#     browser_config=BrowserConfig(headless=False, browser_type="Chromium",verbose=True,viewport_width=1400,viewport_height=1000)
#     run_config=CrawlerRunConfig(
#         word_count_threshold=10,
#         css_selector="div.Pagination_container__VOa4I",
#         wait_until="domcontentloaded",
#         delay_before_return_html=5.0,
#         exclude_external_links=True,
#         exclude_social_media_domains=[],
#         exclude_all_images=True,
#         check_robots_txt=True,
#         simulate_user=True,
#         page_timeout=60000,
#         cache_mode=CacheMode.BYPASS
#     )
#     async with AsyncWebCrawler(config=browser_config) as crawler:
#         initial_page=1
#         has_next_button=True
#         while has_next_button:
#             if initial_page==1:
#                 run_config.js_code="""
#             return new Promise((resolve)=>{
#             setTimeout(()=>{
#             const partnumButton=document.querySelector('li.AccordionDetailTab_item__F09i9:nth-child(3)');
#             if (partnumButton) partnumButton.click();
#             resolve(True);
#             },6000)
#             })
#             """
#                 run_config.session_id=session_id
#             else:
#                 run_config.session_id=session_id
#                 run_config.js_only=True
#                 run_config.js_code="""
#             return new Promise((resolve)=>{
#             setTimeout(()=>{
#             const nextButton=document.querySelector("div.Pagination_container__VOa4I>li>a.Pagination_arrowRight__rRbGO")
#             if (nextButton) nextButton.click();
#             resolve(true);
            

#             },4000)
            
#             })
#             """
#             result=await crawler.arun(url=url,config=run_config)
#             print(result)
#             soup=BeautifulSoup(result.html,"html.parser")
#             print(f" The soup is:{soup}")
#             next_button=soup.select_one("div.Pagination_container__VOa4I>li>a.Pagination_arrowRight__rRbGO")
#             initial_page+=1
#             if next_button == None:
#                 has_next_button=False
#             else:
#                 continue

# if __name__=="__main__":
#     target_url="https://us.misumi-ec.com/vona2/detail/110302634310/?list=PageCategory&seriesCode=110302634310&tab=productSpecifications&Page=1"
#     asyncio.run(pagination_misumi_usa(url=target_url))

        


import asyncio
import uuid
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from bs4 import BeautifulSoup

async def pagination_misumi_usa():
    session_id = str(uuid.uuid4())

    browser_config = BrowserConfig(
        headless=False,
        browser_type="Chromium",
        verbose=True,
        viewport_width=1400,
        viewport_height=1000
    )

    base_url = (
        "https://us.misumi-ec.com/vona2/detail/110300001860/?list=PageCategory&seriesCode=110300001860&tab=codeList"
    )

    run_config = CrawlerRunConfig(
        wait_until="domcontentloaded",
        delay_before_return_html=5,
        simulate_user=True,
        cache_mode=CacheMode.BYPASS,
        page_timeout=60000
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        page = 1

        while True:
            url = f"{base_url}&Page={page}"
            print(f"\n Fetching page {page}")

            try:
                result = await crawler.arun(url=url, config=run_config)
            except Exception as e:
                print(f" Crawl error on page {page}: {e}")
                break

            soup = BeautifulSoup(result.html or "", "html.parser")
            title = soup.title.text.strip() if soup.title else ""
            print(f"Title: {title}")

            if "PAGE NOT FOUND" in title.upper():
                print(" Reached last page. Stopping pagination.")
                break

            print(f" Valid page {page} scraped")
            page += 1

if __name__ == "__main__":
    asyncio.run(pagination_misumi_usa())



