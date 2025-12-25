import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig,CacheMode
from bs4 import BeautifulSoup
import uuid

async def pagination_for_misumi_vn(url):
    session_id = str(uuid.uuid4())
    browser_conf = BrowserConfig(headless=False,verbose=True,viewport_width=1400,viewport_height=940)
    crawler_conf = CrawlerRunConfig(
        word_count_threshold=10,
        css_selector="div.Pagination_container__VOa4I",
        delay_before_return_html=30.0,
        exclude_social_media_domains = [],
        exclude_all_images=True,
        exclude_external_images=True,
        check_robots_txt=True,
        # page_timeout=30.0,
        # js_code="""
        # return new Promise((resolve)=>{
        # setTimeout(()=>{
        #     document.querySelector('a[lang="en"]').click();
        # },3000)
        # setTimeout(()=>{
        # const partTab = document.querySelector('a#codeList');
        # if (partTab) partTab.click();
        # resolve(true);
        # },6000)
        # });
        # """,
        # scan_full_page=True,
        simulate_user=True
    )
    async with AsyncWebCrawler(config=browser_conf) as crawler:
        current_page = 1
        has_next_button = True
        while has_next_button:

            if current_page == 1:
                crawler_conf.session_id = session_id
                print("this is the first page")
            else:
                crawler_conf.js_only = True
                crawler_conf.js_code = """
            return new Promise((resolve)=>{
            setTimeout(()=>{
                const nextButton = document.querySelector("div.Pagination_container__VOa4I>li>a.Pagination_next__5fRp8");
                if (nextButton) nextButton.click();
                resolve(true);
            },4000)
            })
            """
                crawler_conf.session_id = session_id
                print(f"this is page {current_page}")
            result = await crawler.arun(url = url,config = crawler_conf)
            soup = BeautifulSoup(result.html,"html.parser")
            next_button = soup.select_one("div.Pagination_container__VOa4I>li>a.Pagination_next__5fRp8")
            current_page += 1
            if next_button == None:
                has_next_button = False
            else:
                continue

async def pagination_for_misumi_us(url):
    session_id = str(uuid.uuid4())
    browser_conf = BrowserConfig(headless=False,verbose=True,viewport_width=1400,viewport_height=940)
    crawler_conf = CrawlerRunConfig(
        word_count_threshold=10,
        css_selector="a.Pagination_arrowRight__rRbGO",
        delay_before_return_html=30.0,
        exclude_social_media_domains = [],
        exclude_all_images=True,
        exclude_external_images=True,
        check_robots_txt=True,
        # page_timeout=30.0,
        # js_code="""
        # return new Promise((resolve)=>{
        # setTimeout(()=>{
        #     document.querySelector('a[lang="en"]').click();
        # },3000)
        # setTimeout(()=>{
        # const partTab = document.querySelector('a#codeList');
        # if (partTab) partTab.click();
        # resolve(true);
        # },6000)
        # });
        # """,
        # scan_full_page=True,
        simulate_user=True
    )
    async with AsyncWebCrawler(config=browser_conf) as crawler:
        current_page = 1
        has_next_button = True
        while has_next_button:

            if current_page == 1:
                crawler_conf.session_id = session_id
                print("this is the first page")
            else:
                crawler_conf.js_only = True
                crawler_conf.js_code = """
            return new Promise((resolve)=>{
            setTimeout(()=>{
                const nextButton = document.querySelector("a.Pagination_arrowRight__rRbGO");
                if (nextButton) nextButton.click();
                resolve(true);
            },4000)
            })
            """
                crawler_conf.session_id = session_id
                print(f"this is page {current_page}")
            result = await crawler.arun(url = url,config = crawler_conf)
            soup = BeautifulSoup(result.html,"html.parser")
            next_button = soup.select_one("a.Pagination_arrowRight__rRbGO")
            current_page += 1
            if next_button == None:
                has_next_button = False
            else:
                continue

async def pagination_for_mitsubishi(url):
    session_id = str(uuid.uuid4())
    browser_conf= BrowserConfig(headless=False,verbose = True, viewport_width=1400, viewport_height=940)
    run_conf = CrawlerRunConfig(
        word_count_threshold=10,
        cache_mode=CacheMode.DISABLED,
        scan_full_page=True,
        simulate_user=True,
        scroll_delay=1.5,
        delay_before_return_html=20.0,
        css_selector= "div.pager_content",
    )
    async with AsyncWebCrawler(config=browser_conf) as crawler:

        current_page = 1
        has_next_button = True
        while has_next_button:
            if current_page == 1:
                print(f"Crawling page number: {current_page}")
                run_conf.session_id = session_id

            else:
                print(f"Crawling page number: {current_page}")
                run_conf.session_id = session_id
                run_conf.js_code = """
            return new Promise((resolve)=>{
            setTimeout(()=>{
            const next_button = document.querySelector("span.pager_sprite_next");
            if (next_button) next_button.click();
            resolve(true);
            },4000)
            })
            """
                run_conf.js_only = True
            result = await crawler.arun(url=url, config=run_conf)
            soup = BeautifulSoup(result.html,"html.parser")
            next_button = soup.select_one("span.pager_sprite_next")
            current_page += 1 
            if next_button == None
        

asyncio.run(pagination_for_misumi_us("https://us.misumi-ec.com/vona2/mech/M0100000000/M0101000000/"))