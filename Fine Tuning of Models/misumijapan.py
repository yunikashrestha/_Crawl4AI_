import asyncio
from crawl4ai import AsyncWebCrawler,BrowserConfig,CrawlerRunConfig,CacheMode
from bs4 import BeautifulSoup
import uuid

async def pagination_for_japan(url):
    session_id=str(uuid.uuid4())
    brow_config=BrowserConfig(headless=False,verbose=True,viewport_height=1400,viewport_width=1000)
    run_config=CrawlerRunConfig(
        word_count_threshold=10,
        css_selector="div.Pagination_container__VOa4I",
        delay_before_return_html=30.0,
        exclude_external_links=True,
        exclude_social_media_domains=[],
        exclude_all_images=True,
        check_robots_txt=True,
        simulate_user=True,
    )
    async with AsyncWebCrawler(config=brow_config)as crawler:
        initial_page=1
        has_next_button=True
        while has_next_button:
            if initial_page==1:
                run_config.js_code="""
            return new Promise((resolve)=>{
            setTimeout(()=>{
            const partnumButton=document.querySelector("a[href='#codeList']")
            if (partnumButton) partnumButton.click();
            resolve(true);
            },6000)
            })
            """
                run_config.session_id=session_id
            else:
                run_config.session_id=session_id
                run_config.js_only=True
                run_config.js_code="""
            return new Promise((resolve)=>{
            setTimeout(()=>{
            const nextButton=document.querySelector("div.Pagination_container__VOa4I>li>a.Pagination_arrowRight__rRbGO")
            if (nextButton) nextButton.click();
            resolve(true);
            

            },4000)
            
            })

            """
            result=await crawler.arun(url=url,config=run_config)
            print(result)
            soup=BeautifulSoup(result.html,"html.parser")
            print(f" The soup is:{soup}")
            next_button=soup.select_one("div.Pagination_container__VOa4I>li>a.Pagination_arrowRight__rRbGO")
            initial_page+=1
            if next_button == None:
                has_next_button=False
            else:
                continue

if __name__=="__main__":
    target_url="https://jp.misumi-ec.com/vona2/detail/110302634310/?list=PageCategory&clkid=clkid_basic_shape_template"
    asyncio.run(pagination_for_japan(url=target_url))
