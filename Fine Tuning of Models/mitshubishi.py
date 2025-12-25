from crawl4ai import AsyncWebCrawler,BrowserConfig,CrawlerRunConfig
import uuid
import asyncio
from bs4 import BeautifulSoup

async def pagination_for_vt(url):
    session_id=str(uuid.uuid4())
    brow_config=BrowserConfig(headless=False,verbose=True,viewport_height=1400,viewport_width=1000)
    run_config=CrawlerRunConfig(
        word_count_threshold=10,
        css_selector="div.pager_content ",
        delay_before_return_html=30.0,
        exclude_external_links=True,
        exclude_social_media_domains=[],
        exclude_all_images=True,
        check_robots_txt=True,
        remove_overlay_elements=True,
        simulate_user=True,

    )
    async with AsyncWebCrawler(config=brow_config)as crawler:
        initial_page=1
        has_next_button=True
        while has_next_button:
            if initial_page==1:
                run_config.session_id=session_id
            else:
                run_config.session_id=session_id
                run_config.js_only=True
                run_config.js_code="""
            return new Promise((resolve)=>{
            setTimeout(()=>{
            const nextButton=document.querySelector("span.pager_sprite_next>a")
            if (nextButton) nextButton.click();
            resolve(true);
            

            },4000)
            
            })

            """
            result=await crawler.arun(url=url,config=run_config)
            print(result)
            soup=BeautifulSoup(result.html,"html.parser")
            print(f" The soup is:{soup}")
            next_button=soup.select_one("span.pager_sprite_next>a")
            initial_page+=1
            if next_button == None:
                has_next_button=False
            else:
                continue

if __name__=="__main__":
    target_url="https://www.mitsubishielectric.co.jp/fa/products/faspec/search.page?kisyu=/servo&page=1&search=B&word=%E5%9B%9E%E8%BB%A2%E5%9E%8B%E3%82%B5%E3%83%BC%E3%83%9C%E3%83%A2%E3%83%BC%E3%82%BF&K-09=MELSERVO-J5"
    asyncio.run(pagination_for_vt(url=target_url))
